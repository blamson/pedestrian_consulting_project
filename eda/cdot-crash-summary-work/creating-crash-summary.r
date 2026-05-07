library(tibble)
library(dplyr)
library(ggplot2)
library(tidyr)
library(ggrepel)

years <- 2015:2025
crashes <- c(120703, 120770, 119104, 122356, 121407, 86817, 97790, 95381, 102786, 100665, 96173)
fatal_crashes <- c(507, 558, 600, 588, 544, 574, 638, 699, 666, 642, 642)
ped_crashes <- c(1367, 1412, 1448, 1418, 1383, 1062, 1260, 1312, 1570, 1701, 1626)
ped_fatal_crashes <- c(59, 77, 87, 86, 70, 88, 84, 104, 128, 110, 114)

df <- tibble::tibble(
  years = years,
  crashes = crashes,
  fatal_crashes = fatal_crashes,
  ped_crashes = ped_crashes,
  ped_fatal_crashes = ped_fatal_crashes
)



# plot <- df %>%
#   mutate(
#     ped_share = ped_crashes / crashes,
#     ped_fatal_share = ped_fatal_crashes / fatal_crashes
#   ) %>%
#   select(years, ped_share, ped_fatal_share) %>%
#   pivot_longer(-years, names_to = "type", values_to = "value") %>%
#   ggplot(aes(x = years, y = value, color = type)) +
#   geom_line(size = 1.2) +
#   geom_text_repel(
#     aes(label = scales::percent(value, accuracy = 0.1)),
#     size = 3,
#     box.padding=0.25,
#     point.padding=0.25,
#     show.legend = FALSE,
#     max.overlaps = Inf
#   ) +
#   scale_y_continuous(labels = scales::percent) +
#   scale_x_continuous(breaks=df$years) +
#   scale_color_discrete(
#     labels = c(
#       "ped_share" = "% of All Crashes",
#       "ped_fatal_share" = "% of Fatal Crashes"
#     )
#   ) +
#   labs(
#     y = "",
#     x = "Year",
#     color = "",
#     title = "Pedestrians Represent a Small Share of Crashes but a Large Share of Fatalities"
#   ) +
#   theme(
#     legend.position = "top",
#     legend.justification = "center",
#     legend.direction = "horizontal"
#   )

# ggsave(
#   filename = "pedestrian_crash_plot.png",
#   plot = plot,
#   width = 10,
#   height = 6,
#   units = "in",
#   dpi = 300
# )
