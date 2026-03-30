# Problem Context and Definitions

## Rural vs. Urban/suburban

The HSM has three different chapters depending on the characteristics of the road segment/site being analyzed. 

- Chapter 10: Rural two-lane, two-way roads
- Chapter 11: Rural multilane highways
- Chapter 12: Urban and suburban arterials

When deciding between rural vs urban/suburban we look at the population of the area. The following is from the HSM. 

> In the HSM, the definition of "urban" and "rural" areas is based on Federal Highway Administration guidelines which classify urban areas as places inside urban boundaries where the population is greater than 5,000 persons. 

Rural is for areas with less than that population. Granby has a population of approximately 2000 and so meets the **rural classification**. 

This would imply that we would use either chapters 10 or 11. However, chapter 10 does not support roads with 4 or more lanes. Though chapter 11 is about rural multilane highways, the term is used interchangeably with multilane roads and as such is the best fit for this project. 

**However**, a key limitation of chapter 11 is that there is no pedestrian accident quantification available. So, despite it being more appropriate for the context of Granby we will be using chapter 12 for that portion of the writeup. Some chapter 11 results will be cataloged for documentation purposes and for the sake of comparison. 

---

## Other Key Facts

- Agate avenue is a 5 lane road. It has 4 proper lanes with a 5th center turning lane, also known as a **Two Way Left Turn Lane (TWLTL)**.

- The intersection at Agate and Mesa is a 3 leg intersection with stop control on the minor road (Mesa). As such, it is a **3ST** intersection. 

- The intersection at Agate and 4th is a 4 leg intersection with stop control on the minor road (4th). As such, it is a **4ST** intersection. 

- The **Annual Average Daily Traffic (AADT)** of the relevant road segment of Agate avenue is 11,000 vehicles per day. This will function as the **Major AADT** for both key intersections. 

- The intersections of interest for this project are: 
    - **Mesa and Agate** 
    - **4th and Agate**

These intersections are not immediately next to each other and as such we can not assume their traffic calming measures will impact each other. This is more evident due to the traffic signal already installed on **1st and Agate** that lies between them. 

---

# Approximating Intersection Minor AADT

As Minor AADT in Granby is not publicly available we must make certain assumptions to approximate it. We have observed peak hourly traffic volumes. We can calculate the proportion of minor vs major volume using those observed counts and assume that same proportion carries over to AADT. 

$$
\text{AADT}_{\text{minor}} \propto \text{AADT}_{\text{major}} \cdot \frac{\text{Observed minor volume}}{\text{Observed major volume}}
$$

---

## Observed Traffic Volumes

Page 13 of the Agate signal warrant provides the following peak hour volumes for the baseline 2025 scenario:

| Street | Major veh/h | Minor veh/h | Minor/Major |
| ------ | ----------- | ----------- | ----------- |
| 4th St | 1131        | 86          | 0.076       |
| 6th St | 980         | 163         | 0.164       |

---

## Approximating Minor AADT for 4th

For 4th Street, the minor street peak hour volume is approximately 7.6% of the major street volume. Assuming this proportion carries over to daily volumes, we approximate:

$$
\text{AADT}_{\text{minor}} \approx 11000 \cdot 0.076 = 836
$$

---

## Approximating Minor AADT for Mesa

This approximation is more uncertain for Mesa, as observed traffic volumes were not provided for this intersection. In the absence of better data, I assume that the relationship between minor and major traffic volumes at Mesa is similar to those observed at 4th and 6th Streets.

This is a strong and potentially limiting assumption. However, given the available data, this serves as a rough, first-pass estimate to document the analysis process.

Let $p_m$, $p_4$, and $p_6$ denote the minor-to-major proportions for Mesa, 4th, and 6th Streets, respectively. I approximate $p_m$ using the average of the observed proportions:

$$
p_m \approx \frac{p_4 + p_6}{2} = \frac{0.076 + 0.164}{2} = 0.12
$$

To reflect uncertainty, I estimate the variability using the sample standard deviation of the two observed proportions:

$$
\sigma_{p_m} \approx 0.062
$$

This yields an approximate range for $p_m$:

$$
p_m \approx 0.12 \pm 0.062
$$

$$
p_m \in [0.058, 0.182]
$$

This range is wide, reflecting both the small sample size (only two intersections) and the simplifying assumptions used. Any downstream estimates based on this value should therefore be interpreted cautiously.

From this, we can calculate a range for the minor AADT for Mesa as follows:

