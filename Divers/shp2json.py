import geopandas as gpd

# Load shapefile
shapefile_path = "data/routes.shp"
gdf = gpd.read_file(shapefile_path)

# Save as GeoJSON
geojson_path = "data/routes.geojson"
gdf.to_file(geojson_path, driver="GeoJSON")
