import pandas as pd
import sqlalchemy
url = sqlalchemy.engine.URL.create(
    drivername='mysql',
    username='user',
    password='imablu3b@nana',
    host='localhost',
    port=3306,
    database='carscanner'
)
engine = sqlalchemy.create_engine(url)

data = pd.read_csv('sample.csv', index_col=0)
data.to_sql('anuncios', engine, if_exists='append', index=False)