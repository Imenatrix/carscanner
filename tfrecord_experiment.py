import tensorflow as tf
import pandas as pd

def bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  if isinstance(value, type(tf.constant(0))):
    value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def int64_list_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def encode_example(titulo, preco, estado, cidade, bairro, quilometragem, ano, combustivel, cambio, url, data_publicacao, data_pesquisa):
  feature = {
    'titulo' : bytes_feature(tf.io.serialize_tensor(titulo)),
    'preco' : float_feature(preco),
    'estado' : bytes_feature(tf.io.serialize_tensor(estado)),
    'cidade' : bytes_feature(tf.io.serialize_tensor(cidade)),
    'bairro' : bytes_feature(tf.io.serialize_tensor(bairro)),
    'quilometragem' : int64_feature(quilometragem),
    'ano' : int64_feature(ano),
    'combustivel' : bytes_feature(tf.io.serialize_tensor(combustivel)),
    'cambio' : bytes_feature(tf.io.serialize_tensor(cambio)),
    'url' : bytes_feature(tf.io.serialize_tensor(url)),
    'data_publicacao' : bytes_feature(tf.io.serialize_tensor(data_publicacao)),
    'data_pesquisa' : bytes_feature(tf.io.serialize_tensor(data_pesquisa)),
  }
  return tf.train.Example(features=tf.train.Features(feature=feature))

data = pd.read_csv('sample.csv', index_col=0)
data = data.to_numpy()

with tf.io.TFRecordWriter('records/0.tfrecord') as writer:
  for titulo, preco, estado, cidade, bairro, quilometragem, ano, combustivel, cambio, url, data_publicacao, data_pesquisa in data:
    example = encode_example(titulo, preco, estado, cidade, bairro, quilometragem, ano, combustivel, cambio, url, data_publicacao, data_pesquisa)
    writer.write(example.SerializeToString())