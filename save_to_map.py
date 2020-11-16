from config import config, post_tracker as pt
from geojson import FeatureCollection, dump
import arcgis.gis
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import plotly.graph_objects as go
import pandas as pd
import json

def save_to_arcgis_online(username, password):
    gis = GIS("https://www.arcgis.com", username=username, password=password)
    content = arcgis.gis.ContentManager(gis)

    feature_collection = FeatureCollection(pt.posts_with_location)

    print('Making geojson...')
    with open('matched_posts.geojson', 'w') as f:
        dump(feature_collection, f, indent = 4)

    geojson_path = 'matched_posts.geojson'
    geojson_properties = {
        'title':'Potential Customers',
        'description':'Based on webscraping data from Instagram',
        'tags':'arcgis, python, TK, GeoJSON,', 
        'type': 'GeoJson',
        'spatialReference': {
            'wkid': 3857
        }
        }
    try:
        print('Deleting old map...')
        my_content = content.search(query="title:Potential Customers", 
                                item_type="GeoJSON", 
                                max_items=1)
        old_item = content.get(my_content[0].id)
        old_item.delete()
    except Exception:
        pass
    try:
        print('Making new map...')
        geojson_item = content.add(geojson_properties, geojson_path)
        geojson_item.publish()
    except Exception:
        pass
    print('-------------------------------------------------------------------------------')


def create_map():

    with open('matched_posts.geojson', 'w') as f:
        my_file = json.load(f)

    fig = go.Figure(go.Scattermapbox())

    fig.update_layout(mapbox_style="stamen-terrain", 
                    mapbox_zoom=10, 
                    mapbox_center_lat = 40.58,
                    mapbox_center_lon = -105.08,
                    margin={"r":0,"t":0,"l":0,"b":0},
                    mapbox=go.layout.Mapbox(
                        layers=[{
                            'sourcetype': 'geojson',
                            'source': my_file,
                            'type': 'Feature',
                        }]
                    ))
    fig.show()