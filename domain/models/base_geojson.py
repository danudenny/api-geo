from typing import List, Any
from domain.constants import GeometryType
from pydantic import BaseModel

class Geometry(BaseModel):
    type: GeometryType = GeometryType.Polygon
    coordinates: Any

class Feature(BaseModel):
    type: str
    geometry: Geometry
    properties: Any

    def to_dict(self):
        return self.model_dump()


class GeojsonFormat(BaseModel):
    type: str
    features: List[Feature]

    def to_dict(self):
        return self.model_dump()
