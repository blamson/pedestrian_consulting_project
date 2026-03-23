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

# Using the HSM Excel Sheet

For the sake of simplicity, we will use the Excel sheet tools provided by HSM. They can be found [here](https://www.highwaysafetymanual.org/Pages/tools.aspx). All calculations have direct citations for formulas and tables found in the HSM, so manual calculations can be done if there is interest. 

In these sheets, we provide a set of values that we have documented and the results are automatically calculated according to HSM guidelines. 

Two sheets will be used for this analysis. 

- The **urban and suburban arterials** sheet as it gives pedestrian accident estimates.
- The **rural multilane highways** sheet as it is more appropriate given the characteristics of Granby.

## Results

- Npedi: Number of pedestrian incidents
- 