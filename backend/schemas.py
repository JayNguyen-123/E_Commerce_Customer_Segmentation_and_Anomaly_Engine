from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Dict, Any

class TransactionRecord(BaseModel):
    """
    Validates structural integrity constraint mappings for single transaction rows.
    Protects downstream scikit-learn numpy parsing matrices from dirty logging inputs.
    """
    CustomerID: float = Field(..., description="Unique user identifying tracking integer code matrix key.")
    Quantity: int = Field(..., description="Volumetric calculation count of products ordered.")
    UnitPrice: float = Field(..., description="Fiscal cost per individual stock unit item.")
    InvoiceDate: Any = Field(..., description="Timestamp tracking sequence tracking string or system DateTime tracking layout.")
    InvoiceNo: str = Field(..., description="Unique invoice transaction identifier key tag reference.")

    @field_validator('Quantity')
    @classmethod
    def quantity_must_be_nonzero(cls, v: int) -> int:
        if v == 0:
            raise ValueError('Transaction Quantity calculation cannot sit directly at zero values.')
        return v

    @field_validator('UnitPrice')
    @classmethod
    def unit_price_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Transactional financial unit value fields cannot record negative pricing indexes.')
        return v


class SegmentedCustomerResponse(BaseModel):
    """
    Strict out-of-box schema layout serialization validation tracking rules 
    for returning aggregated client data records back over microservice bridges.
    """
    CustomerID: int = Field(..., description="Aggregated unique customer mapping tracking integer identifier.")
    Recency: int = Field(..., description="Total count day window since customer last made contact with checkout checkouts.")
    Frequency: int = Field(..., description="Volumetric total unique checkout sequences successfully executed over data timeframe lifecycle.")
    Monetary: float = Field(..., description="Cumulative gross monetary allocation spend profiles tracked across record states.")
    Cluster: int = Field(..., description="DBSCAN designated density group tracking indicator allocation (-1 flags system anomalies).")
    PC1: float = Field(..., description="Principal Component Coord Coordinates Point 1.")
    PC2: float = Field(..., description="Principal Component Coord Coordinates Point 2.")
    PC3: float = Field(..., description="Principal Component Coord Coordinates Point 3.")


class PipelineAPIResponse(BaseModel):
    """
    Master container architecture structure defining complete standard JSON communication output 
    configurations shared across system network layers.
    """
    metadata: Dict[str, Any] = Field(
        ..., 
        example={
            "eps": 0.5,
            "min_samples": 5,
            "silhouette_score": 0.6214,
            "total_explained_variance": 0.8432,
            "variance_threshold_met": True
        },
        description="Telemetry calculation states recorded during DBSCAN grid search sweeps and PCA reduction."
    )
    data: List[SegmentedCustomerResponse] = Field(
        ..., 
        description="Collection portfolio compiling the transformed behavioral metrics tracking arrays mapped to cluster positions."
    )
