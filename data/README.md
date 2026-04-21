# Data
git 
This directory contains all of the data files used or kept as reference in this project. 

- `crash-modification-factors/`: Contains a large dataset on all of the crash modification factors from cmfclearinghouse. Wasn't really used much beyond initial exploration, was far easier to just use the cmfclearinghouse website directly. 
- `results/`: Self explanatory
- AADT tables:
    - `04a_aadt.csv`: Contains basic addt info on relevant road segments.
    - `AADT.csv`: Contains the same information as above with a bit more detail. Was never used.
    - `aadt_maximums.csv`: Manually created using the HSM excel tool. Shows the range of appropriate AADT values for each kind of model. Used in estimating crash frequencies. 
- `spfs.csv`: Manually created using model coefficients pulled from the HSM. Used in estimating crash frequencies.