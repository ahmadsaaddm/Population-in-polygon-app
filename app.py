from flask import Flask, request, render_template, jsonify
import geopandas as gpd
from shapely.ops import unary_union
import pandas as pd

app = Flask(__name__)

gdf_population = gpd.read_file('/Users/population/Downloads/kontur_population_20231101.gpkg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_geojson', methods=['POST'])
def process_geojson():
    try:
        geojson_data = request.get_json()
        
        gdf_polygon = gpd.GeoDataFrame.from_features(geojson_data['features'])
        
        if gdf_polygon.crs is None:
            gdf_polygon.set_crs(epsg=4326, inplace=True)  
        
        # Ensure  geometries valid
        gdf_population_valid = gdf_population[~gdf_population.geometry.is_empty & gdf_population.geometry.is_valid]
        gdf_polygon = gdf_polygon[~gdf_polygon.geometry.is_empty & gdf_polygon.geometry.is_valid]
        
        projected_crs = 'EPSG:3857' 
        gdf_population_valid = gdf_population_valid.to_crs(projected_crs)
        gdf_polygon = gdf_polygon.to_crs(projected_crs)
        
        # Combine all polygon into a single geometry
        polygon_geom = unary_union(gdf_polygon.geometry)
        if not polygon_geom.is_valid:
            return jsonify({"error": "The combined polygon geometry is invalid."})
        
        # Perform the intersection
        gdf_population_valid['intersection'] = gdf_population_valid.geometry.intersection(polygon_geom)
        
        # Check if intersections are valid
        gdf_population_valid['valid_intersection'] = gdf_population_valid['intersection'].is_valid
        gdf_population_valid = gdf_population_valid[gdf_population_valid['valid_intersection']]
        
        # Calculate intersection areas
        gdf_population_valid['intersection_area'] = gdf_population_valid['intersection'].area
        gdf_population_valid['polygon_area'] = gdf_population_valid['geometry'].area
        
        # Handle cases where polygon_area might be zero to avoid division by zero
        gdf_population_valid['polygon_area'] = gdf_population_valid['polygon_area'].replace(0, pd.NA)
        gdf_population_valid['fraction'] = gdf_population_valid['intersection_area'] / gdf_population_valid['polygon_area'].fillna(1)
        
        # Adjust population by the fraction of the area
        gdf_population_valid['adjusted_population'] = gdf_population_valid['population'] * gdf_population_valid['fraction']
        
        # Sum the adjusted population
        total_population = gdf_population_valid['adjusted_population'].sum()
        
        return jsonify({"total_population": float(total_population)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)