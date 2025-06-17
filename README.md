# Loan Prediction – Data cleaning and preprocessing
## name:
albatoul_284575_c2

### Data Cleaning and Feature Engineering

My section of the project focuse on preparing the loan dataset for machine learning modeling.
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

### Main Features Affecting Loan Status (based on analysis)

1. **Credit_History** – Strongest predictor
2. **Education** – Graduates more likely to be approved
3. **Married** – Combined incomes increase approval rate
4. **Log_Total_Income** – Higher total income improves approval chances
5. **Log_LoanAmount** – Normalized loan size is relevant

### Model Suggestions:

Based on the cleaned and engineered dataset, the following classification models are recommended:

- **Logistic Regression** – a simple model to try first and fit this data
- **Decision Tree** – makes decisions step by step, like a flowchart
- **Random Forest** –  gives better results by using many decision trees together

To evaluate these models properly, cross-validation should be applied in the modeling step  for more reliability to ensure results are stable and not dependent on a single train-test split but the decission for .
