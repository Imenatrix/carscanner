import numpy as np
import pandas as pd

rows_per_minute = 30

rows_per_month = rows_per_minute * 60 * 24 * 30

years = 10
months = years * 12 + 1
time = np.arange(months + 1)

def sql(time):
    bytes_per_row = 330
    bytes_over_time = rows_per_month * bytes_per_row
    return bytes_over_time * time

def firebase(time):
    bytes_per_row = 450
    bytes_over_time = rows_per_month * bytes_per_row
    return bytes_over_time * time

def tfrecord(time):
    bytes_per_row = 570
    bytes_over_time = rows_per_month * bytes_per_row
    return bytes_over_time * time

def big_query(time):
    coiso = lambda x: x if x < 3 else 3
    coiso = np.vectorize(coiso)
    time_active = coiso(time)
    time_inactive = time - time_active
    bytes_per_row = 330
    bytes_over_time = rows_per_month * bytes_per_row
    return {
        'active' : bytes_over_time * time_active / (1<<30),
        'inactive' : bytes_over_time * time_inactive / (1<<30)
    }


def gb(bytes_array):
    return bytes_array / (10 ** 9)

def gib(bytes_array):
    return bytes_array / (1<<30)

def sql_gb(time):
    return gb(sql(time))

def sql_gib(time):
    return gib(sql(time))

services = {
    'dynamodb' : {
        'cost' : 0.25,
        'storage' : lambda time: gb(firebase(time)),
    },
    'rds' : {
        'cost' : 0.115,
        'storage' : sql_gb,
        'additional_costs' : {
            'server' : 32.12,
            'proxy' : 21.90
        }
    },
    'cloud_storage' : {
        'cost' : 0.03,
        'storage' : lambda time: gib(tfrecord(time)),
    },
    'cloud sql' : {
        'cost' : 0.17,
        'storage' : sql_gb,
        'additional_costs' : {
            'server' : 49.31
        }
    },
    'firestore' : {
        'cost' : 0.18,
        'storage' : lambda time: gib(firebase(time)),
    }
}

big_query_service = {
    'cost_active' : 0.023,
    'cost_inactive' : 0.016,
    'storage' : big_query
}

def estimate(services, cum):
    out = {}
    for title, service in services.items():
        out_service = estimate_service(title, service, cum)
        out = {**out, **out_service}
    return out

def estimate_service(title, service, cum):
    storage = service['storage'](time)
    price = service['cost'] * storage
    if 'additional_costs' in service:
        for cost in service['additional_costs'].values():
            price += cost
    
    out = {}
    out[f'{title} - storage'] = storage
    out[f'{title} - price'] = price
    if cum:
        out[f'{title} - cumulative'] = np.cumsum(price)
    return out

def estimate_big_query(title, service, cum):
    storage = service['storage'](time)
    price = service['cost_active'] * storage['active'] + service['cost_inactive'] * storage['inactive']
    if 'additional_costs' in service:
        for cost in service['additional_costs'].values():
            price += cost
    
    out = {}
    out[f'{title} - storage'] = storage['active'] + storage['inactive']
    out[f'{title} - price'] = price
    if cum:
        out[f'{title} - cumulative'] = np.cumsum(price)
    return out

df = pd.DataFrame({
    'month' : time,
    **estimate(services, True),
    **estimate_big_query('big query', big_query_service, True)
})
df = df.round(2)

df.to_csv('coiso.csv')