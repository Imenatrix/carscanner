from faker import Faker
from datetime import datetime
import mimesis
import pandas as pd

fake = Faker()

def generate_row():
    return {
        'titulo' : fake.catch_phrase(),
        'preco' : fake.random_int(min=10000, max=1000000),
        'estado' : fake.state_abbr(),
        'cidade' : fake.city(),
        'bairro' : fake.city(),
        'quilometragem' : fake.random_number(digits=6),
        'ano' : fake.year(),
        'combustivel' : fake.random_element(elements=('Flex', 'Gasolina', 'Diesel')),
        'cambio' : fake.random_element(elements=('Automático', 'Manual')),
        'url' : mimesis.Internet().uri(query_params_count=5),
        'data_publicacao' : fake.date_time(),
        'data_pesquisa' : fake.date_time()
    }

data = [generate_row() for x in range(43200)]
df = pd.DataFrame.from_dict(data, 'columns')
df.to_csv('sample.csv')
