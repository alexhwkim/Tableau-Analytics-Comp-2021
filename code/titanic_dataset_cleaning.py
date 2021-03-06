import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
from sklearn.impute import SimpleImputer, MissingIndicator

df = pd.read_csv("Data Disaster.csv")
df.dtypes
df.head()

# Check Normality of Ages to determine what to backfill null values with
df_age_nonull = df[['Age']]
df_age_nonull = df_age_nonull.dropna()
stats.normaltest(df_age_nonull['Age'])

# Null Handling for Age, Embarked, Cabin
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].value_counts().index[0])
imputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value='Unknown')
df['Cabin'] = imputer.fit_transform(df[['Cabin']])

# Check Correlation between key variables
df_num = df[['Age','SibSp','Parch','Fare']]
df_cat = df[['Survived','Pclass','Sex','Ticket','Cabin','Embarked']]
sns.heatmap(df_num.corr())
colnames = ['Pclass',	'Sex', 'Cabin',	'Embarked']

def find_correlation(df, col_variable):
  df_pivtab = pd.pivot_table(df, index = 'Survived', columns = col_variable,
                      values = 'Ticket' ,aggfunc ='count')
  stat, p_value, dof, expected = chi2_contingency(df_pivtab)
  if np.isnan(p_value) == False:
    print("The p-value of the Chi-square test comparing", col_variable, "with Survived is:", p_value)

for columns in colnames:
  find_correlation(df_cat, columns)

# New df with a column for total number of (direct) relatives, and not survived
df_with_rel = df
total_relatives = df_with_rel["SibSp"] + df_with_rel["Parch"]
df_with_rel["TotRel"] = total_relatives
died = 1 - df_with_rel["Survived"]
df_with_rel["Died"] = died
df_with_rel.loc[:, ["Survived", "Died"]]
df_with_rel
