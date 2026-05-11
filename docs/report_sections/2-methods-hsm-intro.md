The **Highway Safety Manual (HSM)** is the federal standard for estimating crash risk on roads and at intersections. Published by the American Association of State Highway and Transportation Officials (AASHTO) with support from the Federal Highway Administration (FHWA), it provides a standardized, evidence-based methodology used by transportation engineers across the country.

The HSM lets us answer the question that motivates this project: how much would installing a particular treatment (a bulbout, a traffic signal) actually reduce crash risk at a specific intersection? It does so by combining two tools:

- A **Safety Performance Function (SPF)** estimates the baseline number of crashes per year at an intersection from its traffic volume and core characteristics.
- One or more **Crash Modification Factors (CMFs)** adjust that baseline up or down to reflect site-specific features such as lighting, turn lanes, signal control, or curb extensions.

Together, these produce both vehicle and pedestrian crash estimates for an intersection in a specific configuration. SPFs are covered in a separate section.

### The SPF+CMF Calculation is a Snapshot

A single SPF+CMF calculation produces one number: the expected crash frequency at one intersection in one specific configuration. It is not a forecast of what will happen over the next several years. It is a snapshot of risk under one set of conditions.

![Each SPF+CMF calculation produces a snapshot of crash risk for one intersection condition. Comparing before and after snapshots quantifies the treatment's effect. |900](docs/report_images/snapshotVisual.png)

> To measure the effect of a treatment, take the snapshot twice (once before, once after) and compare.

For 4th & Agate, the before snapshot describes a four-leg unsignalized intersection with the existing minor-road traffic on 4th Street. The after snapshot describes the same intersection with a signal installed and additional vehicles routed through it from the 6th Street left-turn diversion. Each state gets its own calculation, and the difference between them quantifies the safety impact. The same logic applies to Mesa & Agate: one snapshot describes the intersection without the bulbout, another with the bulbout in place. 

### Choosing the Right HSM Chapter

The HSM organizes its predictive methods into three chapters:

- **Chapter 10:** Rural two-lane, two-way roads
- **Chapter 11:** Rural multilane highways
- **Chapter 12:** Urban and suburban arterials

Selection follows FHWA's classification rule: areas with populations above 5,000 are urban, and below that threshold are rural. Granby has a population of approximately 2,000, which places it firmly in the rural category. Chapter 11 would normally be the right choice, since Agate Avenue is a multilane road in a rural setting.

However, Chapter 11 contains no pedestrian crash model. Its SPFs estimate vehicle crashes only, with no mechanism for translating those into pedestrian crash estimates. Because pedestrian risk is the entire focus of this analysis, Chapter 11 cannot be used.

The remaining options are narrow. Chapter 10 covers only two-lane roads, which excludes the five-lane Agate corridor. That leaves Chapter 12, Urban and Suburban Arterials, as the only chapter with the SPFs and CMFs needed for pedestrian analysis at multilane intersections. We use Chapter 12 throughout, with the understanding that this is a contextual mismatch: the chapter was developed for higher-density urban settings, and applying it to a town the size of Granby introduces a limitation.