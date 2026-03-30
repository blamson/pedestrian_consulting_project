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

## Approximating Minor AADT for Mesa

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

This yields:

$$
p_m \approx 0.12 \pm 0.062
$$

$$
p_m \in [0.058, 0.182]
$$

This implies a coefficient of variation of roughly 50%, indicating substantial uncertainty. Downstream estimates should therefore be interpreted as order-of-magnitude approximations.

From this:

$$
\text{AADT}_{\text{minor}} \approx 11000 \cdot p_m
$$

$$
\mu = 1320,\quad \text{lower} \approx 638,\quad \text{upper} \approx 2002
$$

So:

$$
\text{AADT}_{\text{minor}} \in [638, 2002]
$$

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

## Baseline Results (No Traffic Signal)

| Parameter                         | Value   |
| --------------------------------- | ------- |
| Intersection Type                 | 4ST     |
| Calibration Factor                | 1       |
| AADT major                        | 11,000  |
| AADT minor                        | 836     |
| Major roads with left turn lanes  | 0       |
| Major roads with right turn lanes | 0       |
| Intersection lighting             | Present |

| Metric     | Value (Incidents/year) |
| ---------- | ---------------------- |
| $N_{biMV}$ | 1.38                   |
| $N_{biSV}$ | 0.214                  |
| $N_{pedi}$ | 0.035                  |

This corresponds to approximately one pedestrian-related crash every **28.6 years**.

For stop-controlled intersections, the HSM estimates pedestrian crashes as a fixed proportion (~2.2%) of total crashes. As a result, this estimate does **not** depend on pedestrian volume or crossing characteristics, which is a significant limitation.

---

## Applying Traffic Signal CMF

A traffic signal CMF (mean = 0.77, range ≈ 0.55–0.99) is applied multiplicatively to the existing combined CMF, consistent with HSM methodology.

Traffic signal CMF Link - [CMID 319](https://cmfclearinghouse.fhwa.dot.gov/detail.php?facid=319)

| Metric             | Old   | New (low, mean, high)  |
| ------------------ | ----- | ---------------------- |
| Combined CMF       | 0.91  | 0.5005, 0.7007, 0.9009 |
| $N_{biMV}$         | 1.38  | 0.69, 0.97, 1.24       |
| $N_{biSV}$         | 0.214 | 0.11, 0.15, 0.19       |
| $N_{biALL}$        | 1.594 | 0.80, 1.12, 1.44       |
| $N_{pedi}$         | 0.035 | 0.018, 0.025, 0.032    |
| Years per accident | 28.57 | 31.65, 40.70, 56.98    |

This yields an estimated range of **one pedestrian crash every 31–57 years**, with a mean of ~40 years.

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

This analysis includes uncertainty in minor-road AADT:

| Parameter         | Values          |
| ----------------- | --------------- |
| Intersection Type | 3ST             |
| AADT major        | 11,000          |
| AADT minor        | 638, 1320, 2002 |
| Lighting          | Present         |

| Metric           | Values (Incidents/year) |
| ---------------- | ----------------------- |
| $N_{biMV}$ (adj) | 0.620, 0.836, 0.991     |
| $N_{biSV}$ (adj) | 0.120, 0.174, 0.215     |
| $N_{pedi}$       | 0.016, 0.021, 0.025     |
| Years per crash  | 40.00, 47.62, 62.50     |

Baseline estimates suggest one pedestrian crash every **40–60 years**.

---

## Applying Curb Extension CMF

A curb extension (bulb-out) CMF of 0.67 is applied multiplicatively to the existing lighting-adjusted CMF (0.91), yielding a combined CMF of 0.6097.

Curb Extension CMF Link - [CMID 1786](https://cmfclearinghouse.fhwa.dot.gov/detail.php?facid=1786)

| Metric           | Values (Incidents/year) |
| ---------------- | ----------------------- |
| $N_{biMV}$ (adj) | 0.416, 0.560, 0.665     |
| $N_{biSV}$ (adj) | 0.08, 0.12, 0.14        |
| $N_{biALL}$      | 0.50, 0.68, 0.81        |
| $N_{pedi}$       | 0.011, 0.015, 0.018     |
| Years per crash  | 56.22, 67.16, 91.59     |

With the curb extension, the expected frequency is approximately **one pedestrian crash every ~67 years**, with a range extending beyond 90 years.

---

# Final Interpretation

The installation of a traffic signal at 4th & Agate and a curb extension at Mesa & Agate both result in reductions in estimated pedestrian crash frequency under the HSM framework. 

At 4th & Agate, the addition of a traffic signal reduces the expected pedestrian crash frequency from approximately once every 29 years to a range of 31 to 57 years, with a mean of over 40 years. An alternate model that checks the pedestrian crash frequency of a signalized intersection (4SG) produced similar estimates, suggesting that the magnitude in reduction is consistent despite the varying methodologies. 

At Mesa & Agate, the addition of a curb extension reduces the expected crash frequency from approximately once every 40-60 years to once every 56-92 years. The average shifts from 47 to 67, an increase of 20 years. Though this result is promising, it is limited by the lack of data on traffic volume at the intersection. 

Though both locations show a similar decrease in crash frequency of around 20-30%, the order of magnitude does not change between either scenario. The pedestrian crash frequency is extremely low in both cases before any measures have been taken. This does not mean that these measures are unnecessary as they further ensure the safety of Granby residents, though it does require a certain shift in interpretation. 

These results are also limited by the methodology used in the HSM and the data provided. A lot of precision is lost in this analysis due to lack of provided uncertainty in many of the metrics used, such as the major road AADT. On top of that, the HSM is heavily lacking in pedestrian focused models, forcing a reliance on very basic proportional estimates. It is very possible that a more sophisticated approach would produce very different results. 

In conclusion, both the traffic signal and curb extensions show promise in improving pedestrian safety, but this is within the context of an area that is already fairly low in risk and coming from results stemming from severe modeling limitations. 