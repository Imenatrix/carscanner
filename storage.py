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

def aws_dynamo(gb):
    price_per_gb = 0.25
    price = gb * price_per_gb
    price_cum = np.cumsum(price)
    return {
        'dynamodb' : price,
        'dynamodb - cumulative' : price_cum
    }

def cloud_storage(gib):
    price_per_gib = 0.03
    price = gib * price_per_gib
    price_cum = np.cumsum(price)
    return {
        'cloud storage' : price,
        'cloud storage - cumulative' : price_cum
    }

def cloud_sql(gib):
    price_per_gib = 0.17
    instance_cost = 49.31
    price = gib * price_per_gib + instance_cost
    price_cum = np.cumsum(price)
    return {
        'cloud sql' : price,
        'cloud sql - cumulative' : price_cum
    }

def aws_rds(gb):
    price_per_gb = 0.115
    instance_cost = 32.12
    proxy_cost = 21.90
    price = gb * price_per_gb + instance_cost + proxy_cost
    price_cum = np.cumsum(price)
    return {
        'rds' : price,
        'rds - cumulative' : price_cum
    }

df = pd.DataFrame({
    'month' : time_array,
    'bytes' : bytes_array,
    'gigabytes' : gib_array,
    **aws_dynamo(gb_array),
    **aws_rds(gb_array),
    **cloud_storage(gib_array),
    **cloud_sql(gib_array),
})
df = df.round(2)

df.to_csv('coiso.csv')