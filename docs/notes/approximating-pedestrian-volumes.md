# Approximating Pedestrian Volumes

This writeup uses the guide from the National Bicycle & Pedestrian Documentation Project attached in the Agate & Mesa memo provided by SGM. It converts observed peak pedestrian volume into daily, weekly, monthly and annual pedestrian volumes using a variety of factors. 

# Mesa Street

## Observed data

|Peak duration|Total pedestrians|PPH|Start time|
|---|---|---|---|
|1-hour|6|6|2/19/2025 16:00|
|2-hour|6|3|2/19/2025 14:45|
|3-hour|7|2.3|2/19/2025 13:30|

Scaled for seasonality (factor of 1.9)

|Peak duration|Total pedestrians (adjusted)|PPH (adjusted)|Start time|
|---|---|---|---|
|1-hour|11.4|11.4|2/19/2025 16:00|
|2-hour|11.4|5.7|2/19/2025 14:45|
|3-hour|13.3|4.4|2/19/2025 13:30|

## Adjusting pedestrian volumes to annual units

The SGM mesa analysis has a reference on how to do this. I will be following it step by step using the given unadjusted AND adjusted pedestrian volumes.

The adjusted counts come from scaling the feb counts to may using the seasonal scalars and taking the average of the "Long winter" and "Moderate Climate" factors. So:

$$
6 \cdot \frac{\frac{1}{2} (0.11 + 0.08)}{\frac{1}{2} (0.03 + 0.07)} \\
= 6 \cdot \frac{0.095}{0.05} \\
= 6 \cdot 1.9 \\
= 11.4
$$

2/19/2025 was a thursday, so I'll use the weekday scaling. 

### Step 1. Scale hourly peak up

Multiply these counts by 1.05

- **Unadjusted:** 6 * 1.05 = 6.3 hourly users
- **Adjusted:** 11.4 * 1.05 = 11.97 hourly users

This scaling is done to adjust for pedestrians who use the intersection between 11pm and 6am. 

### Step 2. Calculate daily total

Use table 1 on page 12. Multi use path, october-march table at 1400. Gives 9%. 

- **Unadjusted:** 6.3 / 0.09 = 70 daily users
- **Adjusted:** 11.97 / 0.09 = 133 daily users

## Step 3. Calculate weekly volumes

Divide the daily counts by the daily adjustment factors. Thursday has a factor of 12%.

- **Unadjusted:** 70 / 0.12 = 583.33 weekly users
- **Adjusted:** 133 / 0.12 = 1108.33 weekly users

### Step 4. Convert to monthly volumes

Multiply weekly volume by average number of weeks in a month (4.33).

- **Unadjusted:** 583.33 * 4.33 = 2525.82 monthly users (Feb)
- **Adjusted:** 1108.33 * 4.33 = 4797.64 monthly users (Scaled to May)

### Step 5. Convert to annual totals

Divide the monthly volume by the month factor in table 3. SGM used the average of the long winter and moderate climate scalars. 

For Feb I'll take the average of the climate regions to be consistent with SGM. So I will divide by 0.05. For the adjusted I'll take the average of the May values. So 0.095.

- **Unadjusted:** 2525.82 / 0.05 = 50514.4 annual users
- **Adjusted:** 4797.64 / 0.095 = 50501.4 annual users.

Both values end up at around 50.5 thousand pedestrians per year. 

**NOTE** that this difference is due to rounding. Performing these calculations programmatically results in both reaching an expected annual volume of **50,516.67** pedestrians. 

Code output:

```
> hourly_to_annual(6, hour_factor=0.09, day_factor = 0.12, month_factor = 0.05)
Hourly volume: 6
Step 1. Adjusting for evening pedestrian traffic ---
Hourly volume adjusted: 6.3
Step 2. Estimating daily volume ---
Daily volume: 70
Step 3. Estimating weekly volume ---
Weekly volume: 583.333333333333
Step 4. Estimating monthly volume ---
Monthly volume: 2525.83333333333
Step 5. Estimating annual volume ---
Annual volume: 50516.6666666667
[1] 50516.67
> hourly_to_annual(11.4, hour_factor=0.09, day_factor = 0.12, month_factor = 0.095)
Hourly volume: 11.4
Step 1. Adjusting for evening pedestrian traffic ---
Hourly volume adjusted: 11.97
Step 2. Estimating daily volume ---
Daily volume: 133
Step 3. Estimating weekly volume ---
Weekly volume: 1108.33333333333
Step 4. Estimating monthly volume ---
Monthly volume: 4799.08333333333
Step 5. Estimating annual volume ---
Annual volume: 50516.6666666667
[1] 50516.67
```

# 4th street

## Observed data

These are volumes per hour in the given intervals. So not cumulative. So the first row is 7 people/hour. As it is the highest it is what we will be using. 

|Interval|Volume (pph)|
|---|---|
|2/19/2025 15:45|7|
|2/19/2025 14:00|6|
|2/19/2025 13:00|3|
|2/19/2025 11:45|2|

This data was collected on the same day as the Mesa observations, so the same day/month factors can be used. The only difference in this calculation is a change to the hour factor. 

Looking at the row for 15:00 on a multi-use path, we get an hourly factor of 0.10. From this we run the same script as above to get the following results. 

```
Estimating pedestrian volume for 4th and Agate
Hourly volume: 7
Step 1. Adjusting for evening pedestrian traffic ---
Hourly volume adjusted: 7.35
Step 2. Estimating daily volume ---
Daily volume: 73.5
Step 3. Estimating weekly volume ---
Weekly volume: 612.5
Step 4. Estimating monthly volume ---
Monthly volume: 2652.125
Step 5. Estimating annual volume ---
Annual volume: 53042.5
```