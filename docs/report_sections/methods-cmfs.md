A **Crash Modification Factor (CMF)** is a multiplier that adjusts the SPF's baseline crash estimate to reflect site-specific features that depart from the SPF's base conditions. Where the SPF answers "how many crashes per year for an intersection of this type at this traffic volume?", CMFs answer "how does this answer change because lighting is present, or because there is a turn lane, or because a signal was just installed?"

A CMF is defined as the ratio of expected crash frequency with the feature in place to expected crash frequency without:

$$\text{CMF} = \frac{\text{Expected crash frequency with treatment}}{\text{Expected crash frequency without treatment}}$$

- $\text{CMF} = 1$: no effect on expected crash frequency
- $\text{CMF} < 1$: the feature is associated with fewer crashes than the base condition
- $\text{CMF} > 1$: the feature is associated with more crashes than the base condition

<!-- row -->
![Improves nighttime visibility, reducing crashes.](docs/report_images/lightCMFvisual.png)
![Separates turning vehicles from through traffic, reducing conflicts.](docs/report_images/leftTurnCMFvisual.png)
![Steep grades lengthen stopping distance, raising crash risk.](docs/report_images/gradeCMFvisual.png)
![Alcohol sales nearby are linked to higher-risk driving.](docs/report_images/alcoholCMFvisual.png)
<!-- /row -->

## Combining Multiple CMFs

Real intersections depart from base conditions in more than one way: lighting is present, a turn lane exists, a signal is installed, and so on. Each departure contributes its own CMF, and the standard HSM practice is to combine them multiplicatively:

$$N_{\text{predicted}} = N_{\text{SPF}} \cdot \text{CMF}_1 \cdot \text{CMF}_2 \cdot\, \cdots\, \cdot \text{CMF}_n$$

This assumes the treatments act independently, meaning the effect of installing a signal is the same regardless of whether lighting is present, and vice versa. In practice, treatments at the same site can interact, and the multiplicative combination can over or under count the joint effect. The HSM acknowledges this and recommends judgment when stacking many CMFs at one site. For this analysis, the small number of treatments per intersection (three to four CMFs at most) keeps the concern manageable.

## Where CMFs Come From

Two sources are used in this analysis:

- **HSM Chapter 12.** The HSM publishes CMFs for the most common geometric and traffic-control features, including lighting, turn lanes, left-turn signal phasing, and red-light cameras. These are organized in tables alongside the SPFs they apply to.
- **CMF Clearinghouse.** Maintained by the FHWA, this is a public database of thousands of CMFs derived from individual research studies, indexed by countermeasure ID (CMID). It is the primary source for treatments not covered by the HSM, including curb extensions.

Each Clearinghouse entry comes with a quality rating, a standard error where available, and a citation to the original study.

## CMFs Used in This Analysis

Four CMFs appear in this analysis:

| CMF | Value | Source | Applies to |
| --- | --- | --- | --- |
| Lighting | 0.91 | HSM Ch 12 (Equation 12-36) | Both intersections, both states (lighting is present on Agate) |
| TWLTL (two-way left-turn lane) | 0.92 | CMF Clearinghouse | Both intersections, both states (Agate has a center TWLTL) |
| Traffic signal installation | 0.77 | CMF Clearinghouse, CMID 319 | 4th & Agate, after-signal only |
| Curb extension (bulbout) | 0.63 | CMF Clearinghouse, CMID 1786 | Mesa & Agate, after-bulbout only |

The combined CMF for each intersection-state is the product of all applicable CMFs:

- **Mesa & Agate, before:** $0.91 \times 0.92 = 0.84$
- **Mesa & Agate, after:** $0.91 \times 0.92 \times 0.63 = 0.53$
- **4th & Agate, before:** $0.91 \times 0.92 = 0.84$
- **4th & Agate, after:** $0.91 \times 0.92 \times 0.77 = 0.65$

These combined values are what get multiplied into the SPF outputs to produce the final crash frequency estimates.

## A Note on CMF Quality

CMF values are estimated from observational studies, and not all CMFs are equally reliable. The HSM and the CMF Clearinghouse both report standard errors and quality ratings where available. The curb extension CMF used here (CMID 1786) carries a notable caveat: the Clearinghouse reports that this CMF cannot be formally rated because it appears in the 1st edition of the HSM without an adjusted standard error. The point estimate of 0.63 is widely cited and applied, but its uncertainty is not formally quantified. This is one of several reasons the Limitations section frames the analysis as a relative comparison rather than a precise forecast.