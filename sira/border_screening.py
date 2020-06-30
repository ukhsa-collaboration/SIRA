# Time scales dealt as hours

from .traveller_class import Traveller
from .flight_time_class import FlightTime
from .incubation_period_class import IncubationPeriod

import numpy.random as rand
    
def _is_detected(detect_prob):
    '''
    Function to capture whether a traveller who has become symptomatic is 
    detected as such, after undergoing border screening. In particular, this
    function allows for an imperfect rate of detection
    
    Parameters
    ----------
    detect_prob : float
        A value in the semi-open range (0,1], specifying the success rate of
        screening; the probability that screening will detect a symptomatic 
        traveller
        
    Returns
    -------
    detection : bool
        Value describing whether a symptomatic traveller has been successfully
        detected by the screening process or not
    '''
    if detect_prob == 1:
        detection = True
    else:
        detection = (rand.random() < detect_prob)
    return detection
    

def border_screening(num_people=10, flight_dist = None, inc_dist = None, 
                      exp_dist = None, time_scale = 'hours', reporting = False,
                      full_output = False, exit_scr_sens = 1, entry_scr_sens = 1, 
                      second_screen = None, release_time = None, asymp_prob = None,
                      **kwargs):
    '''
    Function to explicitly run the modeling of a group of individuals, having
    been infected at some randomly distributed times prior, attempting to 
    take a flight to some destination country and subsequently trying to gain
    entry. Each infected person is allocated a randomly distributed 
    incubation period and a randomly distributed flight time. The model then 
    tests if each person has become symptomatic, according to their given 
    incubation period, prior to boarding flight (at origin border), on flight 
    (hence displaying symptoms at destination boarder), or not being 
    sypmtomatic on arrival (thus becoming a community case in the destination
    country). If an infected individual is detected as symptomatic at any 
    boarder, they are marked as "DETECTED" at this boarder and then removed
    from the model.

    Additional functionality has been added through the use of the parameters
    `second_screen` and `release_time`. These allow the user to simulate the 
    scenarion where travellers, after arriving at their destination border and
    undergoing their entry screening, must complete a period of self-
    isolation. They are then screened again at `second_screen` after their 
    initial screening. If they test positive here, they are then released at
    `release_time` after arrival. To deploy this feature, both parameters must
    be specified, else the model shall revert to its base function.
    
    The base model assumes that border screening is 100% effective at both the
    origin border and destination border, and thus travellers who are
    symptomatic prior to crossing of these borders will always be removed from
    the model. Use of the parameters "exit_scr_sens" and "entry_scr_sens" then 
    allows the users to introduce some probability of failure into these 
    processes. 
    
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
    time_scale : str
        Parameter to define whether the incuabtion period has been defined over
        a scale of hours, or days, as model requires incubation period to be 
        given in the form of hours. Accepts values "hours" or "days"; if value 
        "days" is passed, the program will convert the incubation period from
        days to hours. If "hours" is given no further operation is undertaken.  
    reporting : bool
        True or False, describing whether user wishes for 
        detection/non-detection statistics to be printed to upon the completion
        of simulation
    full_output : bool
        True or False, describing whether users wishes for list containing
        the detection counts to be returned. List is returned in the form:
        [non-fliers-count, detected-on-arrival-count, 
        detected-at-second-test-count, 
        symptomatics-detected-before-release-count,
        non-detecteds-count]
    exit_scr_sens : float
        To take value in the semi-open range (0,1], specifying the exit 
        screening sensitivty; the probability that exit screening will detect
        symptomatic cases, and hence remove them from the model
    entry_scr_sens : float
        To take value in the semi-open range (0,1], specifying the entry 
        screening sensitivty; the probability that entry screening will detect
        symptomatic cases, and hence remove them from the model
    second_screen : float
        numerical value to, in the instance that a self-isolation period is 
        wished to be deployed in the model, specify at which time after the
        initial testing the traveller is to be tested again. Must be specified
        in conjunction with `release_time` for functionality to be implemented.
        TO BE GIVEN IN HOURS AFTER ARRIVAL INTO DESTINATION COUNTRY.
    release_time : float
        numerical value to, in the instance that a self-isolation period is 
        wished to be deployed in the model, specify at which time after the
        initial testing the traveller is set to be release (give they tested
        negative in both administered tests). Must be specified in conjunction
        with `second_screen` for functionality to be implemented. TO BE GIVEN 
        IN HOURS AFTER ARRIVAL INTO DESTINATION COUNTRY.
    asymp_prob : float or None
        Parameter to take value of either None, or float in the range (0, 1).
        This the describes the probability that modelled inidividuals are to 
        be asymptomatic. If assumes value None, sets individual to be 
        symptomatic as default
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
    from border_screening import boarder_screening
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
    
    self_isolation = False

    if not((0 < entry_scr_sens <= 1) and (0 < exit_scr_sens <= 1)):
        print("ValueError: parameters entry_scr_sens and exit_scr_sen are \
               probabilities, and hence must assume values in the range \
               (0,1]")
        return
        
    # Assign a veriable to describe whether self-isolation is being 
    # enforced, based on input parameters (note both parameters must be
    # specified for self-isolation to run)
    if (second_screen is not None) and (release_time is not None):
        # We require release time to be after second testing time, else
        # model reverts back to base version (no self-isolation)
        if second_screen < release_time:
            self_isolation = True

    # Count to record how many infected are detected at arrival boarder
    people_detected_arrival = 0
    # Count to record how many infected are detected prior to leaving the 
    # departing country
    people_detected_departure = 0
    # Count to record how many infected go undetected to enter UK boarder
    people_undetected = 0
    # Count to record how many infected detected after second testing (if 
    # self-isolation is being enforced)
    people_detected_secondtest = 0
    # Count to record how many infected detected after isolation (if 
    # self-isolation is being enforced)
    people_detected_release = 0

    # Loop the model through each infected person in our group
    for _ in range(num_people):
        # Initiate a instance of an infected traveller
        try:
            person = Traveller(exp_dist, asymp_prob, **kwargs['exp'])
        except KeyError:
            person = Traveller(exp_dist)
            
        # Get the amount of time from traveller being infected, to
        # boarding their flight      
        depart_time = person.get_depart_time()
        
        # If traveller is to become symptomatic, get incubation period
        if person.symptomatic:
            try:
                inc_period = IncubationPeriod(inc_dist, **kwargs['inc'])    
            except KeyError:
                inc_period = IncubationPeriod(inc_dist)
        # Else, traveller is to be assymptomatic; get distirbution
        # according to which assymptomatic travellers become detectable
        # by testing. Note that in this case, we still assign this 
        # distribution to the parameter `inc_period`
        else:
            try:
                inc_period = IncubationPeriod(inc_dist, **kwargs['inc'])    
            except KeyError:
                inc_period = IncubationPeriod(inc_dist)

        # Using the distribution `inc_period`, we then get the time of
        # symptom onset, or in the case that the traveller is 
        # asymptomatic, the time at which they become detecable to testing    
        symp_onset = inc_period.get_inc_time(time_scale = time_scale) 
        
        try:
            flight = FlightTime(flight_dist, **kwargs['flight'])    
        except KeyError:
            flight = FlightTime(flight_dist) 

        # Get amount of time taken for our traveller to fly from origin to 
        # destination country    
        flight_time = flight.get_flight_time()
        
        # Test to see if infected case has become symptomatic prior to boarding
        # flight, thus being detected at Chinese boarder
        if symp_onset <= depart_time:
            if _is_detected(exit_scr_sens):
                people_detected_departure += 1
                person.undetected = False
        
        # Test to see if infected case has become symptomatic during flight,
        # thus being detected or arrival at UK boarder
        if symp_onset <= depart_time + flight_time and person.undetected:
            if _is_detected(entry_scr_sens):
                people_detected_arrival += 1
                person.undetected = False
        
        # If a self-isolation phase is being included in this model, we then 
        # enter our traveller into this stage
        if self_isolation and person.undetected:
            if symp_onset <= depart_time + flight_time + second_screen:
                if _is_detected(entry_scr_sens):
                    people_detected_secondtest += 1
                    person.undetected = False
            elif person.symptomatic and person.undetected:
                if symp_onset <= depart_time + flight_time + release_time:
                    if _is_detected(entry_scr_sens):
                        people_detected_release += 1 
                        person.undetected = False           
        # Else we assume case has gained entry to UK, thus will go on to become
        # a community case on UK soil
        if person.undetected:
            people_undetected += 1
            
    if reporting is True:    
        # Display results for users interpretation
        print('Number of infected people detected at departure boarder: ', 
              people_detected_departure)
        print('Number of infected people detected at UK boarder: ', 
              people_detected_arrival)
        if self_isolation:
            print('Number of infected people detected after second testing: ', 
                  people_detected_secondtest)
            print('Number of symptomatic people detected prior to release: ', 
                  people_detected_release)
        print('Number of infected people passing through UK boarder: ', 
              people_undetected)
    
    # Total number of infected people who manage to travel to UK boarder
    travel_total = num_people - people_detected_departure
    # Ratio of infected people detected by screening
    detected_ratio = (people_detected_arrival + people_detected_release +
                      people_detected_secondtest) / travel_total
    
    # If users specifies for full output, all population counts are returned
    if full_output:
        return [
                people_detected_departure, people_detected_arrival,
                people_detected_secondtest, people_detected_release,
                people_undetected, detected_ratio
                ]
    # Else, simply return detection ratio
    else:
        return detected_ratio
      