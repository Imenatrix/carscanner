import numpy as np
import pandas as pd

rows_per_minute = 30

rows_per_month = rows_per_minute * 60 * 24 * 30

years = 10
months = years * 12 + 1
time = np.arange(months + 1)

class Service:
    cost = 0
    title = ''
    unit = 'GB'
    bytes_per_entry = 0
    additional_costs = {}

    def storage_in_bytes(self, time):
        bytes_over_time = rows_per_month * self.bytes_per_entry
        return bytes_over_time * time
    
    def storage_in_unit(self, time):
        storage = self.storage_in_bytes(time)
        if self.unit == 'GB':
            return storage / (10 ** 9)
        elif self.unit == 'GiB':
            return storage / (1<<30)
        
    def total_storage(self, time):
        return self.storage_in_unit(time)

    def calc_aditional_costs(self):
        price = 0
        for cost in self.additional_costs.values():
            price += cost
        return price
    
    def calc_cost(self):
        storage = self.storage_in_unit(time)
        price = self.cost * storage
        return price + self.calc_aditional_costs()
    
    def estimate(self, cum):
        storage = self.total_storage(time)
        price = self.calc_cost()
        
        out = {}
        out[f'{self.title} - storage'] = storage
        out[f'{self.title} - price'] = price
        if cum:
            out[f'{self.title} - cumulative'] = np.cumsum(price)
        return out

    
class DynamoDB(Service):
    cost = 0.25
    title = 'dynamodb'
    bytes_per_entry = 450

class RDS(Service):
    cost = 0.115
    title = 'rds'
    bytes_per_entry = 330
    additional_costs = {
        'server' : 32.12,
        'proxy' : 21.90
    }

class CloudStorage(Service):
    cost = 0.03
    title = 'cloud storage'
    bytes_per_entry = 570
    unit = 'GiB'

class CloudSQL(Service):
    cost = 0.17
    unit = 'GiB'
    title = 'cloud sql'
    bytes_per_entry = 330
    additional_costs = {
        'server' : 49.31
    }

class Firestore(Service):
    cost = 0.18
    unit = 'GiB'
    title = 'firestore'
    bytes_per_entry = 450

class BigQuery(Service):
    cost_active = 0.023
    cost_inactive = 0.016
    bytes_per_entry = 330
    title = 'big query'
    unit = 'GiB'

    def storage_in_bytes(self, time):
        coiso = lambda x: x if x < 3 else 3
        coiso = np.vectorize(coiso)
        time_active = coiso(time)
        time_inactive = time - time_active
        bytes_over_time = rows_per_month * self.bytes_per_entry
        return {
            'active' : bytes_over_time * time_active,
            'inactive' : bytes_over_time * time_inactive
        }
    
    def storage_in_unit(self, time):
        storage = self.storage_in_bytes(time)
        if self.unit == 'GB':
            return {
                'active' : storage['active'] / (10 ** 9),
                'inactive' : storage['inactive'] / (10 ** 9)
            }
        elif self.unit == 'GiB':
            return {
                'active' : storage['active'] / (1<<30),
                'inactive' : storage['inactive'] / (1<<30)
            }

    def total_storage(self, time):
        storage = self.storage_in_unit(time)
        return storage['active'] + storage['inactive']
    
    def calc_cost(self):
        storage = self.storage_in_unit(time)
        price = self.cost_active * storage['active'] + self.cost_inactive * storage['inactive']
        return price + self.calc_aditional_costs()

services = [
    DynamoDB(),
    RDS(),
    CloudStorage(),
    CloudSQL(),
    Firestore(),
    BigQuery(),
]

def estimate(services, cum):
    out = {}
    for service in services:
        out = {**out, **service.estimate(cum)}
    return out

df = pd.DataFrame({
    'month' : time,
    **estimate(services, True)
})
df = df.round(2)

df.to_csv('coiso.csv')