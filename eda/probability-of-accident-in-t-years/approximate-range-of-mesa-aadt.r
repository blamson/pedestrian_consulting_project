# Uses a normal distribution with the average of 4th and 6th minor aadt proportions

fourth_prop <- 0.076
sixth_prop <- 0.164
mu <- mean(c(fourth_prop, sixth_prop))
sigma <- sd(c(fourth_prop, sixth_prop))

set.seed(100)

x <- rnorm(100000, mu, sigma)
results <- summary(x)
print(results)

print(results * 11000)
