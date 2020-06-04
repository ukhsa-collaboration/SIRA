import numpy.random as rand
import scipy.stats as stats

def scaled_weibull(**kwargs):
    return stats.weibull_min.rvs(**kwargs)

class IncubationPeriod(object):
    '''
    Simple class to model the distribution of incubation periods of a given 
    disease among the infected travellers. Incubation time, obtained from the 
    method get_inc_time, is used to model the random time from infection to 
    developing symptoms for some infected individual
    
    '''
    def __init__(self, inc_dist = None, **kwargs):
        '''
        Initiate an incubation period instance for an infected passenger 
        
        Parameters
        ----------
        inc_dist : numpy statsitical distribution function
                Distribution function to model the shape of the distribution of
                the incubation period (in days or hours) for the disease 
                infecting travellers
        **kwargs : dict
                Dictionary containing variables to which define the specific 
                shape of the chosen input distirbution of incubation periods.
                Parameterisations may be made on scale of hours or days.
        '''
        # Set distribution function for incubation period
        if inc_dist is None:
            self.inc_dist = rand.normal
        elif inc_dist is rand.weibull:
            self.inc_dist = scaled_weibull
        else:
            self.inc_dist = inc_dist
        # Set parameters for incubation period
        if not kwargs:
            self.kwargs = {'loc' : 4*24, 'scale' : 10}
        else:
            self.kwargs = kwargs
        
    def get_inc_time(self, time_scale = 'hours'):
        '''
        Returns a time (in hours) for length of incubation period for some
        infected individual. This is selected according to instances chosen
        incubation period distribution. If parameterisation is made on a 
        time scale of days, set time_scale to "days" to ensure the returned
        value is measured in hours
        '''
        inc_time = self.inc_dist(**self.kwargs)
        
        if time_scale.lower() == 'days':
            inc_time *= 24
        elif time_scale.lower() == 'hours':
            pass
        else:
            return 'Invalid time scale chosen; currently supports "hours" \
                    or "days".'
        return inc_time