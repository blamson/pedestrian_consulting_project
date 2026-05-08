### Page Overview

This page simulates pedestrian crashes over a chosen time period (e.g., a decade) at a specific intersection. Each click runs a single simulation of that period, generating a random number of crashes based on the model inputs. Results are accumulated across runs and displayed in a bar chart by scenario.

Above the simulation, you’ll see the implied crash probability for each scenario, which updates as sidebar inputs change.

#### Why this is useful

The underlying outputs (e.g., “crashes per year” or “10-year probability of at least one crash”) are not very intuitive on their own. This page translates those values into tangible results. 

Each click represents one simulated time period. Across many runs, you can observe how often crashes occur under each scenario, and how outcomes vary even when the expected risk is low. Zeros will be common, but non-zero outcomes will still appear intermittently depending on the scenario.

The key question: do some scenarios consistently produce more crashes than others over repeated simulations?

#### How the simulation works

The model uses the estimated expected crashes per year and scales it to the chosen time horizon. It then samples from a **Poisson distribution**, which is commonly used to model counts of rare, independent events over time.

Each simulation draw produces an integer number of crashes (0, 1, 2, …), representing one possible realization of that scenario over the selected period.