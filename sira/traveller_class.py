import numpy.random as rand

class Traveller(object):
    '''
    Class to model travellers who are attempting to gain entry to some
    destination country, who at some point have become infected with a given
    disease. Flight deperture time, obtained from the method get_depart_time
    is used to model the random time prior to their flight, that the individual
    became infected by this disease. 
    '''    
    def __init__(self, exp_dist = None, **kwargs):
        '''
        Initiate an instance of an infected passenger.
        
        Parameters
        ----------
        exp_dist : numpy statsitical distribution function
            Distribution function to model the shape of the distribution of 
            times (in hours) taken from passengers becoming infected to 
            boarding flight to the destination country
        **kwargs : dict
            Dictionary containing variables to which define the specific shape
            of the chosen input distirbution of time taken from becoming 
            infected to boarding plane
        '''
        # Set distribution function of time from exposure to boarding flight
        if exp_dist is None:
            self.exp_dist = rand.normal
        else:
            self.exp_dist = exp_dist
        # Set parameters of time from exposure to boarding flight distibrution
        if not kwargs:
            self.kwargs = {'loc' : 4*24, 'scale' : 10}
        else:
            self.kwargs = kwargs 
            
    def get_depart_time(self):
        '''
        Returns a time (in hours) for length of time from infection to boarding
        flight for some infected individual. This is selected according to 
        instances chosen exposure-to-boarding distribution
        '''
        flight_time =  self.exp_dist(**self.kwargs)
        return flight_time