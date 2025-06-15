# Loan Prediction – Data Preparation

## Part: Data Cleaning and Feature Engineering

My section of the project focuses on preparing the loan dataset for machine learning.
For a detailed explanation of the data issue and handling process, please see the Word document.


### Tasks Completed:
- Loaded and inspected the dataset
- Handled missing values using statistical methods (mean, median, mode)
- Removed duplicate rows
- Visualized outliers
- Performed exploratory data analysis on categorical and numerical features
- Created new features (e.g., Total_Income)
- Applied log transformations to reduce skewness
- Removed columns that were no longer useful or repeated the same information
- Encoded categorical variables using Label Encoding

### Model Suggestions:

Based on the cleaned and engineered dataset, the following classification models are recommended:

- **Logistic Regression** – a simple model to try first and fit this data
- **Decision Tree** – makes decisions step by step, like a flowchart
- **Random Forest** –  gives better results by using many decision trees together

To evaluate these models properly, cross-validation should be applied in the modeling step  for more reliability to ensure results are stable and not dependent on a single train-test split.
