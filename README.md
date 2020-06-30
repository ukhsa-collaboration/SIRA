# SIRA
# Simulated Importation Risk Assessment
----

This package was borne from work undertaken at Public Health England's Emergency Response Department. This package makes use of Monte Carlo simulation to quantify the effectiveness of contingencies that aim to reduce the risk of importation of diseases assumed to have broken out in some foreign country.

----

## Requirements

This package depends on the following packages:

`SciPy >= 1.4.1`
`NumPy >= 1.18.1`

----

## Model Description

In particular, the code contained within this package was put together to help assess the effectiveness of border screening as a means of reducing the risk of importation during times of international disease outbreak.

The idea of implementing border screening to reduce importation risk has long been held in contention and much literature exists arguing this case for specific diseases/outbreaks (influenza and the 2003 SARS outbreak most prominently). This code was then put together to address the general case; allowing the user to model the border screening process for infected travellers originating from some country assumed to be affected by an outbreak of some arbitrary disease (requiring only a probability distribution for the incubation period to be known).

The model then required two other arguments (with supporting parameters), describing the distributions for flight times from the country of traveller origin to the destination country, as well as some other distribution that describes when (prior to boarding the flight) the travellers were most likely to have been infected (this is typically assumed to be uniformly distributed from some sensibly chosen number of hours prior, to the point of boarding).

The model then makes use of Monte Carlo simulation to imitate a number of travellers becoming infected sometime prior to boarding a flight, and then attempting to cross the border into the destination country. Each traveller, when initiated, is assigned a time of infection (prior to boarding), flight time, and incubation period distributed according to the inputted distributions. Each traveller is then progresses through the model according to the following algorithm:

- If the traveller has become symptomatic prior to the flight, they do not fly and exit the model, recorded as a NON FLIER
- If the traveller manages to board the plane, but becomes symptomatic during the flight they are detected at the destination border and exit the model, being recorded recorded as a BORDER DETECTION
- Else, it is assumed that the travellers incubation period has exceeded the time from becoming infected, to travelling to the destination country and crossing the border. They exit the model being recorded as a BORDER NONDETECTED

The ratio of travellers being detected at the border, against the number of travellers successfully boarding their flight then measures the success rate of the implemented border screening.

A scientific article which fully explores the theory behind this method is currently in the process of being produced and publish. A linked will be included when this is complete.

----

## Version 1.1.0

This version builds upon the previous release to meet the newly identified needs of Public Health England's modellers. In particular, this version now allows the user to:

- Specify a probability that the infected individuals modelled may be asymptomatic. This is specified using the parameter `asymp_prob`.
- Specify two additional times, at the first of which an additional test may be administered, and at the second, those deemed to by undetected and symptom free may be released. These are specified using the parameters `second_screen` and `release_time`.

These additional features are of course optional, and leaving them unspecified will revert the model to run as previously described.

The introduction of asymptomatic travellers only impacts the behaviour of the model in latter stages when second testing is being enforced. Modelled asymptomatic individuals behave the same as their symptomatic counterparts, with the exception that instead of their incubation period describing how long until that person displays symptoms, it describes only how long until this person is detectable through testing. In the case of symptomatic cases, these times are assumed to coincide. Though subtle, this can make some difference; we explore this more below.

The primary purpose of these additions, is that this model now allows the user to incorporate a period of isolation after arrival. Thus, by the terminology above, this model can now incorporate the requiring of all those who would have been recorded as a BORDER NONDETECTED, undergo a period of self-isolation before being re-assessed and (if well enough) released into the destination country. As stated above, the second test (if defined) will be administered `second_screen` (value to be given in hours) after arrival into the destination country. If the traveller is symptomatic or detectable (if modelled individual is determined to be asymptomatic) by this second test, they are recorded as such and exit the model much as before. However, if the user so chooses, they may also specify `release_time` (value to be given in hours). If given, this value is to be larger or equal to `second_screen`, and is used to represent the time that can be required for results of testing to come back. In this period though, some cases may develop symptoms even though the test they just gave with come back negative (i.e. the incubation period falls somewhere between `second_screen` and `release_time`), and being under observation in self-isolation, we then also record these as detections. But for those who have been deemed asymptomatic, if the test they provide is to come back negative and their "incubation period" (time till detectable) is reached before `release_time`, due to their nature of not displaying detectable symptoms (except to testing), they are released and recorded as UNDETECTED. Else, if the infected individuals incubation period or time until detectable exceeds the time from infection until release time, these also go undetected and are recorded as such.   