$$
\text{AADT}_{\text{minor}} \approx 11000 \cdot p_m \\
\mu = 11000 \cdot 0.12 = 1320 \\
\text{lower} = 11000 \cdot 0.058 \approx 638 \\
\text{upper} = 11000 \cdot 0.182 \approx 2002
$$

So we have a mean of 1320 veh/day and a final range of:

$$
\text{AADT}_{\text{minor}} \in [638, 2002]
$$

---

# Approximating Daily Pedestrian Volume

The Mesa and Agate memo provided by SGM details a set of instructions for converting observed hourly pedestrian volumes into annual and daily volumes. The details on this calculation can be found in `docs/notes/approximating-pedestrian-volumes.md`. 

## 4th Street

Using the observed pedestrian volumes provided on page 15 of the Agate Signal Warrant gives us the following data.

|Interval|Volume (pph)|
|---|---|
|2/19/2025 15:45|7|
|2/19/2025 14:00|6|
|2/19/2025 13:00|3|
|2/19/2025 11:45|2|

Using the top row of 7 people per hour for the calculation gives us an estimated daily pedestrian volume of 145.32 people per day. 

## Mesa

|Peak duration|Total pedestrians|PPH|Start time|
|---|---|---|---|
|1-hour|6|6|2/19/2025 16:00|
|2-hour|6|3|2/19/2025 14:45|
|3-hour|7|2.3|2/19/2025 13:30|

The same methodology results in an estimated daily pedestrian volume of 138.4 people per day. 

---

# Using the HSM Excel Sheet

