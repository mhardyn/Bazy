import os

from dotenv import load_dotenv
from sqlalchemy import *
from sqlalchemy import create_engine

load_dotenv()

database_password = os.environ.get('DATABASE_PASSWORD')
suszi_login = 'mhardyn'
server = 'morfeusz.wszib.edu.pl'
driver = 'ODBC+Driver+17+for+SQL+Server'

# dialect+driver://username:password@host:port/database?dodtkowe_opcje_klucz_wartość
engine = create_engine(
    f'mssql+pyodbc://{suszi_login}:{database_password}@{server}/{suszi_login}?driver={driver}&Encrypt=no',
    echo=False
)

metadata = MetaData()

worker_table = Table('workers', metadata,
                     Column('pesel', String(11), primary_key=True),
                     Column('first_name', String(255), nullable=False),
                     Column('last_name', String(255), nullable=False),
                     Column('birthday', Date, nullable=False),
                     Column('address_id', Integer, ForeignKey('address.address_id')),
                     )

address_table = Table('address', metadata,
                    Column('address_id', Integer, primary_key=True, autoincrement=True),
                     Column('country', String(255), nullable=False),
                     Column('city', String(255), nullable=False),
                     Column('street', String(255), nullable=False),
                     Column('postal_code', String(25), nullable=False),
                     )

connection = engine.connect()

if __name__ == '__main__':

    # Złączenie INNER
    query = select(worker_table.join(address_table))
    result = connection.execute(query)
    print(worker_table.join(address_table))
    print(result.fetchall())

    # Złączenie + konkretne kolumny np. pesel i państwo

    query = (select(worker_table.c.pesel, address_table.c.country) \
             .select_from(worker_table.join(address_table)))
    result = connection.execute(query)
    print(result.all())

    # Złączenie + konkretne kolumny np. pesel i państwo DRUGI SPOSÓB

    query = (select(worker_table.c.pesel, address_table.c.country) \
             .join_from(worker_table, address_table))
    result = connection.execute(query)
    print(result.all())

    # Złączenie + konkretne kolumny np. pesel i państwo TRZECI SPOSÓB

    query = (select(worker_table.c.pesel, address_table.c.country) \
             .join(address_table))
    result = connection.execute(query)
    print(result.all())

    # Złączenie + ON

    query = select(worker_table.c.pesel, address_table.c.country) \
             .join(worker_table, worker_table.c.address_id == address_table.c.address_id)
    result = connection.execute(query)
    print(result.all())

    # Potwierdzenie, że złączenie domyślne to INNER

    query = select(worker_table, address_table.c.country) \
             .join(worker_table) \
             .where(worker_table.c.last_name == 'Kozłowski')
    result = connection.execute(query)
    print(result.all())

    # Alias

    w = worker_table.alias()
    a = address_table.alias()

    query = select(w, a.c.country) \
             .join(w)
    result = connection.execute(query)
    print(result.all())

    # Left join

    query = select(worker_table, address_table.c.country) \
        .join(address_table, isouter=True) \
        .where(worker_table.c.last_name == 'Kozłowski')
    result = connection.execute(query)
    print(result.all())

    # Full combo

    query = select(func.year(worker_table.c.birthday), func.count().label('Liczba urodzonych w danym roku w Krakowie')) \
        .join(address_table) \
        .where(address_table.c.city == 'Kraków') \
        .group_by(func.year(worker_table.c.birthday)) \
        .order_by(Column('Liczba urodzonych w danym roku w Krakowie').desc()) \
        .having(func.count() > 1)
    result = connection.execute(query)
    print(result.all())

    # Insert
    # insert_sql = insert(address_table) \
    #     .values(country='Polska', city='Kraków', street='Aleja Kijowska 15', postal_code='30-387')
    # connection.execute(insert_sql)
    # connection.commit()
    #
    # insert_many = insert(worker_table)
    # connection.execute(insert_many, [
    #     {'pesel': '11111111111', 'first_name': 'Nowy', 'last_name': 'Jeden', 'birthday': '2000-01-01', 'address_id': 10},
    #     {'pesel': '22222222222', 'first_name': 'Nowy', 'last_name': 'Dwa', 'birthday': '2000-01-01', 'address_id': 10},
    # ])
    #
    # connection.commit()

    # Update

    update_sql = update(worker_table).values(first_name='Zmienione').where(worker_table.c.address_id == 11)
    connection.execute(update_sql)
    connection.commit()

    # Delete

    delete_sql = delete(worker_table).where(worker_table.c.address_id == 10)
    connection.execute(delete_sql)
    connection.commit()

    # Insert
    insert_sql = insert(address_table) \
        .values(country='Polska', city='Kraków', street='Aleja Kijowska 15', postal_code='30-387')
    result = connection.execute(insert_sql)

    new_address_id = result.inserted_primary_key[0]

    insert_many = insert(worker_table)
    connection.execute(insert_many, [
        {'pesel': '11111111111', 'first_name': 'Nowy', 'last_name': 'Jeden', 'birthday': '2000-01-01', 'address_id': new_address_id},
        {'pesel': '22222222222', 'first_name': 'Nowy', 'last_name': 'Dwa', 'birthday': '2000-01-01', 'address_id': new_address_id},
    ])

    connection.commit()

    



