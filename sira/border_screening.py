# Time scales dealt as hours

from .traveller_class import Traveller
from .flight_time_class import FlightTime
from .incubation_period_class import IncubationPeriod
    

def border_screening(num_people=10, flight_dist = None, inc_dist = None, 
                      exp_dist = None, time_scale = 'hours', reporting = False,
                      **kwargs):
    '''
    Function to explicitly run the modeling of a group of individuals, having
    been infected at some randomly distributed times prior, attempting to 
    take a flight to some destination country and subsequently trying to gain
    entry. Each infected person is allocated a randomly distributed 
    incubation period and a randomly distributed flight time. The model then 
    tests if the person has become symptomatic according to their given 
    incubation period, prior to boarding flight (at origin boarder), on flight 
    (hence displaying symptoms at destination boarder), or not being 
    asypmtomatic on arrival (thus becoming a community case in the destination
    country). If an infected individual is detected as symptomatic at any 
    boarder, they are marked as "DETECTED" at at this boarder and then removed
    from the model 
    
    Parameters
    ----------
    num_people : int
        Number of simulated infected persons to be modelled attempting to 
        travel to the destination country
    flight_dist :  numpy statsitical distribution function
         Distribution function to model the shape of the distribution of
         the flight time (in hours) from origin country, to destination country
         for infected individuals  
    inc_dist : numpy statsitical distribution function
        Distribution function to model the shape of the distribution of
        the incubation period (in hours) for given disease infecting travelling
        individuals
    exp_dist : numpy statsitical distribution function
        Distribution function to model the shape of the distribution of 
        times (in hours) taken from passengers becoming infected to 
        boarding flight to the destination country
    reporting : bool
        True or False, describing whether user wishes for 
        detection/non-detection statistics to be printed to upon the completion
        of simulation
    **kwargs : dict
        Dictionary of dictionaries (with keys 'exp', 'inc' and 'flight') which
        contains the variables used to define the specific shape of the chosen
        input distributions for exp_dist, inc_dist and flight_dist.
    
    Returns
    -------
    detected_ratio : float
        Value describing the ratio of infected persons detected at the boarder
        of the destination country, compared to the amount of infected persons 
        who successfully travel to the detsination country
        
    Example
    -------
    from BoarderScreening.py import boarder_screening
    >>> boarder_screening(num_people = 10000,
                          flight_dist = rand.uniform,
                          exp_dist = rand.normal,
                          inc_dist = rand.uniform, 
                          **{
                             'exp':{'loc':4*24, 'scale':10},
                             'inc':{'low':4*24, 'high':6*24},
                             'flight':{'low':10, 'high':12}
                             }
                          )
    '''
    
    # Count to record how many infected are detected at UK boarder
    people_detected_UK = 0
    # Count to record how many infected are detected prior to leaving the 
    # Chinese boarder
    people_detected_CHINA = 0
    # Count to record how many infected go undetected to enter UK boarder
    people_nondetected = 0
    # Loop the model through each infected person in our group
    for _ in range(num_people):
        # Initiate a instance of an infected traveller
        try:
            person = Traveller(exp_dist, **kwargs['exp'])
        except KeyError:
            person = Traveller(exp_dist)
            
        depart_time = person.get_depart_time()
        
        try:
            inc_period = IncubationPeriod(inc_dist, **kwargs['inc'])    
        except KeyError:
            inc_period = IncubationPeriod(inc_dist) 
            
        symp_onset = inc_period.get_inc_time(time_scale = time_scale) 
        
        try:
            flight = FlightTime(flight_dist, **kwargs['flight'])    
        except KeyError:
            flight = FlightTime(flight_dist) 
            
        flight_time = flight.get_flight_time()
        
        # Test to see if infected case has become symptomatic prior to boarding
        # flight, thus being detected at Chinese boarder
        if symp_onset <= depart_time:
            people_detected_CHINA += 1
        # Test to see if infected case has become symptomatic during flight,
        # thus being detected or arrival at UK boarder
        elif symp_onset <= depart_time + flight_time:
            people_detected_UK += 1
        # Else we assume case has gained entry to UK, thus will go on to become
        # a community case on UK soil
        else:
            people_nondetected += 1
            
    if reporting is True:    
        # Display results for users interpretation
        print('Number of infected people detected at Chinese boarder: ', 
              people_detected_CHINA)
        print('Number of infected people detected at UK boarder: ', 
              people_detected_UK)
        print('Number of infected people passing through UK boarder: ', 
              people_nondetected)
    
    # Total number of infected people who manage to travel to UK boarder
    travel_total = num_people - people_detected_CHINA
    # Ratio of infected people detected by screening
    detected_ratio = people_detected_UK / travel_total
    # Return detection ratio
    return detected_ratio
      