For the sake of simplicity, we will use the Excel sheet tools provided by HSM. They can be found [here](https://www.highwaysafetymanual.org/Pages/tools.aspx). All calculations have direct citations for formulas and tables found in the HSM, so manual calculations can be done if there is interest. 

In these sheets, we provide a set of values that we have documented and the results are automatically calculated according to HSM guidelines. 

Only one sheet will be used for this analysis. 

- The **urban and suburban arterials** sheet as it gives pedestrian accident estimates.
- The **rural multilane highways** sheet is more appropriate for the characteristics of granby but does not give us the pedestrian values we are interested in and so **will not be used** in this analysis.

# Results - 4th & Agate

## Baseline Results (no traffic signal)

First, the input parameters.

|Parameter|Value|
|---|---|
|Intersection Type|4ST|
|Calibration Factor|1|
|AADT major|11,000|
|AADT minor|836|
|Major roads with left turn lanes|0|
|Major roads with right turn lanes|0|
|Intersection lighting (not a signal)|Present|


|Metric|Value (Incidents per year)|
|---|---|
|$N_{biMV}$ (Total)|1.38|
|$N_{biSV}$ (Total)|0.214|
|$N_{pedi}$ (Total)|0.035|

Here we have a predicted vehicle/pedestrian incident rate of 0.035 incidents per year. Or, one pedestrian related incident per 28.57 years. This value is a flat proportion of the total incidents (single or multi vehicle). That proportion being $0.022$. $(1.38 + 0.214) * 0.022 \approx 0.035$. 

This value does not take into account any pedestrian values or the road configuration such as the number of lanes. Unfortunately this is due to the limitations to stop-controlled models in the HSM. 

## Applying Traffic Signal CMF

What we can do however is manually apply a relevant Crash Modification Factor for installing a traffic signal. The one used can be found [here](https://cmfclearinghouse.fhwa.dot.gov/detail.php?facid=319). It has a mean of 0.77 and a standard error of 0.22. So a range of 0.55 to 0.99. 

From the excel sheet, the current combined CMF is 0.91. We can multiply this value by the traffic signal CMF to get a new combined CMF. Our results update as such:

|Index $r_i$|Metric|Old Value|New Values (low, mean, high)|
|---|---|---|---|
|$r_1$|Combined CMF|0.91|0.5005, 0.7007, 0.9009|
|$r_2$|$N_{biMV}$ (Total)|1.38|0.69, 0.97, 1.24|
|$r_3$|$N_{biSV}$ (Total)|0.214|0.11, 0.15, 0.19|
|$r_4$|$N_{biALL} (r_2 + r_3)$|1.594|0.80, 1.12, 1.44|
|$r_5$|$N_{pedi}$ $(r_4 \cdot 0.022)$|0.035|0.018, 0.025, 0.032|
|$r_6$|Years per accident ($1/r_5$)|28.57|31.65, 40.70, 56.98|

So, simply applying the traffic signal CMF to our previous results gives us an estimation of one pedestrian accident every 31 to 57 years, a noticably wide range. On average, we expect an accident every 40 years. 

## Using 4SG Intersection Type in Excel Sheet

As an alternative estimation we can change the intersection type in the excel sheet. Previously we had it set to 4ST which is a 4 way stop controlled intersection. We can instead use 4SG which is a 4 way intersection with signal control. The upside to this methodology is that we now have access to the pedestrian SPFs that exist for this type of intersection. We can input new parameters such as pedestrian volume, max number of road lanes, and the existence of a nearby school.

The downside is we have no justifiable "before" pedestrian crash frequency as our "before" scenario cannot use these SPFs. These results are stil of value relative to the prior sections findings but they cannot be directly compared.

|Parameter|Value|
|---|---|
|Intersection Type|4SG|
|Calibration Factor|1|
|AADT major|11,000|
|AADT minor|836|
|Intersection lighting (not a signal)|Present|
|Type of left-turn signal phasing for Leg #1|N/A|
|Type of left-turn signal phasing for Leg #2|N/A|
|Type of left-turn signal phasing for Leg #3|N/A|
|Type of left-turn signal phasing for Leg #4 (if applicable)|N/A||
|Sum of all pedestrian crossing volumes  (PedVol) -- Signalized intersections only|145.32|
|Maximum number of lanes crossed by a pedestrian (nlanesx)|5|
|Schools within 300 m (1,000 ft) of the intersection (present/not present)|Present|

Below are the reported values from the sheet. I will report pedestrian values both with and without the school parameter, as it is technically far enough away from this intersection to not apply. 

|Metric|Values|
|---|---|
|$N_{biMV}$ (Total)|1.508|
|$N_{biSV}$ (Total)|0.114|
|$N_{pedi}$ (With school CMF)|0.025|
|$N_{pedi}$ (Without school CMF)|0.018|
|Years per pedestrian accident (school present)|40|
|Years per pedestrian accident (school not present)|55.56|

What we can see here is this output roughly matches our range of values from the previous section. Of course it is difficult to draw meaningful conclusions from these results due to the lack of values without a traffic signal. 

# Results - Mesa & Agate

This section has an additional layer of complexity on it as the minor road AADT has a degree of uncertainty attached to it. In the parameter table, I will be using the 

|Parameter|Values|
|---|---|
|Intersection Type|3ST|
|Calibration Factor|1|
|AADT major|11,000|
|AADT minor|638, 1320, 2002|
|Major roads with left turn lanes|0|
|Major roads with right turn lanes|0|
|Intersection lighting (not a signal)|Present|

We will use a similar approach to the last section, first getting the baseline pedestrian crash rates then applying the relevant CMF. The only CMF applied here is for the intersection lighting, giving us a CMF of 0.91. Unadjusted is the value before the cmf is applied. 

|Metric|Values (Incidents per year)|
|---|---|
|$N_{biMV}$ (Total, unadjusted)|0.682, 0.919, 1.090|
|$N_{biMV}$ (Total, adjusted)|0.620, 0.836, 0.991|
|$N_{biSV}$ (Total, unadjusted) |0.132, 0.191, 0.236|
|$N_{biSV}$ (Total, adjusted) |0.120, 0.174, 0.215|
|$N_{pedi}$ (Total)|0.016, 0.021, 0.025|
|Years per pedestrian accident|40.00, 47.62, 62.50|

The baseline pedestrian accident rates for Mesa & Agate indicate an accident expected every 40 to 60 years. This is already very low, and the curb extensions bring it even lower. The only listed CMF for a curb extension (aka a bulbout) is stated to decrease overall accident rates by $37\%$. So we can apply that to the above results. The CMF before the sub extension is at 0.91, so we multiply that by 0.67 to get the new overall CMF of 0.6097.

[CMF Link](https://cmfclearinghouse.fhwa.dot.gov/detail.php?facid=1786)

Note that this CMF has no documented standard deviation, however it is commonly cited in official traffic articles from various states. For this HSM methodology it is the best estimation of crash reduction that we have. 

|Metric|Values (Incidents per year)|
|---|---|
|$N_{biMV}$ (Total, unadjusted)|0.682, 0.919, 1.090|
|$N_{biMV}$ (Total, adjusted)|0.416, 0.560, 0.665|
|$N_{biSV}$ (Total, unadjusted) |0.132, 0.191, 0.236|
|$N_{biSV}$ (Total, adjusted) |0.08, 0.12, 0.14|
|$N_{biALL}$ (Total, unadjusted) |0.81, 1.11, 1.33|
|$N_{biALL}$ (Total, adjusted) |0.50, 0.68, 0.81|
|$N_{pedi}$ (Total)|0.011, 0.015, 0.018|
|Years per pedestrian accident|56.22, 67.16, 91.59|