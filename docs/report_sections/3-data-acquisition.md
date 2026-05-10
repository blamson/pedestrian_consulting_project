This section documents the data inputs needed to apply the SPFs and CMFs from the previous sections. Three categories of data are required:

- Traffic volume on the major and minor roads at each intersection
- Pedestrian volume crossing each intersection (used by the 4SG SPF)
- Intersection conditions that determine which CMFs apply and which SPF variant to use

Each subsection below explains where the values came from and how they were derived when not directly available.

## Traffic Volume

The SPFs require **Annual Average Daily Traffic (AADT)** in vehicles per day for both the major road (Agate Avenue) and the minor road (Mesa or 4th).

### Agate Avenue (major road)

Agate AADT is published directly by the Colorado Department of Transportation. CDOT Station 101868, located on US-40 (Agate Avenue) east of Mesa Street in Granby, reports an AADT of **11,000 vehicles per day** (2024). This value is used as $\text{AADT}_{maj}$ for both Mesa & Agate and 4th & Agate.

### 4th Street and 6th Street (minor roads)

AADT is not published for the minor streets in Granby. The 2025 SGM Signal Warrant Study provides peak-hour traffic counts at the relevant intersections, both before and after the planned 6th Street left-turn diversion. AADT for each minor street is approximated by scaling the Agate AADT by the observed minor-to-major peak-hour ratio:

$$\text{AADT}_{minor} \approx \text{AADT}_{maj} \times \frac{\text{Observed minor volume}}{\text{Observed major volume}}$$

This assumes the peak-hour proportion is representative of the daily proportion. The resulting values:

![|600](docs/report_images/4th6thVolumeCalculations.png)

The 4th Street AADT rises from 836 to 1,386 after the diversion, since left-turn traffic from 6th is rerouted through 4th. 6th Street AADT correspondingly drops from 1,826 to 352.

### Mesa Street (minor road)

Mesa Street has no observed traffic counts in either the SGM study or any public dataset. Without direct data, two bounding estimates are used:

- **Lower bound:** 836 vehicles/day (matches 4th Street before diversion)
- **Upper bound:** 1,826 vehicles/day (matches 6th Street before diversion)

These bounds are carried through the analysis as a sensitivity range. The Results section reports outcomes at both bounds.

## Pedestrian Volume

The 4SG SPF requires daily pedestrian volume crossing all legs of the intersection. The SGM Mesa & Agate study and the Signal Warrant Study both provide raw peak-hour pedestrian counts but not daily volumes. A conversion process from the National Bicycle & Pedestrian Documentation Project, attached to the SGM memo, scales hourly peak counts into a daily AADT through a series of seasonal, weekday, and monthly factors.

The chain of factors at Mesa & Agate is:

![Conversion of peak hourly pedestrian count (6 pedestrians) to daily AADT (138.4 pedestrians/day) through hourly, daily, weekly, monthly, and annual adjustments. The same chain applied to 4th & Agate with peak count 7 yields 145.3 pedestrians/day.|600](docs/report_images/mesaPedCalculation.png)

Applied to both intersections, the conversion gives:

- **Mesa & Agate:** 138.4 pedestrians/day (peak hourly count of 6)
- **4th & Agate:** 145.3 pedestrians/day (peak hourly count of 7)

These values feed into the 4SG SPF as $\text{PedVol}$. As a sanity check, the Mesa conversion was run twice, once with a raw peak count and once with the same count seasonally rescaled to a different reference month. Both paths produce the same annual total of 50,517 pedestrians, which divides to the same 138.4 daily average. The conversion is internally consistent.

## Intersection Conditions

The SPFs and CMFs depend on a small set of categorical site features. These were determined from the SGM engineering reports and verified by site inspection via Google Street View.

| Feature | Mesa & Agate | 4th & Agate |
| --- | --- | --- |
| Intersection legs | 3 | 4 |
| Traffic control (before / after) | Stop / Stop | Stop / Signal |
| HSM site type (before / after) | 3ST / 3ST | 4ST / 4SG |
| Major road configuration | 5-lane with TWLTL | 5-lane with TWLTL |
| Lighting | Present | Present |
| Lanes crossed by pedestrian (4SG only) | n/a | 5 |

The lighting and TWLTL entries are what trigger the lighting and TWLTL CMFs from the previous section. The site type entries determine which SPF is applied at each state, and the lanes-crossed entry feeds into the 4SG pedestrian SPF as $n_{lanes}$.