# Problem Context and Definitions

## Rural vs. Urban/Suburban

The HSM has three different chapters depending on the characteristics of the road segment/site being analyzed:

* Chapter 10: Rural two-lane, two-way roads
* Chapter 11: Rural multilane highways
* Chapter 12: Urban and suburban arterials

When deciding between rural vs. urban/suburban, we look at the population of the area. The following is from the HSM:

> In the HSM, the definition of "urban" and "rural" areas is based on Federal Highway Administration guidelines which classify urban areas as places inside urban boundaries where the population is greater than 5,000 persons.

Rural areas are those with populations below this threshold. Granby has a population of approximately 2,000 and therefore meets the **rural classification**.

This would imply that we should use either Chapter 10 or 11. However, Chapter 10 does not support roads with four or more lanes. While Chapter 11 is described as covering rural multilane highways, the term is used broadly and is the closest match for this project context.

**However**, a key limitation of Chapter 11 is that it does not provide pedestrian crash estimation. As a result, despite being less appropriate contextually, Chapter 12 will be used for pedestrian-related analysis. Selected Chapter 11 results will still be documented for comparison.

---

## Other Key Facts

* Agate Avenue is a 5-lane road, consisting of four through lanes and a center two-way left-turn lane (**TWLTL**).

* The intersection at Agate and Mesa is a three-leg intersection with stop control on the minor road (Mesa), classified as a **3ST** intersection.

* The intersection at Agate and 4th is a four-leg intersection with stop control on the minor road (4th), classified as a **4ST** intersection.

* The **Annual Average Daily Traffic (AADT)** on the relevant segment of Agate Avenue is 11,000 vehicles per day. This serves as the **major AADT** for both intersections.

* The intersections of interest are:

  * **Mesa and Agate**
  * **4th and Agate**

These intersections are sufficiently separated such that their traffic control measures are unlikely to interact. This is further supported by the presence of a traffic signal at **1st and Agate** between them.

---

# Approximating Intersection Minor AADT

Minor-road AADT is not publicly available for Granby, so it must be approximated. Observed peak-hour traffic volumes are used to estimate the proportion of minor-to-major traffic, assuming this proportion is representative of daily volumes.

$$
\text{AADT}_{\text{minor}} \approx \text{AADT}_{\text{major}} \cdot
\frac{\text{Observed minor volume}}{\text{Observed major volume}}
$$

This assumes that peak-hour traffic proportions are representative of overall daily traffic patterns.

---

## Observed Traffic Volumes

Page 13 of the Agate signal warrant provides the following peak-hour volumes for the baseline 2025 scenario:

| Street | Major veh/h | Minor veh/h | Minor/Major |
| ------ | ----------- | ----------- | ----------- |
| 4th St | 1131        | 86          | 0.076       |
| 6th St | 980         | 163         | 0.164       |

---

## Approximating Minor AADT for 4th

For 4th Street, the minor street peak-hour volume is approximately 7.6% of the major street volume. Assuming this proportion carries over to daily volumes:

$$
\text{AADT}_{\text{minor}} \approx 11000 \cdot 0.076 = 836
$$

---

## Approximating Minor AADT for Mesa - Approach 1

This approximation is more uncertain for Mesa, as observed traffic volumes were not provided. In the absence of better data, it is assumed that the relationship between minor and major traffic volumes at Mesa is similar to those observed at 4th and 6th Streets.

This introduces substantial uncertainty, but provides a reasonable first-order approximation given available data.

Let $p_m$, $p_4$, and $p_6$ denote the minor-to-major proportions for Mesa, 4th, and 6th Streets, respectively. Approximate $p_m$ using the average of the observed proportions:

$$
p_m \approx \frac{p_4 + p_6}{2} = \frac{0.076 + 0.164}{2} = 0.12
$$

Estimate variability using the sample standard deviation:

$$
\sigma_{p_m} \approx 0.062
$$

