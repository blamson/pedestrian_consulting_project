library(dplyr)
library(glue)
library(readr)

validate_inputs <- function(int_type, aadt_major, aadt_minor) {
  aadt_max <- readr::read_csv("data/aadt_maximums.csv")
  int_type <- tolower(int_type)

  allowed_types <- unique(aadt_max$intersection_type)

  if (!int_type %in% allowed_types) {
    stop(glue("Unsupported intersection type: {int_type}"))
  }

  if (grepl("sg$", int_type)) {
    stop(glue("Signalized intersections ({int_type}) not supported yet"))
  }

  limits <- aadt_max |>
    filter(intersection_type == int_type)

  if (aadt_major > limits$aadt_major) {
    stop(glue(
      "aadt_major exceeds max for {int_type}: {aadt_major} > {limits$aadt_major}"
    ))
  }

  if (aadt_minor > limits$aadt_minor) {
    stop(glue(
      "aadt_minor exceeds max for {int_type}: {aadt_minor} > {limits$aadt_minor}"
    ))
  }

  invisible(TRUE)
}


compute_spf <- function(spf_row, aadt_major, aadt_minor) {
  exp(
    spf_row$a +
    spf_row$b * log(aadt_major) +
    spf_row$c * log(aadt_minor)
  )
}


compute_cmfs <- function(
  lighting,
  twltl,
  bulbout,
  signal
) {
  # Return the product of all provided CMFs

  prod(c(
    lighting = if (lighting) 0.91 else 1,
    twltl = if (twltl) 0.92 else 1,
    bulbout = if (bulbout) 0.63 else 1,
    signal = if (signal) 0.77 else 1
  ))
}


get_ped_factor <- function(int_type) {
  int_type <- tolower(int_type)

  if (int_type == "3st") return(0.021)
  if (int_type == "4st") return(0.022)

  1
}

estimate_crashes <- function(
  spfs,
  int_type,
  aadt_major,
  aadt_minor,
  lighting,
  twltl,
  bulbout,
  signal
) {
  validate_inputs(int_type, aadt_major, aadt_minor)
  int_type <- tolower(int_type)

  spfs <- spfs |>
    mutate(
      intersection_type = tolower(as.character(intersection_type)),
      crash_type = tolower(as.character(crash_type))
    )

  spf_mv <- spfs |>
    filter(intersection_type == int_type, crash_type == "mv")

  spf_sv <- spfs |>
    filter(intersection_type == int_type, crash_type == "sv")

  nbimv <- compute_spf(spf_mv, aadt_major, aadt_minor)
  nbisv <- compute_spf(spf_sv, aadt_major, aadt_minor)

  nbi <- nbimv + nbisv

  cmf_product <- compute_cmfs(
    lighting,
    twltl,
    bulbout,
    signal
  )

  fpedi <- get_ped_factor(int_type)

  # Return single row data frame with all relevant information
  tibble::tibble(
    intersection_type = int_type,
    lighting = lighting,
    twltl = twltl,
    bulbout = bulbout,
    signal = signal,
    aadt_maj = aadt_major,
    aadt_minor = aadt_minor,
    nbi_mv = nbimv,
    nbi_sv = nbisv,
    nbi_all = nbi,
    cmf_product = cmf_product,
    ped_factor = fpedi,
    pred_veh = nbi * cmf_product,
    pred_ped = nbi * cmf_product * fpedi,
  )
}

# MAIN SCRIPT ---
spfs <- read_csv("data/spfs.csv")

baseline <- estimate_crashes(
  spfs,
  int_type = "4ST",
  aadt_major = 11000,
  aadt_minor = 836,
  lighting = TRUE,
  twltl = TRUE,
  bulbout = FALSE,
  signal = FALSE
)

after <- estimate_crashes(
  spfs,
  int_type = "4ST",
  aadt_major = 11000,
  aadt_minor = 1386,
  lighting = TRUE,
  twltl = TRUE,
  bulbout = FALSE,
  signal = TRUE
)

result <- baseline %>% bind_rows(after)
