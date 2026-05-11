## Pedestrian Crash Estimation

The most significant limitation of this analysis is how pedestrian crashes are estimated at stop-controlled intersections. The HSM models used for 3ST and 4ST intersections do not take pedestrian volume as an input. Instead, pedestrian crashes are derived as a fixed proportion of total vehicle crashes: 2.1% for three-leg intersections and 2.2% for four-leg intersections. This means the pedestrian crash estimate is entirely driven by vehicle traffic volume and site geometry. An intersection with twice the pedestrian traffic but the same vehicle volume would produce the same pedestrian crash estimate, which is clearly unrealistic.

The only model in this analysis that incorporates pedestrian volume directly is the 4SG (signalized four-leg) SPF, used for the direct estimate at 4th and Agate. This model is more appropriate for pedestrian risk estimation but is only available for signalized intersections, which limits its applicability to the "after" scenario at 4th and Agate. No equivalent model exists for the unsignalized baseline or for the Mesa intersection.

## Rural vs. Urban Model Selection

Granby has a population of approximately 2,000 and meets the HSM's rural classification (populations below 5,000). The contextually appropriate HSM chapter for rural multilane highways (Chapter 11) does not include any pedestrian crash estimation capability. To obtain pedestrian crash estimates, the analysis uses the urban/suburban arterials chapter (Chapter 12) instead.

This is a necessary compromise. The urban models were calibrated on sites with different traffic patterns, land use, and pedestrian behavior than a small mountain town. The degree to which this mismatch affects the estimates is unknown.

## Minor-Road AADT at Mesa

Mesa Street has no publicly available traffic volume data, and the SGM study did not include Mesa in its traffic analysis. The minor-road AADT used in the Mesa calculations is approximated by bracketing it between the observed ratios at 4th and 6th Streets (see Data Acquisition). This produces a range of 836 to 1,826 vehicles/day.

While the results are presented across this range to show sensitivity, the true value could fall outside it. Mesa is a residential street that dead-ends into Meadow Road, which may make it lower-volume than 4th Street, or seasonal recreation traffic could push it higher. Without actual counts, there is no way to resolve this uncertainty.

## Pedestrian Volume Estimation

The daily pedestrian volumes used in this analysis (138 pedestrians/day at Mesa, 145 at 4th) are derived from single peak-hour observations made on a Thursday afternoon in February 2025. These raw counts are scaled to annual estimates using seasonal, daily, and hourly adjustment factors from the National Bicycle and Pedestrian Documentation Project.

This conversion process introduces uncertainty at every step. The seasonal adjustment alone assumes Granby's pedestrian patterns fall between "long winter" and "moderate climate" profiles, and the hourly factor depends on the time of day the observation was made. A count taken on a different day, at a different hour, or in a different season could produce a meaningfully different annual estimate.

These pedestrian volumes are only used as inputs to the 4SG signalized SPF (the direct estimate at 4th and Agate). They do not affect the stop-controlled models at all, since those models ignore pedestrian volume entirely.

## CMF Uncertainty

CMF values are point estimates derived from observational studies, and each carries its own uncertainty. The traffic signal CMF (0.77) has a published standard error and a quality rating in the CMF Clearinghouse. The curb extension CMF (0.63, CMID 1786), however, cannot be formally rated by the Clearinghouse because it appears in the 1st edition of the HSM without an adjusted standard error. The point estimate is widely used, but its uncertainty is not formally quantified.

Additionally, combining multiple CMFs multiplicatively assumes the treatments act independently. In practice, treatments at the same site can interact in ways the multiplicative model does not capture. The small number of CMFs per intersection in this analysis (three to four at most) keeps this concern manageable, but it remains a theoretical limitation.

## Calibration Factor

The HSM recommends applying a local calibration factor to adjust SPF predictions to regional crash patterns. This factor accounts for differences in driver behavior, climate, enforcement, and other local conditions that the national-level SPFs do not capture. A calibration factor of 1.0 (no adjustment) is used throughout this analysis, meaning the SPF outputs reflect national average conditions rather than Colorado or Granby-specific patterns.

## Summary

The results presented in this report should be interpreted as relative comparisons between before and after conditions rather than precise forecasts of future crash counts. The limitations above affect the absolute magnitude of the estimates but are less likely to distort the direction or general scale of the reductions. Both treatments are associated with lower expected crash frequencies under every modeling assumption tested, which provides reasonable confidence that they will improve pedestrian safety even if the exact degree of improvement is uncertain.