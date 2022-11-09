import sqlite3
db_file = 'data.db'

def db_connection_start():
  connection = None
  try:
    connection = sqlite3.connect(db_file)
    print('\n[CONEXÃO ESTABELECIDA COM O BANCO DE DADOS]')
    
  except sqlite3.Error as e:
    print('\n[ERRO NA CONEXÃO COM O BANCO DE DADOS]', e)

  return connection 

def db_connection_close(connection):
  if connection:
    connection.close()

def db_table_create(connection, SQL_create_table):
  try:
    cursor = connection.cursor()
    cursor.execute(SQL_create_table)
    print('[TABELA CRIADA COM SUCESSO]')
  except sqlite3.Error as e:
    print('[ERRO AO CRIAR TABELA]', e)
    
def db_table_clear(connection, SQL_clear_table):
  try:
    cursor = connection.cursor()
    cursor.execute(SQL_clear_table)
    print('[DADOS REMOVIDOS]')
  except sqlite3.Error as e:
    print('[ERRO AO LIMPAR TABELA]', e)
    


def db_user_insert(connection, SQL_insert_user):
  try:
    cursor = connection.cursor()
    cursor.execute(SQL_insert_user)
    connection.commit()
    print('[DADOS INSERIDOS COM SUCESSO]')
  except sqlite3.Error as e:
    print('[ERRO AO INSERIR DADOS]', e)

def db_search_user(connection, SQL_search_user):
  user = None
  try:
    cursor = connection.cursor()
    cursor.execute(SQL_search_user)
    user = cursor.fetchall()
    print("[DADOS BUSCADOS]")
  except sqlite3.Error as e:
    print('[ERRO AO BUSCAR:] ', e)
  finally:
    return user

def db_search_events(connection, SQL_search_events):
  try:
    cursor = connection.cursor()
    events = cursor.execute(SQL_search_events)
    print("[EVENTOS BUSCADOS]")

    for event in events:
      print(f'(EVENT 0:) {event[0]} | (EVENT 1:) {event[1]} | (EVENT 2:) {event[2]}')
  except sqlite3.Error as e:
    print("[ERRO AO BUSCAR EVENTO:] ", e)
  # finally:
  #   return event
    