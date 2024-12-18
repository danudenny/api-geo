from enum import Enum

class GeometryType(str, Enum):
    Point = "Point"
    MultiPoint = "MultiPoint"
    LineString = "LineString"
    MultiLineString = "MultiLineString"
    Polygon = "Polygon"
    MultiPolygon = "MultiPolygon"
    GeometryCollection = "GeometryCollection"