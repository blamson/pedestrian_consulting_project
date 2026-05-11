This section documents the data inputs needed to apply the SPFs and CMFs from the previous sections. Three categories of data are required:

- Traffic volume on the major and minor roads at each intersection
- Pedestrian volume crossing each intersection (used by the 4SG SPF)
- Intersection conditions that determine which CMFs apply and which SPF variant to use

Each subsection below explains where the values came from and how they were derived when not directly available.

## Traffic Volume

The SPFs require **Annual Average Daily Traffic (AADT)** in vehicles per day for both the major road (Agate Avenue) and the minor road (Mesa or 4th).

### Agate Avenue (major road)

Agate AADT is published directly by the Colorado Department of Transportation. CDOT Station 101868, located on US-40 (Agate Avenue) east of Mesa Street in Granby, reports an AADT of **11,000 vehicles per day** (2024). This value is used as $\text{AADT}_{maj}$ for both Mesa & Agate and 4th & Agate.

![CDOT Station 101868 reporting an AADT of 11,000 on Agate Avenue in Granby|600](docs/report_images/agateAADT.png)

### 4th Street and 6th Street (minor roads)

AADT is not published for the minor streets in Granby. The 2025 SGM Signal Warrant Study provides peak-hour traffic counts at the relevant intersections, both before and after the planned 6th Street left-turn diversion. AADT for each minor street is approximated by scaling the Agate AADT by the observed minor-to-major peak-hour ratio:

$$\text{AADT}_{minor} \approx \text{AADT}_{maj} \times \frac{\text{Observed minor volume}}{\text{Observed major volume}}$$

This assumes the peak-hour proportion is representative of the daily proportion. The resulting values:

| Street | Status | Major veh/h | Minor veh/h | Minor/Major | AADT Volume |
| --- | --- | --- | --- | --- | --- |
| 4th St | Before diversion | 1,131 | 86 | 0.076 | 836 |
| 6th St | Before diversion | 980 | 163 | 0.166 | 1,826 |
| 4th St | After diversion | 1,131 | 143 | 0.126 | 1,386 |
| 6th St | After diversion | 1,062 | 34 | 0.032 | 352 |

> Source: Table 6, Agate Ave Signal Warrant Study (SGM, June 2025)

The 4th Street AADT rises from 836 to 1,386 after the diversion, since left-turn traffic from 6th is rerouted through 4th. 6th Street AADT correspondingly drops from 1,826 to 352.

### Mesa Street (minor road)

Mesa Street has no observed traffic counts in either the SGM study or any public dataset. Without direct data, two bounding estimates are used:

- **Lower bound:** 836 vehicles/day (matches 4th Street before diversion)
- **Upper bound:** 1,826 vehicles/day (matches 6th Street before diversion)

These bounds are carried through the analysis as a sensitivity range. The Results section reports outcomes at both bounds.

## Pedestrian Volume

The 4SG SPF requires daily pedestrian volume crossing all legs of the intersection. The SGM Mesa & Agate study and the Signal Warrant Study both provide raw peak-hour pedestrian counts but not daily volumes. A conversion process from the National Bicycle & Pedestrian Documentation Project (NBPD), referenced in the SGM memo, scales hourly peak counts into a daily AADT through a series of seasonal, weekday, and hourly adjustment factors.

Both observations were made on Thursday, February 19, 2025. The February timing means the counts were taken during cold weather with observed snowfall, well below typical pedestrian activity. The NBPD factors account for this through hourly shares (Table 1), daily shares (Table 2), and monthly seasonal shares (Table 3). For the seasonal step, the average of the "Long Winter" and "Moderate Climate" factors is used, consistent with the approach in the SGM memo.

### 4th & Agate

The peak hourly pedestrian count at 4th & Agate is 7, observed during the 15:00 hour. Applying the NBPD conversion:

| Step | Description | Factor | Value |
| --- | --- | --- | --- |
| 0 | Peak hourly count | -- | 7.00 |
| 1 | Overnight adjustment | x1.05 | 7.35 |
| 2 | Hourly to daily | /0.10 (hour share, 15:00, Oct-Mar) | 73.50 |
| 3 | Daily to weekly | /0.12 (Thursday share) | 612.50 |
| 4 | Weekly to monthly | x4.33 (avg weeks/month) | 2,652.13 |
| 5 | Monthly to annual | /0.05 (Feb avg) | 53,042.50 |
| 6 | AADT (pedestrian) | Annual / 365 | **145.32** |

This value of 145.32 pedestrians/day is used as $\text{PedVol}$ in the 4SG signalized SPF.

### Mesa & Agate

The Mesa pedestrian volume does not enter any SPF directly, since the 3ST model does not take pedestrian volume as an input. However, the same NBPD conversion was applied to the Mesa count as a validation of the conversion process itself. Because the Mesa observation was made in February, the count can be processed two ways: using the raw February count with February seasonal factors, or first scaling the count to a May equivalent and then using May seasonal factors. If the NBPD factor tables are internally consistent, both paths should produce the same annual total.

| Step | Description | Factor | Unadjusted (Feb) | Adjusted (May) |
| --- | --- | --- | --- | --- |
| 0 | Peak hourly count | -- | 6.00 | 11.40 |
| 1 | Overnight adjustment | x1.05 | 6.30 | 11.97 |
| 2 | Hourly to daily | /0.09 (hour share, 16:00, Oct-Mar) | 70.00 | 133.00 |
| 3 | Daily to weekly | /0.12 (Thursday share) | 583.33 | 1,108.33 |
| 4 | Weekly to monthly | x4.33 (avg weeks/month) | 2,525.83 | 4,799.08 |
| 5 | Monthly to annual | /0.05 (Feb avg) or /0.095 (May avg) | 50,516.67 | 50,516.67 |
| 6 | AADT (pedestrian) | Annual / 365 | **138.40** | **138.40** |

Both paths converge on 50,517 annual pedestrians (138.40/day), confirming that the NBPD seasonal factors are self-consistent.

## Intersection Conditions

The SPFs and CMFs depend on a small set of categorical site features. These were determined from the SGM engineering reports and verified by site inspection via Google Street View. For example, we Agate has a two way left turn lane (TWLTL) and street lighting. For the 4 way stop signalized intersection at 4th street in the after scenario, the number of lanes crossed by pedestrians is a required variable. In street view it is clearly seen as 5.
