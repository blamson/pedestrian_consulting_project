# Overview

This file is notes for chapters 10 and 12 from the highway safety manual. These chapters cover the predictive methods used for estimating crash rates. 

# Part C - Introduction

> The predictive method provides a quantitative measure of expected average crash frequency under both existing conditions and conditions which have not yet occurred. This allows proposed roadway conditions to be quantitatively assessed along with other considerations such as community needs, capacity, delay, cost, right-of-way, and environmental considerations.

These methods can be used for evaluating and comparing the expected average crash frequency of situations such as:

- Existing facilities under past or future traffic volumes
- Alternative designs for an existing facility under past or future traffic volumes
- Designs for a new facility under past or future traffic volumes
- The estimated effectiveness of countermeasures after a period of implementation
- The estimated effectiveness of proposed countermeasures on an existing facility (prior to implementation)

That final bullet is our exact use case. 

## Warnings

The observed crash frequency (per year) will fluctuate randomly over any period and, therefore, using averages based on short-term periods (eg 1-3 years) may give misleading estimates and create problems associated with regression-to-the-mean bias (RTM). 

## Chapter breakdown

- Chapter 10: Rural two-lane, two-way roads
- Chapter 11: Rural multilane highways
- Chapter 12: Urban and suburban arterials

Chapter 10 includes three- and four-leg intersections with minor-road stop control and four-leg signalized intersections on all the roadway cross-sections to which the chapter applies.

## SPF General Notes

Estimatating crash frequency uses regression models developed from data for a number of similar sites. As such these models are designed with specific baseline conditions and site types in mid. SPFs are typically fairly simple functions, taking variables like AADT into account primarily. 

CMFs are used to adjust this output based on site conditions that deviate from the baseline. Example, an SPF may have a roadway segment of 10ft and the roadway being analyzed may be wider or shorter. 

## SPF Distribution

> SPF models in HSM are based on the **negative binomial distribution**, which are are better suited to modeling the high natural variability of crash data than traditional modeling techniques, which are based on the normal distribution.

This is an extension of the **Poisson** distribution commonly used for counting. The issue with the Poisson distribution is that the mean and variance are equal, which isn't a desirable property for this kind of estimation. Often in this line of work the variance exceeds the mean. The negative binomial has an additional parameter that controls dispersion. 

## SPF Requirements

To apply an SPF, the following information is necessary:

- Basic geometric design and geographic information of the site to determine the facility type and whether an SPF is available for said site.
- AADT information for estimation of past periods, or forecast estimates of AADT for estimation of future periods
- Detailed geometric design of the site and base conditions to determine whether the site conditions vary from the base conditions and therefore a CMF is applicable. 

## Rural vs Urban

> In the HSM, the definition of "urban" and "rural" areas is based on Federal Highway Administration guidelines which classify urban areas as places inside urban boundaries where the population is greater than 5,000 persons. 

Rural is for areas with less than that population. Granby has a population of approximately 2000 and so meets the rural classification. 

# Chapter 10 - Predictive Methods Rural

The predictive methods in CH 10 are specifically for rural two-lane, two-way highway facilities. Facilities with four or more lanes are not covered in chapter 10. As such, this chapter will be skipped as it does not apply to our project.

# Chapter 11 - Rural Multilane Highways

> Chapter 11 applies to rural multilane highway facilities. The term “multilane” refers to facilities with four through lanes.

Though highway is in the title, it is used interchangeably with road. 

> The terms “highway” and “road” are used interchangeably in this chapter and apply to all rural multilane facilities independent of official state or local highway designation.

We are concerned with the 4ST site type. 4ST means four-leg intersection with stop control. An intersection of a rural multilane highway/road and two minor roads. Stop signs are on both minor-road approaches. 

SPFs needed: Equation 11-11, Table 11-7. 

### 11.6.3 SPFs for Intersections

Baseline conditions for 4ST:

Intersection skew-angle: 0 degrees
Intersection left-turn lanes: 0, except on stop-controlled approaches
Intersection right-turn lanes: 0, except on stop-controlled approaches
Lighting: None

Equation:

$$
N_{\text{spf int}} = \exp[a + b \cdot \ln(AADT_{\text{maj}}) + c \cdot \ln(AADT_{\text{min}})]
$$

Where:

$N_{\text{spf int}} = $ SPF estimate of intersection-related expected average crash frequency for base conditions.

$AADT_{\text{maj}} = $ AADT for major-road approaches

$AADT_{\text{min}} = $ AADT for minor-road approaches

$a, b, c = $ Regression coefficients