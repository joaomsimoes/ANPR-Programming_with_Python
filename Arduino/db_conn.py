import json
from sqlalchemy import create_engine


def db_connection():
    # faz conecção com a gase de dados e devolve o engine
    f = open("database.json")
    data = json.load(f)
    engine = create_engine(data['connection'])

    return engine


def query(prod=None, values=None):
    # liga à base de dados, executa a query e devolve os resultados
    engine = db_connection()
    connection = engine.raw_connection()
    cursor = connection.cursor()
    cursor.callproc(prod, values)
    results = list(cursor.fetchall())
    connection.commit()
    connection.close()

    return results

