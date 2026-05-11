## Interpreting Crash Rates as Long-Term Risk

The SPF and CMF framework produces an expected crash frequency in units of crashes per year. While useful for comparison, annual rates on the order of 0.01 to 0.03 can be difficult to interpret in practical terms. To make these estimates more tangible, they are converted into the probability of at least one pedestrian crash occurring over a 10-year period.

Crash occurrence is modeled as a Poisson process, where the number of events in a given time window follows a Poisson distribution with rate parameter equal to the annual crash frequency multiplied by the number of years. The probability of at least one crash in a 10-year period is:

$$P(\text{at least 1 crash in 10 years}) = 1 - e^{-\lambda \cdot 10}$$

where $\lambda$ is the expected number of pedestrian crashes per year. For example, a rate of 0.032 pedestrian crashes/year yields a 10-year probability of approximately 27.4%.

---

## Mesa and Agate

Mesa and Agate is a three-leg stop-controlled intersection (3ST). The proposed treatment is a curb extension (bulbout) designed to shorten crossing distances, increase pedestrian visibility, and reduce vehicle turning speeds.

Because the 3ST model is stop-controlled, pedestrian crashes are estimated indirectly as a fixed 2.1% of total vehicle crashes. The model does not take pedestrian volume as an input, which is a limitation discussed in the Limitations section.

Agate's AADT is known (11,000 vehicles/day), but Mesa's is not. The calculations below show the lower and upper ratios observed on 4th and 6th streets, which we use as proxies for Mesa's potential ratio with Agate.

### Baseline Conditions

| Metric | Low AADT (836) | High AADT (1,826) |
| --- | --- | --- |
| Total vehicle crashes/year | 0.764 | 1.067 |
| Pedestrian crashes/year | 0.016 | 0.022 |
| 10-year pedestrian crash probability | 15% | 20% |

### With Curb Extension

| Metric | Low AADT (836) | High AADT (1,826) |
| --- | --- | --- |
| Total vehicle crashes/year | 0.512 | 0.715 |
| Pedestrian crashes/year | 0.011 | 0.015 |
| 10-year pedestrian crash probability | 10% | 13% |


![Agate & Mesa: 10-year pedestrian crash probability before and after bulbout installation |900](docs/report_images/mesaBeforeAfterResults.png)

---

## 4th and Agate

4th and Agate is a four-leg stop-controlled intersection (4ST). The proposed treatment is a traffic signal installation, accompanied by a traffic diversion that reroutes left-turning vehicles from 6th Street onto 4th Street.

### Baseline Conditions

Before the diversion, the minor-to-major ratio is 0.076, giving a minor AADT of approximately 836 vehicles/day.

| Metric | Value |
| --- | --- |
| Total vehicle crashes/year | 1.466 |
| Pedestrian crashes/year | 0.032 |
| 10-year pedestrian crash probability | 28% |

### With Traffic Signal (Indirect Estimate)

As with Mesa, the baseline 4ST model estimates pedestrian crashes indirectly but using a slightly larger 2.2% of total vehicle crashes.

This approach keeps the 4ST unsignalized SPF and applies the traffic signal CMF. The minor AADT is updated to 1,386 vehicles/day to reflect the post-diversion traffic pattern.

| Metric | Baseline | Signalized |
| --- | --- | --- |
| Total vehicle crashes/year | 1.466 | 1.270 |
| Pedestrian crashes/year | 0.032 | 0.028 |
| 10-year pedestrian crash probability | 28% | 24% |

This yields a relative reduction of approximately 14%.

### With Traffic Signal (Direct Estimate)

This approach models the intersection as signalized (4SG), which unlocks a pedestrian-specific SPF that takes pedestrian volume as an explicit input (145 pedestrians/day). Unlike the indirect method, this model estimates pedestrian crashes directly rather than as a proportion of vehicle crashes.

| Metric | Value |
| --- | --- |
| Multi-vehicle crashes/year | 1.508 |
| Single-vehicle crashes/year | 0.114 |
| Pedestrian crashes/year | 0.018 |
| 10-year pedestrian crash probability | 16% |

This is the more methodologically appropriate estimate for a signalized intersection, since it incorporates actual pedestrian exposure. However, comparing it against the unsignalized baseline is not strictly apples-to-apples: the "before" comes from the 4ST model and the "after" from the 4SG model.

![Agate & 4th: 10-year pedestrian crash probability before and after signal installation |900](docs/report_images/4thBeforeAfterResults.png)

---

## Comparative Summary

![Percent reduction in 10-year pedestrian crash probability across all scenarios |900](docs/report_images/percentReductionResults.png)

At Mesa, the bulbout produces a narrow 33–35% reduction interval depending on the assumed minor-road AADT. At 4th, the reduction ranges from 14% to 43% depending on estimation method. The indirect method is more conservative; the direct method is more reliable in isolation but introduces uncertainty when compared against the unsignalized baseline.

The absolute annual crash rates are low, on the order of 0.01 to 0.03 pedestrian crashes per year, or roughly one crash every 30 to 90 years. But the 10-year probabilities are not negligible: a 15 to 28% chance of at least one pedestrian crash over a decade is meaningful, particularly given that pedestrian crashes carry a disproportionate risk of serious injury or death. Statewide, pedestrians account for 1–2% of crashes but 12–19% of fatalities.

Both treatments provide incremental but real improvements in an environment that is already low-frequency but high-consequence. These results should be interpreted as relative comparisons rather than precise forecasts. The limitations of the underlying models and input data are discussed in the Limitations section.