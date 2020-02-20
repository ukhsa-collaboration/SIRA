import numpy.random as rand

class FlightTime(object):
    '''
    Simple class to model the distribution of flight time (in hours) from 
    country of origin to the destination country. Flight time, obtained from 
    the method get_flight_time, is used to model the distribution in flight 
    time from between countries
    '''
    
    def __init__(self, flight_dist = None, **kwargs):
        '''
        Initiate a flight time instance for an infected passenger 
        
        Parameters
        ----------
        flight_dist : numpy statsitical distribution function
                Distribution function to model the shape of the distribution of
                the flight time (in hours) for each of the infected travellers
        **kwargs : dict
                Dictionary containing variables to which define the specific 
                shape of the chosen input distirbution of flight times
        '''
        # Set distribution function for flight time
        if flight_dist is None:
            self.flight_dist = rand.normal
        else:
            self.flight_dist = flight_dist
        # Set parameters for flight time
        if not kwargs:
            self.kwargs = {'loc' : 11, 'scale' : 1}
        else:
            self.kwargs = kwargs
        
    def get_flight_time(self):
        '''
        Returns a time (in hours) for length of time taken for some infected 
        individual to travel between origin and destination countries. This is 
        selected according to instances given flight time distribution
        '''
        flight_time = self.flight_dist(**self.kwargs)
        return flight_time