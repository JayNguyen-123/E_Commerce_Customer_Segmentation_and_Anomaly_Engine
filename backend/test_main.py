import io
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from main import app

# Initialize the programmatic mock client interface wrapper
client = TestClient(app)

@pytest.fixture
def valid_csv_data():
    """
    Generates a structurally valid, minimal raw e-commerce CSV buffer stream
    to pass downstream validation layers safely.
    """
    df = pd.DataFrame({
        'CustomerID':,
        'Quantity':,
        'UnitPrice': [15.50, 4.00, 99.99, 1.25, 24.50],
        'InvoiceDate': [
            '2026-01-01 10:00:00', 
            '2026-01-02 11:00:00', 
            '2026-01-03 12:00:00',
            '2026-01-04 13:00:00',
            '2026-01-05 14:00:00'
        ],
        'InvoiceNo': ['5001', '5002', '5003', '5004', '5005']
    })
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return buf

@pytest.fixture
def invalid_csv_data():
    """
    Generates an invalid CSV buffer missing a mandatory system tracking header
    to test the API's structure-checking capabilities.
    """
    df = pd.DataFrame({
        'CustomerID':,
        'Quantity':,
        # Missing 'UnitPrice' completely to break ingestion logic pipelines
        'InvoiceDate': ['2026-01-01 10:00:00'],
        'InvoiceNo': ['5001']
    })
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return buf

def test_system_health_endpoint():
    """Verifies that the telemetry heartbeat router responds with 200 OK status codes."""
    response = client.get("/health")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["status"] == "healthy"
    assert "cache_layer" in json_resp

def test_segmentation_endpoint_success(valid_csv_data):
    """Verifies valid CSV files are successfully accepted, scaled, and clustered."""
    response = client.post(
        "/segment/", 
        files={"file": ("test_valid.csv", valid_csv_data, "text/csv")}
    )
    assert response.status_code == 200
    json_resp = response.json()
    
    # Structural metadata evaluations
    assert "metadata" in json_resp
    assert "data" in json_resp
    
    metrics = json_resp["metadata"]
    assert "eps" in metrics
    assert "min_samples" in metrics
    assert "silhouette_score" in metrics
    assert "total_explained_variance" in metrics
    assert isinstance(metrics["variance_threshold_met"], bool)
    
    # Verify core tracking indexes mapped cleanly to the json records payload array
    assert len(json_resp["data"]) > 0
    first_record = json_resp["data"][0]
    required_keys = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Cluster', 'PC1', 'PC2', 'PC3']
    for key in required_keys:
        assert key in first_record

def test_segmentation_endpoint_missing_columns(invalid_csv_data):
    """Verifies that the API catches structural missing column schema anomalies before processing data."""
    response = client.post(
        "/segment/", 
        files={"file": ("test_invalid.csv", invalid_csv_data, "text/csv")}
    )
    assert response.status_code == 400
    assert "CSV schema structurally invalid" in response.json()["detail"]

def test_segmentation_endpoint_invalid_file_type():
    """Verifies that the server drops raw text streams or non-CSV asset types instantly."""
    fake_txt = io.BytesIO(b"Hello world database tracking error log raw context")
    response = client.post(
        "/segment/", 
        files={"file": ("malicious_script.txt", fake_txt, "text/plain")}
    )
    # The application will pass text to pandas which fails to find headers, triggering a 400
    assert response.status_code == 400