With this we have a mean and a standard deviation. It's a tiny sample size of 2 but it's something. With this we can do some monte carlo sampling to get a rough range on the proportion values. We want a random variable that is bounded by the properties of minor aadt. Minor AADT is, by definition, smaller than the major AADT so will be bounded between 0 and 1. Ideally we'd use the Beta distribution but I'm low on time. I'll use the normal distribution and accept than it allows for the entire real line as output for now. 

Taking the summary output of 100,000 random variables from $N(0.12, 0.062^2)$ gives us the approximated distribution of $p_m$:

|min|1st quartile|median|mean|3rd quartile|max|
|---|---|---|---|---|---|
|-0.161|0.078|0.120|0.121|0.162|0.392|

We'll take the 1st and 3rd quartiles from this as the proportions we'll test. Of course the full range is extremely large, due in part to the obvious lack of certainty 2 measurements gives us. However, we can still use this to get a range of AADT for testing. 

$$
\text{AADT}_{\text{minor}} \approx 11000 \cdot p_m
$$

$$
\mu = 1321, \quad \text{Lower} \approx 861,\quad \text{Upper} \approx 1781
$$

$$
\text{AADT}_{\text{minor}} \in [861, 1781]
$$

## Approximating Minor AADT for Mesa - Approach 2

This approach is similar to the above, but instead of using the average of 4th and 6th it just creates a range out of the proportions of those intersections. 

So this method just tests two values, 0.076 and 0.166, providing AADT estimates of 836 and 1826 respectively. 

---

# Approximating Daily Pedestrian Volume

The Mesa and Agate memo provided by SGM outlines a method for converting observed hourly pedestrian volumes into daily estimates. Details are documented in `docs/notes/approximating-pedestrian-volumes.md`.

## 4th Street

Using observed pedestrian volumes (page 15 of the signal warrant):

| Interval        | Volume (pph) |
| --------------- | ------------ |
| 2/19/2025 15:45 | 7            |
| 2/19/2025 14:00 | 6            |
| 2/19/2025 13:00 | 3            |
| 2/19/2025 11:45 | 2            |

Using the peak value of 7 pph yields an estimated daily pedestrian volume of **145.32 pedestrians/day**.

## Mesa

| Peak duration | Total pedestrians | PPH | Start time      |
| ------------- | ----------------- | --- | --------------- |
| 1-hour        | 6                 | 6   | 2/19/2025 16:00 |
| 2-hour        | 6                 | 3   | 2/19/2025 14:45 |
| 3-hour        | 7                 | 2.3 | 2/19/2025 13:30 |

Applying the same method yields **138.4 pedestrians/day**.

---

# Using the HSM Excel Sheet

