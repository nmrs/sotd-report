import pandas as pd
from datetime import datetime, timedelta
import calendar

# Your original DataFrame
data = {'Date': ['1/1/24', '1/1/24', '1/5/24', '1/2/24', '1/5/24', '1/28/24'],
        'User': ['John', 'John', 'John', 'Bill', 'Bill', 'Bill'],
        'Comment': ['Hi there', 'No', "What's up?", 'Hey', 'Nothing', 'See you later']}

df = pd.DataFrame(data)

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Determine the last day of the month dynamically
last_day_of_month = calendar.monthrange(df['Date'].iloc[0].year, df['Date'].iloc[0].month)[1]

# Create a DataFrame with all days of the month for each user
date_range = pd.date_range(start=f'1/1/{df["Date"].iloc[0].year}', end=f'{df["Date"].iloc[0].month}/{last_day_of_month}/{df["Date"].iloc[0].year}', freq='D')
users = df['User'].unique()
date_user_df = pd.DataFrame([(date, user) for date in date_range for user in users], columns=['Date', 'User'])

# Merge the original DataFrame with the new one
merged_df = pd.merge(date_user_df, df, on=['Date', 'User'], how='left')

# Count the total number of comments per user
total_comments = df.groupby('User')['Comment'].count()

# Count the number of days without comments for each user
no_comment_days = merged_df[merged_df['Comment'].isnull()]
days_without_comments = no_comment_days.groupby('User')['Date'].count()

# Combine the results into a single DataFrame
result_df = pd.DataFrame({'Total_Comments': total_comments, 'Days_Without_Comments': days_without_comments}).fillna(0)

print(result_df)