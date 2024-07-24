import pandas as pd

# Read the CSV file
df = pd.read_csv('test.csv')

# Select rows where the value in the 'column_name' is equal to 'some_value'
filtered_df = df[df['n'] == 1]

# Or, select rows where the value in 'column_name' is greater than 10
print(filtered_df)
