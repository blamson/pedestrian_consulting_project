library(dplyr)
library(readr)

is_missing_like <- function(x) {
  if (is.null(x)) return(TRUE)
  if (length(x) == 0) return(TRUE)
  if (all(is.na(x))) return(TRUE)
  FALSE
}


stop_if_missing_like <- function(variable_name, value) {
  if (is_missing_like(value)) {
    stop(sprintf("%s is missing or invalid", variable_name))
  }
}


validate_inputs <- function(
  int_type, 
  aadt_major, 
  aadt_minor, 
  aadt_max,
  signal_cmf,
  pedvol = NULL, 
  nlanes = NULL
) {
  # Existence checks ---
  stop_if_missing_like("int_type", int_type)
  stop_if_missing_like("aadt_major", aadt_major)
  stop_if_missing_like("aadt_minor", aadt_minor)
  stop_if_missing_like("aadt_max", aadt_max)
  
  int_type <- tolower(trimws(int_type))
  allowed_types <- unique(aadt_max$intersection_type)

  if (!int_type %in% allowed_types) {
    stop(sprintf("Unsupported intersection type: %s", int_type))
  }

  # Signalized specific checks ---
  if (int_type %in% c("4sg", "3sg")) {
    stop_if_missing_like("pedvol", pedvol)
    stop_if_missing_like("nlanes", nlanes)
    if ((nlanes <= 0) | (pedvol <= 0)) {
      stop(sprintf(
        "pedvol and nlanes must be greater than 0: pedvol: %s, nlanes: %s",
        pedvol, nlanes
      ))
    }

    if (nlanes > 10) {
      stop(sprintf(
        "nlanes value must be realistic: nlanes: %s",
        nlanes
      ))
    }

    if (signal_cmf) {
      stop(sprintf(
        "The traffic signal CMF cannot be applied when using a signalized SPF: signal_spf: %s",
        signal_cmf
      ))
    }
  }

  if ((aadt_minor <= 0) | (aadt_major <= 0)) {
    stop(sprintf(
      "Both AADT variables must be greater than 0: aadt_major: %s, aadt_minor: %s",
      aadt_major, aadt_minor
    ))
  }

  # Ensure AADT values are within supported ranges for a given SPF ---
  limits <- aadt_max |>
    dplyr::filter(intersection_type == int_type)

  if (nrow(limits) != 1) {
    stop(sprintf("Expected exactly one row for %s in aadt_max", int_type))
  }

  if (aadt_major > limits$aadt_major) {
    stop(sprintf(
      "aadt_major exceeds max for %s: %s > %s",
      int_type, aadt_major, limits$aadt_major
    ))
  }

  if (aadt_minor > limits$aadt_minor) {
    stop(sprintf(
      "aadt_minor exceeds max for %s: %s > %s",
      int_type, aadt_minor, limits$aadt_minor
    ))
  }

  if (aadt_minor > aadt_major) {
    stop(sprintf(
      "aadt_minor exceeds aadt_major: %s > %s",
      aadt_minor, aadt_major
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


compute_spf_ped_signalized <- function(spf_row, aadt_major, aadt_minor, pedvol, nlanes) {
  # Taken from HSM formula 12-29
  exp(
    spf_row$a +
    spf_row$b * log(aadt_major + aadt_minor) +
    spf_row$c * log(aadt_minor / aadt_major) +
    spf_row$d * log(pedvol) + 
    spf_row$e * nlanes
  )
}


compute_cmfs <- function(
  lighting,
  twltl,
  # bulbout,
  signal_cmf
) {
  # Return the product of all provided CMFs for vehicles

  prod(c(
    lighting = if (lighting) 0.91 else 1,
    twltl = if (twltl) 0.92 else 1,
    # bulbout = if (bulbout) 0.63 else 1,
    signal_cmf = if (signal_cmf) 0.77 else 1
  ))
}


compute_cmfs_ped <- function(
  bulbout,
  school = FALSE
) {
  # Pedestrian-only CMFs
  prod(c(
    bulbout = if (bulbout) 0.63 else 1,
    school = if (school) 1.35 else 1   # Value taken from Table 12-29
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
  aadt_max,
  # Signalized only variables ---
  pedvol=NULL,
  nlanes=NULL,
  # CMFs ---
  lighting=FALSE,
  twltl=FALSE,
  signal_cmf=FALSE,
  # Pedestrian only CMFs ---
  bulbout=FALSE,
  school=FALSE # pedestrian and signalized only
) {
  validate_inputs(int_type=int_type, aadt_major=aadt_major, aadt_minor=aadt_minor, pedvol=pedvol, nlanes=nlanes, aadt_max=aadt_max, signal_cmf=signal_cmf)
  int_type <- tolower(trimws(int_type))

  spfs <- spfs |>
    mutate(
      intersection_type = tolower(as.character(intersection_type)),
      crash_type = tolower(as.character(crash_type))
    )

  spf_mv <- spfs |>
    filter(intersection_type == int_type, crash_type == "mv")

  spf_sv <- spfs |>
    filter(intersection_type == int_type, crash_type == "sv")

  # Multi and single vehicle crashes ---
  nbimv <- compute_spf(spf_mv, aadt_major, aadt_minor)
  nbisv <- compute_spf(spf_sv, aadt_major, aadt_minor)
  nbi <- nbimv + nbisv

  # Pedestrian crashes ---
  if (int_type %in% c("4sg", "3sg")) {
    spf_ped <- spfs |> 
      filter(intersection_type == int_type, crash_type == "ped")

    nped_base <- compute_spf_ped_signalized(
      spf_ped,
      aadt_major,
      aadt_minor,
      pedvol,
      nlanes
    )

    fpedi <- NULL
  } else {
    # regular pedestrian handling
    fpedi <- get_ped_factor(int_type)
    nped_base <- nbi * fpedi
  }

  cmf_veh <- compute_cmfs(
    lighting,
    twltl,
    signal_cmf
  )

  cmf_ped <- compute_cmfs_ped(
    bulbout,
    school
  )

  pred_veh = nbi * cmf_veh
  pred_ped = nped_base * cmf_veh * cmf_ped


  # Return single row data frame with all relevant information
  tibble::tibble(
    intersection_type = int_type,
    lighting = lighting,
    twltl = twltl,
    bulbout = bulbout,
    signal_cmf = signal_cmf,
    school = school,
    pedvol = pedvol,
    nlanes = nlanes,
    aadt_maj = aadt_major,
    aadt_minor = aadt_minor,
    nbi_mv = nbimv,
    nbi_sv = nbisv,
    nbi_all = nbi,
    cmf_veh = cmf_veh,
    cmf_ped = cmf_ped,
    ped_factor = fpedi,
    pred_veh = pred_veh, #nbi * cmf_product,
    pred_ped = pred_ped #nbi * cmf_product * fpedi,
  )
}

# MAIN SCRIPT ---
spfs <- read_csv("data/spfs.csv")
aadt_max <- readr::read_csv("data/aadt_maximums.csv", show_col_types = FALSE)

print("Calculating estimates for Agate and 4th")
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

# readr::write_csv(result, "data/results_04-18-2026.csv")
