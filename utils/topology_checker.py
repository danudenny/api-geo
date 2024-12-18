from shapely.strtree import STRtree
from helpers.logger import log_info, log_debug, log_warning, log_error
import time
import geopandas as gpd
from typing import Optional, List
from rtree import index

class CalculationResult:
    def __init__(self, geom1_area: float, geom2_area: float, overlap_area: float):
        self.geom1_area = float(geom1_area)
        self.geom2_area = float(geom2_area)
        self.overlap_area = float(overlap_area)


class TopologyChecker:
    def __init__(self):
        self.spatial_index = None

    def get_utm_epsg(self, lat: float, lon: float) -> int:
        utm_band = str(int((lon + 180) / 6) + 1)
        if lat > 0:
            return int('326' + utm_band.zfill(2))
        else:
            return int('327' + utm_band.zfill(2))

    def calculate_areas(self, geom1, geom2, overlap_geom) -> CalculationResult:
        centroid = geom1.centroid
        utm_epsg = self.get_utm_epsg(centroid.y, centroid.x)

        geom1_utm = gpd.GeoSeries([geom1], crs='EPSG:4326').to_crs(f'EPSG:{utm_epsg}').iloc[0]
        geom2_utm = gpd.GeoSeries([geom2], crs='EPSG:4326').to_crs(f'EPSG:{utm_epsg}').iloc[0]
        overlap_utm = gpd.GeoSeries([overlap_geom], crs='EPSG:4326').to_crs(f'EPSG:{utm_epsg}').iloc[0]

        return CalculationResult(
            geom1_area=geom1_utm.area,
            geom2_area=geom2_utm.area,
            overlap_area=overlap_utm.area
        )

    def create_spatial_index(self, gdf: gpd.GeoDataFrame) -> index.Index:
        idx = index.Index()
        for i, geom in enumerate(gdf.geometry):
            idx.insert(i, geom.bounds)
        return idx

    def check_overlaps(self, gdf1: gpd.GeoDataFrame, gdf2: Optional[gpd.GeoDataFrame] = None) -> List[dict]:
        gdf1 = gdf1 if gdf1.crs == 'EPSG:4326' else gdf1.to_crs('EPSG:4326')
        if gdf2 is not None:
            gdf2 = gdf2 if gdf2.crs == 'EPSG:4326' else gdf2.to_crs('EPSG:4326')
        else:
            gdf2, self_check = gdf1, True

        geometries = gdf2.geometry.values
        polygon_overlaps = {}
        invalid_count = 0

        log_info("Building STRtree spatial index...")
        tree = STRtree(geometries)

        start_time = time.time()
        processed = 0

        def process_overlap(idx1: int, idx2: int, geom1, geom2) -> None:
            overlap_geom = geom1.intersection(geom2)
            if overlap_geom.area <= 0:
                return

            areas = self.calculate_areas(geom1, geom2, overlap_geom)

            if idx1 not in polygon_overlaps:
                polygon_overlaps[idx1] = {
                    'geometry': geom1,
                    'total_overlap_area': areas.overlap_area,
                    'overlapping_with': {idx2},
                    'original_area': areas.geom1_area
                }
            else:
                polygon_overlaps[idx1]['total_overlap_area'] += areas.overlap_area
                polygon_overlaps[idx1]['overlapping_with'].add(idx2)

            if idx2 not in polygon_overlaps:
                polygon_overlaps[idx2] = {
                    'geometry': geom2,
                    'total_overlap_area': areas.overlap_area,
                    'overlapping_with': {idx1},
                    'original_area': areas.geom2_area
                }
            else:
                polygon_overlaps[idx2]['total_overlap_area'] += areas.overlap_area
                polygon_overlaps[idx2]['overlapping_with'].add(idx1)

        for idx1, geom1 in enumerate(gdf1.geometry.values):
            if idx1 % 5000 == 0:
                elapsed = time.time() - start_time
                rate = idx1 / elapsed if elapsed > 0 else 0
                log_info(f"Processing feature {idx1}/{len(geometries)} ({rate:.1f} features/sec)")

            if not geom1.is_valid:
                invalid_count += 1
                continue

            try:
                for idx2 in tree.query(geom1):
                    if self_check and idx2 <= idx1:
                        continue

                    processed += 1
                    if processed % 1000 == 0:
                        log_info(f"Checked {processed} potential intersections")

                    geom2 = geometries[idx2]
                    if geom2.is_valid and geom1.intersects(geom2) and not geom1.touches(geom2):
                        try:
                            process_overlap(idx1, idx2, geom1, geom2)
                        except Exception as e:
                            invalid_count += 1
                            log_debug(f"Error processing intersection: {e}")
            except Exception as e:
                invalid_count += 1
                log_debug(f"Error processing feature {idx1}: {e}")

        if invalid_count:
            log_warning(f"Skipped {invalid_count} invalid geometry pairs")

        result = []
        for idx, data in polygon_overlaps.items():
            if data['original_area'] > 0:
                overlap_percentage = (data['total_overlap_area'] / data['original_area']) * 100
                is_major = overlap_percentage > 20

                try:
                    geom_wkt = data['geometry'].wkt if data['geometry'] is not None else None

                    if geom_wkt is None:
                        continue

                    result_item = {
                        'error_type': 'major_overlap' if is_major else 'minor_overlap',
                        'feature_id': int(idx),
                        'geometry': geom_wkt,
                        'overlap_percentage': float(overlap_percentage),
                        'total_overlap_area_m2': float(data['total_overlap_area']),
                        'original_area_m2': float(data['original_area']),
                        'overlapping_with': [int(x) for x in data['overlapping_with']],
                        'remarks': f'{"Major" if is_major else "Minor"} overlap '
                                   f'({overlap_percentage:.2f}%) with {len(data["overlapping_with"])} polygons'
                    }
                    result.append(result_item)
                except Exception as e:
                    log_error(f"Error processing result for feature {idx}: {str(e)}")
                    continue

        return result