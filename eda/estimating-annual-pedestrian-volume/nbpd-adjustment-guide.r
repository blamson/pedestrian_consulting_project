library(glue)
hourly_to_annual <- function(intersection_name, hourly_counts, hour_factor, day_factor, month_factor) {
  print(glue("Estimating pedestrian volume for {intersection_name}"))

  print(glue("Hourly volume: {hourly_counts}"))

  print(glue("Step 1. Adjusting for evening pedestrian traffic ---"))
  hourly_counts_adj <- hourly_counts * 1.05
  print(glue("Hourly volume adjusted: {hourly_counts_adj}"))

  print(glue("Step 2. Estimating daily volume ---"))
  day_counts <- hourly_counts_adj / hour_factor
  print(glue("Daily volume: {day_counts}"))

  print(glue("Step 3. Estimating weekly volume ---"))
  weekly_counts <- day_counts / day_factor
  print(glue("Weekly volume: {weekly_counts}"))

  print(glue("Step 4. Estimating monthly volume ---"))
  # 4.33 is average number of weeks per month
  month_counts <- weekly_counts * 4.33 
  print(glue("Monthly volume: {month_counts}"))

  print(glue("Step 5. Estimating annual volume ---"))
  annual_counts <- month_counts / month_factor
  print(glue("Annual volume: {annual_counts}"))

  return(annual_counts)
}

# Mesa and Agate ---
intersection_name <- "Mesa and Agate"
annual_ped_volume <- hourly_to_annual(intersection_name=intersection_name, hourly_counts=6, hour_factor=0.09, day_factor = 0.12, month_factor = 0.05)
# hourly_to_annual(11.4, hour_factor=0.09, day_factor = 0.12, month_factor = 0.095)

# aadt <- 11000
# annual_veh_volume <- aadt * 365

# exposure <- annual_ped_volume * annual_veh_volume
# exposure_pm <- exposure / 1000000
# print(glue("Exposure per million interactions: {exposure_pm}"))

# 4th and Agate

# 4th and Agate ---
intersection_name <- "4th and Agate"
annual_ped_volume <- hourly_to_annual(intersection_name=intersection_name, hourly_counts=7, hour_factor=0.10, day_factor = 0.12, month_factor = 0.05)

