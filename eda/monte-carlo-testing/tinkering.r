r_cmf <- function(n, mean, sd) {
  sigma2_log <- log(1 + (sd^2 / mean^2))
  mu_log     <- log(mean) - 0.5 * sigma2_log
  
  rlnorm(n, mu_log, sqrt(sigma2_log))
}

signal <- r_cmf(10000, 0.77, 0.27)
summary(signal)

# https://cmfclearinghouse.fhwa.dot.gov/detail.php?facid=1285
twltl <- r_cmf(10000, 0.92, 0.157)
summary(twltl)
plot(density(twltl))

# point estimate
# 3st:         p = 0.238
# 4st:         p = 0.229
# 3sg and 3sg: p = 0.235
lighting <- 1 - (0.38 * 0.229)

combined <- signal * twltl * lighting
summary(combined)
plot(density(combined))

