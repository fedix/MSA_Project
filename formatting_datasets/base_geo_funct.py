"""
Module provides basic geo-orienting functions:
    - distance_between(location_1, location_2);
    - within_radius(location, radius, places_set[]);
    - build_geogrid(x_tiles, y_tiles, grid_corners);
    - count_obj(geopoint, radius, category, places_set[]).

Used in:
    - Scientific project (itinerary construction);
    - BD and ML course project (parse,  analyze and
                                clean geo-database);
    - Statistic analisys project (analysis of places
                                  distribution on map).
"""


from geopy import distance
from numpy import mean


def dist_between(locat_1, locat_2):
    """
    Calculates distance between two locations (geo-coord).
    Based on geopy.distance.distance(), but allows additionaly
    direct using of dictionsries with "lat", "lng" fields.
    """
    # create Python "set" (used in geopy) from "dict":
    geopoint_1 = (locat_1["lat"], locat_1["lng"])
    geopoint_2 = (locat_2["lat"], locat_2["lng"])
    dist = distance.distance(geopoint_1,
                             geopoint_2).km
    return dist

def within_radius(location, radius, places_set):
    """
    Divide places to two categories:
    within and out of "radius" from "location".
    Input:
    Geo-coordinates of "location" center and "radius" (km).
    Dataset of objects with defined latitude and longitude
    in format: [{"lat": value, "lng": value}, {place_2}, ...]
    Output:
    Python "dict" with two datasets of the original format:
    {'within': [], 'out_of': []}
    """
    within = []
    out_of = []
    for place in places_set:
            dist = dist_between(location, place)
            if dist < radius:
                within.append(place)
            else:
                out_of.append(place)
    return {'within': within, 'out_of': out_of}

def build_geogrid(x_tiles, y_tiles, grid_corners):  
    """
    Build the geo-coordinates grid in shape of parallelogram
    based on coordinates (lat, lng) of three corners.
    Input:
    Number of grid tiles in x/y direction
    and "list" with geo-coordinates of 3 points:
    [{"lat": value, "lng": value}, {point_2}, {point_3}]
    Output:
    Matrix with parallelogram grid of geo-coordinates
    and this parallelogram`s center.
    """
    coord_origin = grid_corners[0]
    max_x = grid_corners[1]
    max_y = grid_corners[2]
    
    # latitude and longitude steps in x/y directions:
    lat_step_x = (max_x["lat"] - coord_origin["lat"])/x_tiles
    lng_step_x = (max_x["lng"] - coord_origin["lng"])/x_tiles
    lat_step_y = (max_y["lat"] - coord_origin["lat"])/y_tiles
    lng_step_y = (max_y["lng"] - coord_origin["lng"])/y_tiles
    
    grid_step_x = {'lat': lat_step_x, 'lng': lng_step_x}
    grid_step_y = {'lat': lat_step_y, 'lng': lng_step_y}

    grid_nodes = []
    node_No = 0
    
    for y in range(y_tiles):
        for x in range(x_tiles):
            
            lat_shift = (x * grid_step_x["lat"] +
                         y * grid_step_y["lat"])
            lng_shift = (x * grid_step_x["lng"] +
                         y * grid_step_y["lng"])
            
            node_lat = coord_origin["lat"] + lat_shift
            node_lng = coord_origin["lng"] + lng_shift
            
            grid_nodes.append({"No": node_No,
                               "lat": node_lat,
                               "lng": node_lng})
            node_No += 1
    
    center = {"lat": mean([max_x["lat"],
                           max_y["lat"]]),
              "lng": mean([max_x["lng"],
                           max_y["lng"]])}
    
    side_x = dist_between(coord_origin, max_x)
    side_y = dist_between(coord_origin, max_y)
    step_x_km = side_x / x_tiles
    step_y_km = side_y / y_tiles
    
    geo_grid = {"nodes": grid_nodes,
                "center": center,
                "side_x": side_x,
                "side_y": side_y,
                "step_x": step_x_km,
                "step_y": step_y_km}
    
    return geo_grid

def count_obj(geopoint, radius, category, places_set):
    """
    Counts places in "places_set" having predefined
    "category", inside the "radius" around the "geopoint".
    """
    counted = 0
    for place in places_set:
        cat_list = place['categories']
        for cat in cat_list:
            if cat == category:
                if dist_between(place, geopoint) < radius:
                    counted += 1
    return counted

