from pyexpat import features

from shapely.geometry.point import Point

from config.mysql_config import MySQLConfig
from helpers.logger import log_error
from helpers.response import ResponseHelper
from shapely import wkt

class ShipmentServices:
    @staticmethod
    def get_shipment_by_id(db: MySQLConfig, shipment_id: str):
        try:
            query = """
                SELECT DISTINCT
                    posi.shipment_id,
                    posipd.id AS pd_id,
                    posipd.producer_id,
                    posipd.producer_name,
                    posipd.producer_country,
                    posipd.production_place,
                    posipd.area,
                    st_astext (posipp.submitted_polygon, 'axis-order=long-lat') AS polygon,
                    posip.producer_id AS supplier_id,
                    posip.plot_number
                FROM purchase_order_shipment_items posi
                    INNER JOIN purchase_order_shipment_item_producers posip ON posi.id = posip.shipment_item_id
                    INNER JOIN purchase_order_shipment_item_producer_details posipd ON posip.producer_detail_id = posipd.id
                    INNER JOIN purchase_order_shipment_item_producer_polygons posipp ON posip.producer_detail_id = posipp.producer_id
                    WHERE posi.shipment_id = %s
            """

            db.execute(query, (shipment_id,))
            results = db.fetchall()

            if not results:
                log_error(f"No results found for shipment id: {shipment_id}")
                return ResponseHelper.not_found(error={"message": f"No results found for shipment id: {shipment_id}"})

            feature_collection = {
                "type": "FeatureCollection",
                "features": []
            }
            for result in results:
                properties = {
                    "shipment_id": result["shipment_id"],
                    "pd_id": result["pd_id"],
                    "producer_id": result["producer_id"],
                    "producer_name": result["producer_name"],
                    "producer_country": result["producer_country"],
                    "production_place": result["production_place"],
                    "area": result["area"],
                    "supplier_id": result["supplier_id"],
                    "plot_number": result["plot_number"]
                }

                if isinstance(result["polygon"], str):
                    result["polygon"] = wkt.loads(result["polygon"])
                    if isinstance(result["polygon"], Point):
                        result["polygon"] = result["polygon"].buffer(0.00009)
                        result["polygon"] = result["polygon"].wkt

                coordinates = [[x, y] for x, y in zip(result["polygon"].exterior.coords.xy[0], result["polygon"].exterior.coords.xy[1])]
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coordinates]
                    },
                    "properties": properties
                }

                feature_collection["features"].append(feature)

            return ResponseHelper.success(data=feature_collection, message="Success")
        except Exception as e:
            log_error(e)
            return ResponseHelper.error(error={"message": f"Error: {e}"}, message="Failed to retrieve shipment data")