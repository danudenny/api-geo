from config.mysql_config import MySQLConfig
from services.shipment_services import ShipmentServices
from helpers.response import ResponseHelper
from helpers.logger import log_error


class ShipmentHandler:
    def __init__(self):
        self.shipment_services = ShipmentServices()

    def get_shipment_by_id(self, shipment_id, db:MySQLConfig):
        try:
            return self.shipment_services.get_shipment_by_id(db, shipment_id)
        except Exception as e:
            log_error(e)
            return ResponseHelper.error(error={"message": f"Error: {e}"}, message="Failed to retrieve shipment data")