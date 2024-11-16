import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib_inline
random.seed(42)
from statsmodels.stats import power as pwr
from statsmodels.stats.proportion import proportion_effectsize
from scipy.stats import shapiro, chisquare, mannwhitneyu

#Read data
df = pd.read_csv('ab_data.csv')

df.info()
df.head()

#Count number in control and treatment 
df.groupby(['group', 'converted']).agg('count')

#Drop flickers
df.drop(df.query("group == 'control' and landing_page == 'new_page'").index, inplace=True)
df.drop(df.query("group == 'treatment' and landing_page == 'old_page'").index, inplace=True)

#Drop duplicates
df.drop_duplicates(['user_id'], keep=False)

#EDA
df.groupby(['group']).agg({'converted':['sum','count','mean']})
#Control and Treatment count about the same

print(df.dtypes)


#Shapiro-Wilk Test for normality
statistic, p_value = shapiro(df['converted'])
print('Shapiro-Wilk Test:')
print('Statistic:', statistic)
print('p-value:', p_value)

alpha = 0.05
#accept null hypothesis
if p_value > alpha:
    print('Data is normally distributed')
else:
#reject null hypothesis
    print('Data is not normally distributed')

#Sample Ratio Mismatch Test to test if the difference
#is statistically significant

observed_ratio = df['group'].value_counts(normalize=True)
expected_ratio = {'control': 0.5,'treatment': 0.5}

for group, ratio in observed_ratio.items():
    print(f"Group {group}: Observed {ratio:.2f}, Expected {expected_ratio[group]:.2f}")

observed_counts = df['group'].value_counts().values

print(observed_counts)

n_treatment = observed_counts[0]
n_control = observed_counts[1]

expected_counts = [len(df) * ratio for ratio in expected_ratio.values()]

chi2_stat, p_value = chisquare(observed_counts, expected_counts)

print(f"Chi-Square Statistic: {chi2_stat:.2f}, P-value: {p_value:.2f}")

if p_value < 0.05:
    print("SRM detected!")
else:
    print("No evidence of SRM.")

#Mann-Whitney U Test - non-parametric test
convert_control = df[df['group'] == 'control']['converted']
convert_treatment = df[df['group'] == 'treatment']['converted']

stat, p_value = mannwhitneyu(convert_control, convert_treatment, alternative='two-sided')
print(f"Mann-Whitney U Test, U statistic: {stat:.2f}, P-value: {p_value:.2f}")

alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant difference between the control and treatment groups.")
else:
    print("Fail to reject the null hypothesis: No significant difference between the control and treatment groups.")

#Post-Test Computations

#Power Analysis
p_control = df[['group','converted']].query("group == 'control'")['converted'].mean()
p_treatment = df[['group','converted']].query("group == 'treatment'")['converted'].mean()
p_diff = p_control - p_treatment

print('p_control:\t{}\np_treatment:\t{}\np_diff:\t{}'.format(p_control, p_treatment, p_diff))

#Calculate Effect Size
effect_size = proportion_effectsize(p_treatment, p_control)
ratio = n_treatment/n_control

print(effect_size)

#Effect size nearly negligible
#Likely no difference between the two groups.

def mann_whitney_power_simulation(effect_size=effect_size, alpha=0.05, n1=30, n2=30, n_simulations=1000):
    significant_results = 0
    
    # Run the simulations
    for _ in range(n_simulations):
        # Generate two random samples from normal distributions with a specified effect size
        group1 = np.random.normal(loc=0, scale=1, size=n1)
        group2 = np.random.normal(loc=effect_size, scale=1, size=n2)
        
        # Perform the Mann-Whitney U test
        stat, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
        
        # Check if the result is significant
        if p_value < alpha:
            significant_results += 1
    
    # Calculate power as the proportion of significant results
    power = significant_results / n_simulations
    return power

power = mann_whitney_power_simulation(effect_size=effect_size, alpha = 0.05, n1=30,n2=30,n_simulations=1000)
print(power)

#Very small power because there is a very small effect 