For simplicity, the HSM Excel tools are used ([link](https://www.highwaysafetymanual.org/Pages/tools.aspx)). These implement HSM SPFs and CMFs directly.

Only one sheet is used:

* The **Urban/Suburban Arterials** sheet (for pedestrian crash estimation)

The **Rural Multilane Highways** sheet is more contextually appropriate but does not include pedestrian models and is therefore not used for primary results.

---

# Results – 4th & Agate

To account for ambiguity in how the center lane on Agate is represented, two alternative modeling approaches are evaluated:

- Dedicated turn lane CMFs (HSM default)
- Two-way left-turn lane (TWLTL) CMF

These scenarios represent **mutually exclusive assumptions** and should not be applied simultaneously.

---

## Dedicated Turn Lane Scenario (HSM Default)

### Baseline (No Traffic Signal)

| Parameter                         | Value   |
|----------------------------------|--------|
| Intersection Type                | 4ST     |
| Calibration Factor               | 1       |
| AADT (major / minor)            | 11,000 / 836 |
| Left turn lanes (major)         | 1       |
| Right turn lanes (major)        | 1       |
| Lighting                        | Present |

| Metric            | Value (Incidents/year) |
|-------------------|------------------------|
| Combined CMF      | 0.57                   |
| $N_{biMV}$        | 0.866                  |
| $N_{biSV}$        | 0.134                  |
| $N_{pedi}$        | 0.022                  |
| Ped years/accident| 45.45                  |

This corresponds to approximately **1 pedestrian crash every 45.45 years**.

**Limitation:** For stop-controlled intersections, pedestrian crashes are modeled as a fixed proportion (~2.2%) of total crashes and do not reflect pedestrian exposure.

---

### With Traffic Signal and Traffic Diversion

A traffic signal CMF (0.77) is applied multiplicatively ([CMID 319](https://cmfclearinghouse.fhwa.dot.gov/detail.php?facid=319)).

Additionally, the minor AADT is updated to reflect the new proportion expected after the road diversion is implemented. 

| Metric            | Baseline | Signalized |
|-------------------|----------|------------|
| Combined CMF      | 0.577    | 0.44       |
| $N_{biALL}$       | 1.000    | 0.7757      |
| $N_{pedi}$        | 0.022    | 0.017      |
| Ped years/accident| 45.45    | 58.82      |
|Probability of accident in 10 years| 19.75%| 15.3%|


---

## TWLTL Scenario

### Baseline (No Traffic Signal)

| Parameter                         | Value   |
|----------------------------------|--------|
| Intersection Type                | 4ST     |
| Calibration Factor               | 1       |
| AADT (major / minor)            | 11,000 / 836 |
| Turn lanes (major)              | None    |
| TWLTL                           | Present |
| Lighting                        | Present |

| Metric            | Value (Incidents/year) |
|-------------------|------------------------|
| Combined CMF      | 0.837                  |
| $N_{biMV}$        | 1.269                  |
| $N_{biSV}$        | 0.197                  |
| $N_{pedi}$        | 0.032                  |
| Ped years/accident| 31.25                  |

This corresponds to approximately **1 pedestrian crash every 31.25 years**.

**Limitation:** Same as above — pedestrian crashes are modeled as a fixed proportion of total crashes.

---

### With Traffic Signal and Diversion

Applying the traffic signal CMF (0.77):

| Metric            | Baseline | Signalized |
|-------------------|----------|------------|
| Combined CMF      | 0.837    | 0.65       |
| $N_{biALL}$       | 1.466    | 1.270      |
| $N_{pedi}$        | 0.032    | 0.028      |
| Ped years/accident| 31.25    | 35.71      |
|Probability of accident in 10 years| 27.39%| 24.42%|

---

## Comparison Summary

| Scenario                  | Ped Years/Accident (Baseline) | Ped Years/Accident (Signalized and Diverted) |
|---------------------------|-------------------------------|----------------------------------|
| Dedicated Turn Lanes      | 45.45                         | 58.82                            |
| TWLTL                     | 31.25                         | 40.00                            |

| Scenario                  | Prob accident in 10 years (Baseline) | Prob accident in 10 years (Signalized and Diverted) |
|---------------------------|-------------------------------|----------------------------------|
| Dedicated Turn Lanes      | 19.75%                         | 15.3%                            |
| TWLTL                     | 27.39%                         | 24.42%                           |

- Modeling choice has large affects baseline risk estimates.
- The traffic signal produces anywhere from a 10-20% reduction in expected pedestrian accidents (driven by the CMF).
- Absolute pedestrian crash frequency remains low, but differences are non-trivial at scale.

---

## Using 4SG Intersection Type

As an alternative, the intersection is modeled as signalized (4SG), enabling use of pedestrian-specific SPFs.

**Important:** These results are not directly comparable to the previous section, as they are derived from different SPFs with different predictor variables.

| Metric                      | Values |
| --------------------------- | ------ |
| $N_{biMV}$                  | 1.508  |
| $N_{biSV}$                  | 0.114  |
| $N_{pedi}$ (school)         | 0.025  |
| $N_{pedi}$ (no school)      | 0.018  |
| Years per crash (school)    | 40     |
| Years per crash (no school) | 55.56  |

These results are broadly consistent with the CMF-adjusted estimates.

---

# Results – Mesa & Agate

## Approach 2: Alternative AADT Approximation Method

As it has a wider range for the sake of my sanity I simply opt to use the outright values from 4th and 6th. The first method is kept and documented for potential future use. 

### Baseline - TWLTL CMF

This analysis includes uncertainty in minor-road AADT:

| Parameter         | Values          |
| ----------------- | --------------- |
| Intersection Type | 3ST             |
| AADT major        | 11,000          |
| AADT minor        | 836, 1826 |
| Lighting          | Present         |

| Metric               | Lower AADT (836) | Upper AADT (1826) |
| -------------------- | ---------------- | ----------------- |
| Combined CMF         | 0.84             | 0.84              |
| $N_{biALL}$          | 0.764            | 1.067             |
| $N_{pedi}$           | 0.016            | 0.022             |
| Ped years/accident   | 62.5             | 45.45             |
| Probability (10 yrs) | 17.79%           | 19.75%            |

---

### Applying Curb Extension CMF

A curb extension (bulb-out) CMF of 0.67 is applied multiplicatively to the existing lighting-adjusted CMF (0.91) and the TWLTL CMF of 0.92, yielding a combined CMF of 0.56.

Curb Extension CMF Link - [CMID 1786](https://cmfclearinghouse.fhwa.dot.gov/detail.php?facid=1786)

| Metric               | Lower AADT (836) | Upper AADT (1826) |
| -------------------- | ---------------- | ----------------- |
| Combined CMF         | 0.56             | 0.56              |
| $N_{biALL}$          | 0.512            | 0.715             |
| $N_{pedi}$           | 0.011            | 0.015             |
| Ped years/accident   | 90.91            | 66.67             |
| Probability (10 yrs) | 10.42%           | 13.93%            |

## Summaary Comparison

| Scenario       | Ped Years/Accident | Probability (10 yrs) |
| -------------- | ------------------ | -------------------- |
| Baseline       | 45.45 – 62.5       | 17.79% – 19.75%      |
| Curb Extension | 66.67 – 90.91      | 10.42% – 13.93%      |


---

# Final Interpretation

# Final Interpretation

The installation of a traffic signal at 4th & Agate and a curb extension at Mesa & Agate both reduce estimated pedestrian crash frequency under the HSM framework.

At 4th & Agate, the signal reduces the expected pedestrian crash rate from approximately **0.022 to 0.017 crashes/year** under the dedicated turn lane assumption, corresponding to an increase in expected time between crashes from **45 to 59 years**. In probabilistic terms, this is a reduction in the probability of at least one pedestrian crash over a 10-year period from **19.75% to 15.3%**. Under the TWLTL assumption, the same intervention reduces the 10-year probability from **27.39% to 24.42%**. Across both modeling choices, the relative reduction is on the order of **10–20%**.

At Mesa & Agate, the curb extension reduces the expected pedestrian crash rate from **0.016–0.022 crashes/year** to **0.011–0.015 crashes/year**, increasing the expected time between crashes from **45–63 years** to **67–91 years**. This corresponds to a reduction in the 10-year probability of a pedestrian crash from **17.79–19.75%** down to **10.42–13.93%**, a **substantially larger relative reduction (≈30–40%)** than observed at 4th.

A key observation is that while the **absolute annual crash rates are low**, the **multi-year probabilities are not negligible**. A ~20% chance of at least one pedestrian crash over a decade at baseline is materially meaningful from a planning perspective. Even after improvements, probabilities remain in the **10–25% range**, depending on location and modeling assumptions.

However, the order of magnitude does not change. Both intersections remain low-frequency environments, and the interventions primarily reduce risk within that same regime rather than shifting it entirely.

These results are constrained by several modeling limitations:

- Pedestrian crashes in stop-controlled models are estimated as a fixed proportion of total crashes, ignoring pedestrian exposure.
- Minor-road AADT at Mesa is highly uncertain and drives a large portion of variability.
- No uncertainty is propagated through CMFs or SPFs.
- The HSM framework is vehicle-centric, with limited pedestrian-specific modeling capability.

Given these constraints, the results should be interpreted as **relative comparisons rather than precise forecasts**.

**Bottom line:**  
Both interventions meaningfully reduce pedestrian risk. The curb extension at Mesa appears to produce a larger proportional reduction, while the signal at 4th provides more modest but still consistent improvements. In both cases, the practical impact is best understood through **multi-year risk (10-year probabilities)** rather than annualized crash rates.