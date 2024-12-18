from typing import List, Optional, Dict, Any
from geoalchemy2 import Geometry

from pydantic import BaseModel

class ShipmentData(BaseModel):
    shipment_id: str
    pd_id: str
    producer_id: Optional[str]
    producer_name: Optional[str]
    producer_country: str
    production_place: str
    area: float
    polygon: str = Geometry(srid=4326)
    supplier_id: int
    plot_number: int

class GetShipmentByIdResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: List[ShipmentData] or Dict[str, Any]
