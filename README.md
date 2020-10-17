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
- If the traveller manages to board the plane, but becomes symptomatic during the flight they are detected at the destination border and exit the model, being recorded as a BORDER DETECTION
- Else, it is assumed that the travellers incubation period has exceeded the time from becoming infected, to travelling to the destination country and crossing the border. They exit the model being recorded as a BORDER NONDETECTED

The ratio of travellers being detected at the border, against the number of travellers successfully boarding their flight then measures the success rate of the implemented border screening.

A scientific article which fully explores the theory behind this method is available at [medRxiv](https://doi.org/10.1101/2020.07.10.20150664).

----

