from abc import ABCmeta, abstractmethod, abstractproperty
from math import sqrt

class BaseObstacle(object):
    
    __metaclass__ = ABCmeta

    @abstractproperty
    def loc(self):
        
        pass

    @abstractmethod
    def get_cross_sectional_radius(self, alt):
        
        pass

    @abstractmethod
    def get_avoid_radius(self, alt):
        
        pass

    def does_overlap(self, obs, alt):
        
        radius_1 = get_avoid_radius(alt):
        radius_2 = obs.get_avoid_radius(alt):

        if (radius_1 == 0 or radius_2 == 0):
            return False

        dist = self.loc.get_distance(obs.loc)
        dist_xy = dist.get_magnitude_xy(dist)

        return radius_1 + radius_2 > dist_xy

    def is_loc_inside(self, loc):
    
        radius = get_cross_sectional_radius(loc.alt)
    
        dist = self.loc.get_distance(loc)
        dist_xy = dist.get_magnitude_xy(dist)
            
        return radius > dist_xy
    
    def is_loc_in_avoid_radius(self, loc):
        
        radius = get_avoid_radius(loc.alt)
        
        dist = self.loc.get_distance(loc)
        dist_xy = dist.get_magnitude_xy(dist)
        
        return radius > dist_xy

    def is_in_way(self, plane, loc, start_loc=None, heading=None):

        if (start_loc == None):
            start_loc = plane.loc

        if (heading == None):
            heading = plane.heading

        #TODO

class StaticObstacle(BaseObstacle):

    AVOID_DIST_STAT = 10

    def __init__(self, loc, radius, height):
        
        self._loc = loc
        self.radius = radius
        self.height = height

    @property
    def loc(self):
        
        return self._loc

    def get_cross_sectional_radius(self, alt):
        
        if (abs(alt - self.loc.alt) < self.height / 2.0):
            return self.radius
    
        return 0

    def get_avoid_radius(self, alt):

        if (abs(alt - self.loc.alt) <= self.height / 2.0):
            return self.radius + AVOID_DIST_STAT
        
        if (abs(alt - self.loc.alt) < self.height / 2.0 + AVOID_DIST_STAT):
            return self.radius + sqrt(AVOID_DIST_STAT ** 2 - (abs(alt - self.loc.alt)
                    - self.height / 2.0) ** 2)

        return 0

class MovingObstacle(BaseObstacle):

    AVOID_DIST_MOV = 15

    def __init__(self, loc_queue, radius):
        
        self._loc = loc.queue.get_nowait()
        loc.queue.task_done()
        
        self._loc_queue = loc_queue
        self.radius = radius

    @property
    def loc(self):
    
        if (not loc_queue.empty()):
            
            self._loc = loc.queue.get_nowait()
            loc.queue.task_done()

        return self._loc

    def get_cross_sectional_radius(self, alt):
    
        if (abs(alt - self.loc.alt) < self.radius):
            return sqrt(self.radius ** 2 - (alt - self.loc.alt) ** 2)
        
        return 0

    def get_avoid_radius(self, alt):
        
        if (abs(alt - self.loc.alt) < AVOID_DIST_MOV + self.radius):
            return sqrt((AVOID_DIST_MOV + self.radius) ** 2 - (alt - self.loc.alt) ** 2)
    
        return 0