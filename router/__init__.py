from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi.params import File

from handlers.geometry_checker_handler import GeometryCheckerHandler
from handlers.shipment_handler import ShipmentHandler
from config.mysql_config import get_db, MySQLConfig

router = APIRouter()
shipment_handler = ShipmentHandler()
geometry_checker_handler = GeometryCheckerHandler()

@router.get("/read_shipment_data")
def get_shipment_by_id(shipment_id : str = Query(...), db: MySQLConfig=Depends(get_db)):
    return shipment_handler.get_shipment_by_id(shipment_id, db)

@router.post("/check_overlap")
async def check_overlap(geojson: UploadFile = File(...)):
    return await geometry_checker_handler.check_overlap(geojson)