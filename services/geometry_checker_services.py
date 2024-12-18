import json
from fastapi import UploadFile
from helpers.logger import log_error
from helpers.response import ResponseHelper
from utils.topology_checker import TopologyChecker
import geopandas as gpd
from shapely import wkt


class GeometryCheckerServices:
    @staticmethod
    async def check_overlap(geojson: UploadFile):
        try:
            checker = TopologyChecker()
            content = await geojson.read()
            geojson_data = json.loads(content)

            # Create GeoDataFrame directly from GeoJSON
            gdf = gpd.GeoDataFrame.from_features(
                geojson_data['features'] if 'features' in geojson_data else [geojson_data],
                crs='EPSG:4326'
            )

            # Add an index column if not present
            if 'id' not in gdf.columns:
                gdf['id'] = range(len(gdf))

            # Perform overlap check
            result = checker.check_overlaps(gdf)

            # Convert WKT geometries back to GeoJSON format
            for item in result:
                geom = wkt.loads(item['geometry'])
                item['geometry'] = gpd.GeoSeries([geom], crs='EPSG:4326').to_json()

            return ResponseHelper.success(data=result)
        except Exception as e:
            log_error(e)
            return ResponseHelper.error(message=f"Failed to process geometry data: {str(e)}")