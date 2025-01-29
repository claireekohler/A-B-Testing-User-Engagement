## A/B Testing-User-Engagement

# Introduction

A/B testing is a data-driven experimentation method that provides valuable insights into user interactions, enabling businesses to optimize their UX design and digital marketing strategies. This process involves presenting two or more variations of a product or service feature—such as a web page, ad, or app component—to randomly selected user groups to determine which version performs better based on specific metrics. Common metrics include conversion rates, click-through rates, and user engagement. The variations are intentionally designed to be subtle yet impactful, allowing for an iterative progression in design without overwhelming users. A/B testing is an ongoing process, where continual, incremental adjustments are made to optimize user experience and enhance the overall impact of the service. By leveraging A/B testing, businesses can make informed decisions that contribute to sustained growth and user satisfaction.

To understand how to interpret A/B test results and its deployment, I found a dataset from an A/B Test to perform statistical analysis on (more about the methodology below). Based on statistical significance, I aimed to see if there was a performance difference between the new and old webpage using the conversion rate as well as its practical implications in deployment.


# Proposed Methodology

The overall A/B testing methodology:

Create Variations → Random Allocation → Testing → Data Collection → Comparison → Statistical Analysis → Implementation → Iterative Process

I focused on comparison and statistical analysis in my project and developed a project scope.

Performing A/B Test Analysis: 

Sanity Checks to validate data integrity
1. Remove flickers - respondents who switched between control and treatment groups
2. Sample ratio mismatch test (Chi-Squared) to check traffic is being split evenly

Statistical Tests 
1. Shapiro Wilk Test for Normality - critical assumption for statistical tests
2. Mann-Whitney U Test - nonparametric
   
Post-Test Computations
1. Power Analysis 

Assumptions 
1. Variations reflect subtle and iterative design progression that include all users
2. Variations were allocated randomly to visitors removing any sampling bias.

Deliverables
1. Writeup with the following sections: Introduction, Proposed Methodology, Analysis and Results, Conclusions and Further Considerations
2. Supplemental code

# Analysis and Results

Before conducting any statistical testing, I ensured my data was clean to minimize biases and maintain reliability. I removed "flickers," users who switched between the control and treatment groups during the experiment. Including these users could introduce bias, as exposure to both conditions undermines the validity of comparing distinct groups. Additionally, I dropped duplicates, users who appeared in the dataset multiple times, to prevent skewing the distribution.

The difference between the converted users in the control and treatment group was only about two hundred, so testing the null hypothesis that the conversion rates were the same using statistical methods, not just judgement was imperative.

<img width="759" alt="Screenshot 2025-01-28 at 16 40 21" src="https://github.com/user-attachments/assets/f7eaa925-1429-4b2c-825b-6fc6966f5023" />


Normality is a key assumption for many statistical tests, such as the Welch T-Test often used in A/B Testing. To test for normality in the data, I used the Shapiro-Wilk Test. The null hypothesis for this test states that the data is normally distributed. The test outputs a statistic and a p-value, and with an alpha significance level of 0.05, the resulting p-value was 0. This led me to reject the null hypothesis, concluding that the data distribution was not normal.

In A/B Testing, random and equal assignment of users to the control and treatment groups is critical to reduce selection bias. Although I did not perform the experiment myself, I assumed random allocation as a baseline. To validate this assumption, I tested for class imbalance using the Sample Ratio Mismatch (SRM) test. This involved comparing the observed ratio of users in the control and treatment groups against the expected 50-50 ratio using a chi-squared test. With a p-value above 0.05, there was no evidence of sample ratio mismatch, supporting the assumption of balanced group allocation.

To evaluate whether the treatment group achieved a higher conversion rate than the control group, I conducted the Mann-Whitney U Test. This nonparametric test is appropriate for non-normal data distributions. The null hypothesis for this test was that there is no significant difference in conversion rates between the two groups. After calculating the number of converted users in each group, I ran the test. With a p-value of 0.19 (greater than the 0.05 significance level), I failed to reject the null hypothesis, indicating no statistically significant difference in conversion rates between the control and treatment groups.

To ensure the integrity of my analysis and avoid p-hacking, the practice of selectively analyzing data to artificially achieve statistically significant results, I conducted a power analysis. Power measures the probability of correctly rejecting a false null hypothesis, and it depends on the effect size and sample size.

Effect size quantifies the standardized difference between two groups. In this case, the effect size was -0.005, an extremely small value indicating a negligible difference between the groups. With such a small effect size, the test's power was calculated to be only 0.04 with a simulated sample size of 1000. This low power means there is a very high likelihood of failing to detect a true difference if one exists. However, given the negligible effect size, the conclusion that the groups are not meaningfully different remains robust. Thus, even if the results were statistically significant, the difference would lack practical significance.


# Conclusion and Further Considerations

The key takeaway from this analysis is the importance of testing rather than making assumptions. A/B testing provides valuable insights, helping businesses make data-driven decisions that save time and resources by avoiding the implementation of ineffective design choices. Moving forward, a valuable next step would be to conduct A/B tests independently, adopting an iterative approach. This would involve experimenting with small design adjustments, statistically evaluating their impact, and refining the process to optimize user engagement.
