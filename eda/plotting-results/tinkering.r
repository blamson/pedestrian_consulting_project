library(dplyr)
library(tidyr)
library(ggplot2)
library(ggrepel)

df <- readr::read_csv("data/results_2026-04-19.csv", show_col_types = FALSE) %>%
  mutate(
    intersection_type = as.factor(intersection_type),
    treatment = case_when(
        intersection_type == "4sg" ~ "Signal",
        bulbout ~ "Bulbout",
        signal_cmf ~ "Signal",
        TRUE ~ "Baseline"
    ),
    treatment = factor(treatment, levels = c("Baseline", "Bulbout", "Signal")),
    condition = case_when(
      treatment == "Baseline" ~ "Before",
      TRUE ~ "After"
    ),
    condition = factor(condition, levels=c("Before", "After"))
  ) %>%
  select(
    intersection_name,
    intersection_type,
    pred_veh,
    pred_ped,
    ten_year_ped_prob,
    treatment,
    condition
  )

myplot <- ggplot(df, aes(y=ten_year_ped_prob*100, x=intersection_name)) +
  geom_line(aes(color=condition)) +
  geom_point(aes(color = condition)) +
  labs(
    title=stringr::str_wrap("Probability of a Pedestrian Accident in a 10 Year Period - Before and After", 60),
    subtitle="Ranges show outcomes under different models or traffic volumes",
    color="Intersection Treatment"
  ) +
  xlab("") +
  ylab("Chance of Accident (%)") +
  # ylim(0, 28) +
  scale_y_continuous(
    limits=c(0, 28),
    breaks=seq(0,25,5)
  ) +
  theme(legend.position="bottom") +
  geom_label_repel(
    aes(
      label=paste0(round(ten_year_ped_prob*100), "%")
    )
  )

ggsave(myplot, filename="eda/plotting-results/ten-year-probability4.png")
