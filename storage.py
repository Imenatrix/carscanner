import numpy as np
import pandas as pd

bytes_per_row = 2303
rows_per_minute = 30

rows_per_month = rows_per_minute * 60 * 24 * 30
bytes_per_month = rows_per_month * bytes_per_row

years = 10
months = years * 12 + 1
time = np.arange(months + 1)

bytes_array = time * bytes_per_month
gb_array = bytes_array / (10 ** 9)
gib_array = bytes_array / (1<<30)

def gb(t):
    return gb_array

def gib(t):
    return gib_array

services = {
    'dynamodb' : {
        'cost' : 0.25,
        'storage' : gb,
    },
    'rds' : {
        'cost' : 0.115,
        'storage' : gb,
        'additional_costs' : {
            'server' : 32.12,
            'proxy' : 21.90
        }
    },
    'cloud_storage' : {
        'cost' : 0.03,
        'storage' : gib,
    },
    'cloud sql' : {
        'cost' : 0.17,
        'storage' : gib,
        'additional_costs' : {
            'server' : 49.31
        }
    },
    'firestore' : {
        'cost' : '0.18',
        'storage' : gb,
    }
}

def estimate(services, cum):
    out = {}
    for title, service in services.items():
        out_service = estimate_service(title, service, cum)
        out = {**out, **out_service}
    return out

def estimate_service(title, service, cum):
    price = service['cost'] * service['storage'](time)
    if 'additional_costs' in service:
        for cost in service['additional_costs'].values():
            price += cost
    
    out = {}
    out[title] = price
    if cum:
        out[f'{title} - cumulative'] = np.cumsum(price)
    return out

df = pd.DataFrame({
    'month' : time,
    'bytes' : bytes_array,
    'gigabytes' : gib_array,
    **estimate(services, True)
})
df = df.round(2)

df.to_csv('coiso.csv')