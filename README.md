# 📊 E-Commerce Customer Segmentation & Anomaly Engine

An industrial-grade, unsupervised machine learning pipeline that transforms raw e-commerce transaction logs into actionable marketing cohorts and isolates structural business anomalies. 

Built with a decoupled **FastAPI backend** managing dynamic density sweeps (`DBSCAN`) and dimensionality reduction (`PCA`), and a **Streamlit frontend control center** for real-time 3D data interaction and cohort export extraction.

---

## 🚀 Key Features

*   **RFM Transaction Aggregation**: Automatically transforms flat transactional row logs (invoices, prices, dates) into standard consumer behavioral matrices (*Recency, Frequency, Monetary Value*).
*   **Dynamic DBSCAN Parameter Sweeps**: Replaces static, hardcoded K-Means clustering with a structural grid-search optimization algorithm that chooses density parameters based on maximum `Silhouette Score` metrics.
*   **Outlier & Fraud Filtering**: Leverages density-based parsing to isolate hyper-frequent wholesale accounts, data errors, and single-interaction scrapers as independent anomaly data targets (`Cluster -1`).
*   **Interactive 3D Space Mappings**: Condenses scaled multi-dimensional metrics into three distinct principal coordinates using **Principal Component Analysis (PCA)** for low-latency visual clustering.
*   **Distributed In-Memory Session Caching**: Employs a **Redis** caching ring to instantly return cluster results for duplicate uploads using cryptographic `SHA-256` content hashing, dropping execution times down to sub-millisecond retrieval speeds.
*   **Decoupled Microservice Design**: Architecture is fully separated into a high-performance backend inference server (FastAPI), an in-memory cache grid (Redis), and an analytical presentation dashboard interface (Streamlit).

---

## 🗂️ Project Directory Architecture

```text
customer_segmentation/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions automated test & verification pipeline
│
├── backend/
│   ├── Dockerfile                # Light Python container config for the FastAPI server
│   ├── engine.py                 # Core ML engine (RFM engine, DBSCAN parameter sweep, PCA)
│   ├── main.py                   # FastAPI server entrypoint (Routing, Redis integration)
│   ├── requirements.txt          # Python dependencies required specifically for backend processing
│   ├── schemas.py                # Pydantic data schemas validating transactional data uploads
│   └── test_main.py              # Automated Pytest regression suites checking edge cases
│
├── frontend/
│   ├── app.py                    # Streamlit analytical user interface (3D interactive graphs)
│   ├── Dockerfile                # Web deployment container configuration for Streamlit app
│   └── requirements.txt          # Frontend web panel specific dependencies (Streamlit, Plotly)
│
├── docker-compose.yml            # Infrastructure orchestra file uniting Backend, Frontend & Redis
└── README.md                     # Portfolio technical documentation for engineering hiring managers
```

## 🛠️ Technology Stack & Dependencies

*   **Language**: Python 3.10+
*   **Core Data Ecosystem**: `pandas`, `numpy`, `scikit-learn`
*   **Visual Frameworks**: `plotly-express`, `matplotlib`
*   **Networking / Cache Layer**: `fastapi`, `uvicorn`, `redis`, `requests`
*   **Interface Layer**: `streamlit`
*   **CI/CD & Testing**: `pytest`, `httpx`, GitHub Actions

---

## 💻 Installation & Quickstart

### The One-Command Local Deployment (Recommended)
The absolute fastest way to deploy the entire multi-container infrastructure is via Docker Compose. Ensure you have Docker installed, and execute from the root directory:

```bash
docker-compose up --build
```

### Manual Local Development Set Up
If you prefer to run the components independently inside a local environment without container wrappers:

```bash
# Initialize and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install all backend and frontend dependencies
pip install -r backend/requirements.txt -r frontend/requirements.txt

# Run the backend API server (Ensure you have a local Redis server running on port 6379)
cd backend && uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# In a separate terminal tab, run the Streamlit UI panel
cd frontend && streamlit run app.py
```

---

## 🔬 Deep Technical Specifications

### Input Schema Validation Layer
Incoming raw byte uploads are systematically parsed and run against a structured `Pydantic v2` validation layer mapping to ensure pipeline security. The API engine instantly catches and drops records containing negative transactional pricing matrices or missing spatial consumer identifiers before inference scripts map metrics to system RAM.

### Dimensionality Reduction & Variance Safeguards
To preserve structural integrity during the multi-dimensional mapping phase, the engine records individual eigenvector eigenvalues. 

$$\text{Cumulative Variance Ratio} = \sum_{i=1}^{3} \lambda_i$$

A system telemetry check verifies whether the combined 3 principal components (PC1, PC2, PC3) capture $\ge 80\%$ of the initial log-transformed dataset's variance distribution. This guarantees that your interactive 3D charts display accurate mathematical patterns rather than vague visual approximations.

### Distributed In-Memory Session Caching
The application embeds a high-performance database caching ring utilizing **Redis (Remote Dictionary Server)**. 

$$\text{Session Cache Key} = \text{SHA256}(\text{Raw Binary Upload Data Stream})$$

When an analyst uploads a transaction log file, the server evaluates its unique cryptographic fingerprint hash. If a duplicate file hash matches an existing record in the key-value store, the engine instantly bypasses the data scaling, DBSCAN parameter sweep, and PCA algorithms entirely, streaming the results back under sub-millisecond retrieval speeds.

### Automated GitHub Actions CI/CD Pipeline
Continuous Integration is fully managed via automated GitHub workflows (`.github/workflows/ci-cd.yml`). Every single Pull Request or codebase push triggers a cloud runner worker container that:
1. Provisions an isolated Linux kernel container runtime environment.
2. Spins up a sidecar infrastructure dependency instance of a Redis caching system.
3. Automatically runs the complete end-to-end `pytest` unit test verification suite (`test_main.py`).

This layout pipeline structural loop guarantees that no breaking logic modifications or structural regression mutations are ever merged into the main deployment frames.

---

## 📊 Business Persona Deliverables

The engine classifies structural consumer behavior into standard analytical categories:

*   **Core Champions**: High frequency patterns with low day counts since last interaction. *Action plan: Early-access product incentives.*
*   **At-Risk Accounts**: Historically high spenders exhibiting elevated inactivity periods. *Action plan: High-incentive target campaigns.*
*   **System Outliers (`Cluster -1`)**: Entities with unnatural behavior traits or extreme spend concentrations. *Action plan: Flag for B2B accounts review or fraud detection scrutiny.*
