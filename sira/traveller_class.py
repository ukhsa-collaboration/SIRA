import numpy.random as rand

class Traveller(object):
    '''
    Class to model travellers who are attempting to gain entry to some
    destination country, who at some point have become infected with a given
    disease. Flight deperture time, obtained from the method get_depart_time
    is used to model the random time prior to their flight, that the individual
    became infected by this disease. 
    '''    
    def __init__(self, exp_dist = None, asymp_prob = None, **kwargs):
        '''
        Initiate an instance of an infected passenger.
        
        Parameters
        ----------
        exp_dist : numpy statsitical distribution function
            Distribution function to model the shape of the distribution of 
            times (in hours) taken from passengers becoming infected to 
            boarding flight to the destination country
        asymp_prob : None or float
            Float to describe the probability that simulated individual is 
            going to be asymptomatic. If value is set to None, model does not
            consider the possibility of asymptomatic infections
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
        # Boolean variable to capture whether person has been detected by 
        # methods of diseas detection
        self.undetected = True
        # Randomly allocate if individual is to be symptomatic or not
        self.get_asymptomatic(asymp_prob)

            
    def get_depart_time(self):
        '''
        Returns a time (in hours) for length of time from infection to boarding
        flight for some infected individual. This is selected according to 
        instances chosen exposure-to-boarding distribution
        '''
        flight_time =  self.exp_dist(**self.kwargs)
        return flight_time

    def get_asymptomatic(self, asymp_prob):
        '''
        Class method to randomly decide whether modelled individual is to be
        symptomatic or asymptomatic

        Parameters
        ----------
        aysmp_prob : float or None
            Float to describe the probability that the modelled individual is 
            to be asymptomatic. If given value is None, function sets 
            asymptomatic to True as default
        '''
        if  asymp_prob is None:
            self.symptomatic = True
        else:
            draw = rand.random()
            if draw < asymp_prob:
                self.symptomatic = True
            else:
                self.symptomatic = False