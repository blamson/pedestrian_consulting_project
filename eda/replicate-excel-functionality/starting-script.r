library(dplyr)
library(glue)
library(readr)

compute_spf <- function(spf_row, aadt_maj, aadt_min) {
  exp(
    spf_row$a +
    spf_row$b * log(aadt_maj) +
    spf_row$c * log(aadt_min)
  )
}

print("Reading data ---")
spfs <- readr::read_csv("data/spfs.csv") %>%
  mutate(
    intersection_type = factor(intersection_type),
    crash_type = factor(crash_type)
  )

print("Setting parameters ---")
int_type <- "4ST"
aadt_maj <- 11000
aadt_minor <- 1826
lighting <- TRUE # 0.91
twltl <- TRUE # 0.92
bulbout <- TRUE # 0.63
signal <- FALSE # 0.77


print("Calculating multi vehicle crash rate ---")
spf <- spfs %>% filter(intersection_type == tolower(int_type) & crash_type == "mv")
nbimv <- compute_spf(spf, aadt_maj=aadt_maj, aadt_min = aadt_minor)
print(glue("Initial Nbimv: {round(nbimv, 5)}"))

print("Calculating single vehicle crash rate ---")
spf <- spfs %>% filter(intersection_type == tolower(int_type) & crash_type == "sv")
nbisv <- compute_spf(spf, aadt_maj=aadt_maj, aadt_min = aadt_minor)
print(glue("Initial Nbisv: {round(nbisv, 5)}"))

nbi <- nbimv + nbisv
print(glue("Initial Nbi: {round(nbi, 5)}"))

cmfs <- c(
  lighting = if (lighting) 0.91 else 1,
  twltl = if (twltl) 0.92 else 1,
  bulbout = if (bulbout) 0.63 else 1,
  signal = if (signal) 0.77 else 1
)

cmf_combined <- prod(cmfs)
print(glue("Combined cmf: {round(cmf_combined, 5)}"))

if (tolower(int_type) == "3st") {
  fpedi <- 0.021
} else if (tolower(int_type) == "4st") {
  fpedi <- 0.022
} else {
  # This will need a separate handling later as sg intersections use a totally different spf entirely. 
  fpedi <- 1
}

npedi <- nbi * cmf_combined * fpedi
print(glue("Predicted vehicular crashes per year:  {round(nbi * cmf_combined, 5)}"))
print(glue("Predicted pedestrian crashes per year: {round(npedi, 5)}"))
