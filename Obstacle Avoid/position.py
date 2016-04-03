from math import sin, cos

from unit_conversions import deg_to_rad

class Distance(object):

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

    def get_magnitude(self):
    
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def get_magnitude_xy(self):
        
        return sqrt(self.x ** 2 + self.y ** 2)

    def get_transform(self, angle):
        
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        z = self.z

        return Distance(x, y, z)

class Location(object):
    
    EARTH_RADIUS = 6378137
    EARTH_ECCEN = 0.0818191908
    
    def __init__(self, lon, lat, alt):
        
        self.lon = lon
        self.lat = lat
        self.alt = alt

    def _get_earth_radii(self):
    
        r_1 = (EARTH_RADIUS * (1 - EARTH_RADIUS ** 2) /
               (1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2) ** (3 / 2))
        r_2 = EARTH_RADIUS / sqrt(1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2)
           
        return (r_1, r_2)

    def get_distance(self, loc_2, angle=0):
    
        e_radii = _get_earth_radii()
        
        x = e_radii[1] * cos(self.lat) * (loc_2.lon - self.lon)
        y = e_radii[0] * (loc_2.lat - self.lat)
        z = loc_2.alt - self.alt
        
        dist = Distance(x, y, z)
        
        return dist.get_transform(angle)

    def get_location(self, dist):
        
        e_radii = _get_earth_radii()
    
        lat = dist.y / e_radii[0] + self.lat
        lon = dist.x / e_radii[1] / cos(self.lat) + self.lon
        alt = self.alt + dist.alt
    
        return Location(lat, lon, alt)
    
    def get_distance(self, loc_2, angle=0):
    
    @classmethod
    def convert_location(cls, global_relative_frame):
        
        lon = deg_to_rad(global_relative_frame.lon)
        lat = deg_to_rad(global_relative_frame.lat)
        alt = global_relative_frame.alt

        return cls(lon, lat, alt)