source("src/R/crash-frequency-helpers.r")

library(dplyr)
library(readr)

print("Reading in necessary data ---")
spfs <- read_csv("data/spfs.csv")
aadt_max <- readr::read_csv("data/aadt_maximums.csv", show_col_types = FALSE)

print("Calculating estimates for Agate and 4th ---")
base_4th <- estimate_crashes(
  spfs,
  int_type = "4ST",
  aadt_major = 11000,
  aadt_minor = 836,
  aadt_max = aadt_max,
  lighting = TRUE,
  twltl = TRUE
)

post_4th <- estimate_crashes(
  spfs,
  int_type = "4ST",
  aadt_major = 11000,
  aadt_minor = 1386,
  aadt_max = aadt_max,
  lighting = TRUE,
  twltl = TRUE,
  signal_cmf = TRUE
)

post_4th_signalized <- estimate_crashes(
  spfs,
  int_type = "4SG",
  aadt_major = 11000,
  aadt_minor = 1386,
  aadt_max = aadt_max,
  lighting = TRUE,
  twltl = TRUE,
  nlanes = 5,
  pedvol = 53042.5 / 365
)

print("Calculating estimates for Agate and Mesa ---")
aadt_minor <- 0.076 * 11000
base_mesa_low <- estimate_crashes(
  spfs,
  int_type = "3ST",
  aadt_major = 11000,
  aadt_minor = aadt_minor,
  aadt_max = aadt_max,
  lighting = TRUE,
  twltl = TRUE
)

post_mesa_low <- estimate_crashes(
  spfs,
  int_type = "3ST",
  aadt_major = 11000,
  aadt_minor = aadt_minor,
  aadt_max = aadt_max,
  lighting = TRUE,
  twltl = TRUE,
  bulbout = TRUE
)

aadt_minor <- 0.166 * 11000
base_mesa_high <- estimate_crashes(
  spfs,
  int_type = "3ST",
  aadt_major = 11000,
  aadt_minor = aadt_minor,
  aadt_max = aadt_max,
  lighting = TRUE,
  twltl = TRUE
)

post_mesa_high <- estimate_crashes(
  spfs,
  int_type = "3ST",
  aadt_major = 11000,
  aadt_minor = aadt_minor,
  aadt_max = aadt_max,
  lighting = TRUE,
  twltl = TRUE,
  bulbout = TRUE
)

result <- bind_rows(list(base_4th, post_4th, post_4th_signalized, base_mesa_low, base_mesa_high, post_mesa_low, post_mesa_high))

write <- FALSE
if (write){readr::write_csv(result, paste0("data/results_", Sys.Date(), ".csv"))}