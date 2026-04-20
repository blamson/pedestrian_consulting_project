# This script takes advantage of the "accidents per year" output we get from HSM models
# We get another perspective on the output here, seeing the probability of at least one accident in 10 years
# We use the poisson distribution for this, and assume a constant npedi rate over t years.
# This gives us a lambda=npedi * t
# We want: 1 - P(0 accidents in 10 years)

calc_probability <- function(num_acc_per_year=1, years=10){
  # Assumes a constant rate across all years
  # Common input for accidents per year is npedi from hsm output

  lambda <- num_acc_per_year * years
  prob_accident <- round(1 - ppois(0, lambda), 5)
  print(glue::glue("Probability of an accident in {years} years: {prob_accident * 100}%"))

  return(prob_accident)
}

t <- 10

x1 <- calc_probability(0.016, t)
x2 <- calc_probability(0.022, t)

change <- (x1-x2)/x1 
