from services.geometry_checker_services import GeometryCheckerServices
from helpers.response import ResponseHelper
from helpers.logger import log_error


class GeometryCheckerHandler:
    def __init__(self):
        self.geometry_checker_services = GeometryCheckerServices()

    async def check_overlap(self, geojson):
        try:
            return await self.geometry_checker_services.check_overlap(geojson)
        except Exception as e:
            log_error(e)
            return ResponseHelper.error(error={"message": f"Error: {e}"}, message="Failed to process geometry")