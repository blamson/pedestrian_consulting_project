A **Safety Performance Function (SPF)** is a negative binomial regression model that predicts the expected number of crashes per year at an intersection from its traffic volume. Each SPF is fit to crash data collected from a large number of similar sites, and the resulting curve represents the average crash frequency you would expect at a site of that type at a given traffic volume.

![An SPF is a best-fit curve through observed crash data at similar sites. Each X marks one site; the blue curve is the SPF.|450](docs/report_images/spfVisual.png)

Each X in the chart above marks one observed site, and the blue curve is the SPF. The SPF does not predict what will happen at any specific intersection, only what is typical for a site of that type at that traffic volume.

## How SPFs Work

The traffic volume input for an SPF is **AADT**, or Annual Average Daily Traffic, measured in vehicles per day. At an intersection, two AADT values are used: $\text{AADT}_{maj}$ for the major road (the higher-volume through road, in our case Agate Avenue) and $\text{AADT}_{min}$ for the minor road (the cross street with stop control, like Mesa or 4th).

In its general form, an SPF used in this analysis is:

$$\text{Crashes per year} =\; {\Large e^{\,a \,+\, b \cdot \ln(\text{AADT}_{maj}) \,+\, c \cdot \ln(\text{AADT}_{min})}}$$

The fitted coefficients $a$, $b$, and $c$ are different for each intersection type and crash type, and each SPF is fit under specific **base conditions** (geometry, lane count, lighting, and so on). Real intersections rarely match base conditions exactly. This is what CMFs are for, and they are covered in the next section.

### What "Negative Binomial" Means Here

Calling these regressions negative binomial is a statement about which probability distribution the response variable (the crash count) is assumed to follow:

- **Ordinary linear regression** assumes the response is normally distributed around the mean and fits by minimizing squared residuals.
- **Negative binomial regression** assumes the response is drawn from a negative binomial distribution with a mean $\mu$ that depends on the predictors, and fits by maximizing the negative binomial likelihood.

The $e^{(\dots)}$ on the right side of the equation comes from the **log link function** that connects the mean to the linear combination of predictors:

$$\ln(\mu) = a + b \cdot \ln(\text{AADT}_{maj}) + c \cdot \ln(\text{AADT}_{min})$$

Solving for $\mu$ gives the exponential form shown above. The log link is standard for count data because it guarantees $\mu > 0$. Predicted crash counts cannot be negative.

Why negative binomial and not Poisson? Because crash counts show **overdispersion**. A Poisson distribution has equal mean and variance, but real crash data have variance well above mean. The negative binomial accommodates this with a dispersion parameter $k$:

$$\text{Var}(Y) = \mu + k \mu^2$$

When $k = 0$ the negative binomial reduces to Poisson. The HSM reports a fitted $k$ alongside each SPF as the **overdispersion parameter**.

## SPFs Used in This Analysis

Three SPF variants from HSM Chapter 12 (Urban and Suburban Arterials) appear in this analysis, one for each intersection-state combination.

### Mesa & Agate (3ST, unsignalized)

Three-leg intersection with stop control on the minor road, both before and after the bulbout. The HSM provides two separate negative binomial models for this site type, one fit on **multi-vehicle crash counts** as the response variable and another fit on **single-vehicle crash counts**. Both share the same general form but use different coefficients:

$$\text{Multi-vehicle crashes per year} =\; {\Large e^{\,-13.36 \,+\, 1.11 \cdot \ln(\text{AADT}_{maj}) \,+\, 0.41 \cdot \ln(\text{AADT}_{min})}}$$

$$\text{Single-vehicle crashes per year} =\; {\Large e^{\,-6.81 \,+\, 0.16 \cdot \ln(\text{AADT}_{maj}) \,+\, 0.51 \cdot \ln(\text{AADT}_{min})}}$$

### 4th & Agate, Before Signal (4ST, unsignalized)

Four-leg intersection with stop control on the minor road. As with Mesa, the HSM provides two negative binomial models for this site type, each trained on a different response variable: one on multi-vehicle crash counts, the other on single-vehicle crash counts. Same general form as 3ST, with different fitted coefficients:

$$\text{Multi-vehicle crashes per year} =\; {\Large e^{\,-8.90 \,+\, 0.82 \cdot \ln(\text{AADT}_{maj}) \,+\, 0.25 \cdot \ln(\text{AADT}_{min})}}$$

$$\text{Single-vehicle crashes per year} =\; {\Large e^{\,-5.33 \,+\, 0.33 \cdot \ln(\text{AADT}_{maj}) \,+\, 0.12 \cdot \ln(\text{AADT}_{min})}}$$

### 4th & Agate, After Signal (4SG, signalized)

Once the signal is installed, the intersection is no longer 4ST. The 4SG model is a single negative binomial regression fit on a different response variable entirely: **pedestrian crash counts**. It uses a different functional form that incorporates pedestrian volume directly, alongside vehicle traffic and intersection geometry:

$$\text{Pedestrian crashes per year} =\; {\Large e^{\,-9.53 \,+\, 0.40 \cdot \ln(\text{AADT}_{total}) \,+\, 0.26 \cdot \ln(\text{AADT}_{min}/\text{AADT}_{maj}) \,+\, 0.45 \cdot \ln(\text{PedVol}) \,+\, 0.04 \cdot n_{lanes}}}$$

where $\text{AADT}_{total} = \text{AADT}_{maj} + \text{AADT}_{min}$, $\text{PedVol}$ is the daily pedestrian volume crossing all legs of the intersection, and $n_{lanes}$ is the maximum number of traffic lanes a pedestrian crosses in any single crossing maneuver.

## From Vehicle Crashes to Pedestrian Crashes

The three SPFs above predict different quantities. The 3ST and 4ST SPFs predict vehicle crashes only and need an extra step to translate into pedestrian crash estimates. The 4SG SPF predicts pedestrian crashes directly. The chain in each case:

**Mesa & Agate (3ST):**
- Sum multi-vehicle and single-vehicle SPF outputs to get total vehicle crashes
- Apply CMFs to adjust for site-specific conditions (covered in the next section)
- Multiply by **2.1%**, the HSM's fixed pedestrian crash share for 3ST intersections

**4th & Agate, Before Signal (4ST):**
- Sum multi-vehicle and single-vehicle SPF outputs to get total vehicle crashes
- Apply CMFs
- Multiply by **2.2%**, the HSM's fixed pedestrian crash share for 4ST intersections

**4th & Agate, After Signal (4SG):**
- Apply CMFs to the pedestrian SPF output
- No conversion step needed; the SPF already predicts pedestrian crashes **directly**

The 2.1% and 2.2% values are HSM defaults for stop-controlled intersections where pedestrian volume is not used as an input. This is a limitation discussed further in the Limitations section.