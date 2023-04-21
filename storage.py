import numpy as np
import pandas as pd

bytes_per_row = 2303
rows_per_minute = 30

rows_per_month = rows_per_minute * 60 * 24 * 30

bytes_per_month = rows_per_month * bytes_per_row

years = 10
months = years * 12 + 1

time_array = np.arange(months + 1)
bytes_array = time_array * bytes_per_month
gb_array = bytes_array / (10 ** 9)
gib_array = bytes_array / (1<<30)

price_per_gb_aws_dynamo = 0.25
price_per_gib_cloud_storage = 0.02
price_per_gib_cloud_sql = 0.17
price_per_gb_aws_rds = 0.115
aws_dynamo_price_array = price_per_gb_aws_dynamo * gb_array
cloud_storage_price_array = price_per_gib_cloud_storage * gib_array
cloud_sql_price_array = price_per_gib_cloud_sql * gib_array + 49.31
aws_rds_price_array = price_per_gb_aws_rds * gb_array + 32.12 + 21.90

df = pd.DataFrame({
    'month' : time_array,
    'bytes' : bytes_array,
    'gigabytes' : gib_array,
    'dynamodb' : aws_dynamo_price_array,
    'dynamodb - cumulative' : np.cumsum(aws_dynamo_price_array),
    'cloud storage' : cloud_storage_price_array,
    'cloud storage - cumulative' : np.cumsum(cloud_storage_price_array),
    'cloud sql' : cloud_sql_price_array,
    'cloud sql - cumulative' : np.cumsum(cloud_sql_price_array),
    'aws rds' : aws_rds_price_array,
    'aws rds - cumulative' : np.cumsum(aws_rds_price_array)
})
df = df.round(2)

df.to_csv('coiso.csv')