import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

df = pd.read_csv('customer_shopping_behavior.csv')
df.head()
df.info()
df.describe(include='all')
df.isnull().sum()
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.isnull().sum()
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

#Feature Engineering
#create a column age_group
labels = ['Young Adult', 'Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)
df[['age','age_group']].head(10)

#create column purchase_freq_days
freq_mapping = {
    'Fortnightly':14,
    'Monthly':30,
    'Weekly':7,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90,
    'Quarterly':90
}
df['purchase_freq_days'] = df['frequency_of_purchases'].map(freq_mapping)
df[['purchase_freq_days','frequency_of_purchases']].head(10)
df[['discount_applied','promo_code_used']].head(10)
(df['discount_applied'] == df['promo_code_used']).all()
df = df.drop('promo_code_used',axis=1)



# step 1: connect to MySQL
username = "root"
password = "Sujay@0903"
host = "localhost"
port = "3306"
database = "customer_behaviour"

# URL-encode the password
encoded_password = quote_plus(password)

engine = create_engine(f'mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}')

#step 2: Load dataframe into MySQL
table_name = "customer"
df.to_sql(table_name, engine, if_exists='replace', index=False)
print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")