import io
import os
import redis
import json
import hashlib
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from engine import process_and_cluster

# Initialize the FastAPI server application
app = FastAPI(
    title="Customer Segmentation & Anomaly API",
    version="1.0.0",
    description="Production-grade unsupervised ML inference microservice with Redis caching layers."
)

# Enable Cross-Origin Resource Sharing (CORS) for flexible container networking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize connectivity configurations pointing to the Redis service container
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    cache = redis.Redis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        db=0, 
        decode_responses=True,
        socket_connect_timeout=2  # Short timeout to prevent server block if Redis is booting up
    )
except Exception:
    cache = None

@app.get("/health")
def health_check():
    """System telemetry heartbeat validation endpoint."""
    redis_status = "online"
    if cache is None:
        redis_status = "offline"
    else:
        try:
            cache.ping()
        except redis.exceptions.ConnectionError:
            redis_status = "offline"
            
    return {"status": "healthy", "cache_layer": redis_status}

@app.post("/segment/")
async def segment_customers(file: UploadFile = File(...)):
    """
    Accepts raw transactional CSV files, runs input data structure validations,
    evaluates cryptographic hash states against Redis cache rings, and fires ML inferences.
    """
    # 1. Read binary stream data content safely from incoming payload
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file stream payload: {str(e)}")

    # 2. Cryptographic Cache Fingerprinting Layer
    file_hash = hashlib.sha256(contents).hexdigest()
    
    if cache is not None:
        try:
            cached_result = cache.get(file_hash)
            if cached_result:
                # Cache Hit: Instantly stream string payload out back to caller microservice
                return json.loads(cached_result)
        except redis.exceptions.ConnectionError:
            pass  # Fail-safe: Bypass cache hit lookup gracefully if connection drops

    # 3. CSV File Structural Validation Checking
    try:
        raw_df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Uploaded file streaming asset is not a valid CSV layout structure.")

    # Pydantic-equivalent column existence schema structure checks
    required_cols = ['CustomerID', 'Quantity', 'UnitPrice', 'InvoiceDate', 'InvoiceNo']
    missing_cols = [col for col in required_cols if col not in raw_df.columns]
    if missing_cols:
        raise HTTPException(
            status_code=400, 
            detail=f"CSV schema structurally invalid. Missing target columns: {missing_cols}"
        )

    # 4. Invoke Core Machine Learning Engine Calculations
    try:
        processed_rfm, metrics = process_and_cluster(raw_df)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Downstream machine learning execution engine failed to parse matrix arrays: {str(e)}"
        )

    # 5. Serialization and Cache Storage Write-Back Operations
    # Flatten index structure to preserve CustomerID inside standard dictionary payloads
    result_json = processed_rfm.reset_index().to_dict(orient="records")
    response_payload = {"metadata": metrics, "data": result_json}

    if cache is not None:
        try:
            # Set key with an explicit Time-To-Live (TTL) expiration window of 1 Hour (3600s)
            cache.setex(file_hash, 3600, json.dumps(response_payload))
        except redis.exceptions.ConnectionError:
            pass  # Safeguard: Do not crash production runtime if cache writing fails

    return response_payload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
