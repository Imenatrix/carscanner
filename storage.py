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


df = pd.DataFrame({
    'month' : time_array,
    'bytes' : bytes_array,
    'gigabytes' : gib_array,
})
df = df.round(2)

df.to_csv('coiso.csv')