library(dplyr)

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
  # This validation function is very aggressive, basically just kills the process if anything fails. 
  # Anything more sophisticated than that is out of scope for this project

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
  signal_cmf
) {
  # Return the product of all provided CMFs for vehicles
  # Lighting cmf taken from HSM equation 12-36
  # Signal cmf taken from cmfclearinghouse - cmid 319
  # TWLTL cmf taken from cmfclearinghouse - cmid 1285

  prod(c(
    lighting = if (lighting) 0.91 else 1,
    twltl = if (twltl) 0.92 else 1,
    signal_cmf = if (signal_cmf) 0.77 else 1
  ))
}


compute_cmfs_ped <- function(
  bulbout,
  school = FALSE
) {
  # Pedestrian-only CMFs
  # Bulbout cmf taken from cmfclearinghouse - cmid 1786
  # School cmf taken from HSM table 12-29
  prod(c(
    bulbout = if (bulbout) 0.63 else 1,
    school = if (school) 1.35 else 1   # Value taken from HSM table 12-29
  ))
}


get_ped_factor <- function(int_type) {
  int_type <- tolower(int_type)

  if (int_type == "3st") return(0.021)
  if (int_type == "4st") return(0.022)

  1
}


calc_long_term_ped_accident_probability <- function(num_acc_per_year=1, years=10){
  # This script takes advantage of the "accidents per year" output we get from HSM models
  # We get another perspective on the output here, seeing the probability of at least one accident in 10 years
  # We use the poisson distribution for this, and assume a constant npedi rate over t years.
  # This gives us a lambda=npedi * t
  # We want: 1 - P(0 accidents in 10 years)
  # Assumes a constant rate across all years
  # Common input for accidents per year is npedi from hsm output

  lambda <- num_acc_per_year * years
  prob_accident <- round(1 - ppois(0, lambda), 5)

  return(prob_accident)
}


estimate_crashes <- function(
  spfs,
  int_name,
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

  # sanitize the spf dataframe to work in this context
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
    # unsignalized pedestrian estimation is just a flat proportion of total crashes
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
  ten_year_ped_prob = calc_long_term_ped_accident_probability(pred_ped)

  # Return single row data frame with all relevant information
  # This feels hacky and weird, but to be honest is the easiest way I can think of to contain everything I care about. 
  tibble::tibble(
    intersection_name = int_name,
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
    nped_base = nped_base,
    cmf_veh = cmf_veh,
    cmf_ped = cmf_ped,
    ped_factor = fpedi,
    pred_veh = pred_veh, 
    pred_ped = pred_ped, 
    ten_year_ped_prob = ten_year_ped_prob
  )
}