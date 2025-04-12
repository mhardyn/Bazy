#connection string z dokumentacji alchemy :
#dialect+driver://username:password@host:port/database?dodatkowe opcje klucz=wartosc

import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

database_password = os.environ.get('DATABASE_PASSWORD')
user = 'mhardyn' #u nas akurat baza ma taka sama nazwe jak user
server = 'morfeusz.wszib.edu.pl'
driver = 'ODBC+Driver+17+for+SQL+Server'

#tworzymy nasz engine ktore zawieraja poole polaczen do bazy , poki nie wykonamy polaczenia beda to tylko proxy polaczenia
engine = create_engine(
    f'mssql+pyodbc://{user}:{database_password}@{server}/{user}?driver={driver}&Encrypt=no',
    #echo=True
)

#connection = engine.connect()

#query = sqlalchemy.text("SELECT * from workers where pesel=:filter_pesel")
#result=connection.execute(query, {"filter_pesel": '111111'})
#print(result.fetchall())

#connection.close()

#musimy przekazac do sql alchemy jak wyglada nasza tabelka zeby wiedzial jak z niej korzystac

metadata = sqlalchemy.MetaData()
worker_table = sqlalchemy.Table('workers',metadata,
                 sqlalchemy.Column('pesel',sqlalchemy.String(11),primary_key=True),
                 sqlalchemy.Column('first_name',sqlalchemy.String(255), nullable=False),
                 sqlalchemy.Column('last_name',sqlalchemy.String(255), nullable=False),
                 sqlalchemy.Column('birthday',sqlalchemy.Date, nullable=False),
                 sqlalchemy.Column('address_id',sqlalchemy.Integer)
                 )

connection = engine.connect()

#query = sqlalchemy.text("SELECT * from workers where pesel=:filter_pesel")
query = sqlalchemy.select(worker_table)
result = connection.execute(query)
print(result.fetchall())

#kolumna wyswietli sie w reprezentacji stringowej
print(worker_table.columns.first_name)

#takie porownanie nie da nam true jakbsmy sie mogli spodziewac
#bo to jest typ binary expression
expression=worker_table.columns.first_name == 'Anna'
print(type(expression))

#zapytanie zeby otrzymac z tabeli tylko pierwsze imie

query = sqlalchemy.select(worker_table.c.first_name)
result = connection.execute(query)
print(result.fetchall())

query = sqlalchemy.select(worker_table.c.first_name,
                          worker_table.c.last_name)
result = connection.execute(query)
print(result.fetchall())

query = sqlalchemy.select(worker_table.c['first_name','last_name'])
result = connection.execute(query)
print(result.fetchall())

#limit/top - to jest dowod ze jestesmy niezalezni od dialektu
#bo limit jest w postgresie a top w mssql

query = sqlalchemy.select(worker_table).limit(2)
result = connection.execute(query)
print(result.fetchall())

#sortowanie

query = sqlalchemy.select(worker_table).order_by(worker_table.c.first_name.desc())
result = connection.execute(query)
print(result.fetchall())

query = sqlalchemy.select(worker_table).order_by(
    worker_table.c.first_name.desc(),
    worker_table.c.last_name)
result = connection.execute(query)
print(result.fetchall())

query = sqlalchemy.select(worker_table) \
    .order_by(worker_table.c.first_name.desc()) \
    .order_by (worker_table.c.last_name)\
    .limit(2) \
    .offset(1)
result = connection.execute(query)
print(result.fetchall())

#offset jest uzywany do pagowania, i musi byc uzyty razem z order by!

#Filtrowanie danych

query = sqlalchemy.select(worker_table) \
    .where (worker_table.c.pesel == '111111')
print(type(query))
print(query)
print(query.compile().params)
result = connection.execute(query)
print(result.fetchall())

#AND
query = sqlalchemy.select(worker_table) \
    .where ((worker_table.c.address_id > 1) & (worker_table.c.address_id <= 4))
result = connection.execute(query)
print(result.fetchall())

#AND2
query = sqlalchemy.select(worker_table) \
    .where (worker_table.c.address_id > 1)\
    .where (worker_table.c.address_id <= 4)
result = connection.execute(query)
print(result.fetchall())

#AND3
query = sqlalchemy.select(worker_table) \
    .where (sqlalchemy.and_(worker_table.c.address_id > 1, worker_table.c.address_id <= 4))
result = connection.execute(query)
print(result.fetchall())

#OR
query = sqlalchemy.select(worker_table) \
    .where ((worker_table.c.address_id > 1) | (worker_table.c.address_id <= 4))
result = connection.execute(query)
print(result.fetchall())

#OR2
query = sqlalchemy.select(worker_table) \
    .where (sqlalchemy.or_(worker_table.c.address_id > 1, worker_table.c.address_id <= 4))
result = connection.execute(query)
print(result.fetchall())

#w Alchemy jest tak samo jak w sql to znaczy operator logiczny and jest wazniejszy niz or
#imie Anna i Monika i adres id >2
query = sqlalchemy.select(worker_table) \
    .where ((worker_table.c.first_name == 'Anna') |
            (worker_table.c.first_name == 'Monika') &
            (worker_table.c.address_id > 2)
            )
result = connection.execute(query)
print(result.fetchall())

query = sqlalchemy.select(worker_table) \
    .where(
    sqlalchemy.and_(
        sqlalchemy.or_(worker_table.c.first_name == 'Anna',worker_table.c.first_name == 'Monika'),
        worker_table.c.address_id > 2
    )
)
result = connection.execute(query)
print(result.fetchall())

#jeszcze zrobimy zeby query korzystalo z in
query = sqlalchemy.select(worker_table) \
    .where(
    sqlalchemy.and_(
        worker_table.c.first_name.in_(['Anna','Monika']),
        worker_table.c.address_id > 2
    )
)
result = connection.execute(query)
print(result.fetchall())

#like
query = sqlalchemy.select(worker_table)\
    .where(worker_table.c.first_name.like('Ann%'))
result = connection.execute(query)
print(result.fetchall())

#kolejnosc metod jest niewazna, mozna dac sobie na przyklad order by na poczatku , on sobie na koncu zlozy zapytanie

#FUNKCJE AGREGUJACE

#count

query = sqlalchemy.select(sqlalchemy.func.count()).select_from(worker_table)
result = connection.execute(query)
print(result.scalar()) #scalar daje pierwsza kolumne z perwszego wiersza

#min/max
query = sqlalchemy.select(sqlalchemy.func.min(worker_table.c.address_id))
result = connection.execute(query)
print(result.scalar())

query = sqlalchemy.select(sqlalchemy.func.max(worker_table.c.birthday))
result = connection.execute(query)
print(result.scalar())

#group by
query = sqlalchemy.select(sqlalchemy.func.year(worker_table.c.birthday), sqlalchemy.func.count())\
    .group_by (sqlalchemy.func.year(worker_table.c.birthday))
result = connection.execute(query)
print(result.fetchall())

#having
query = sqlalchemy.select(sqlalchemy.func.year(worker_table.c.birthday), sqlalchemy.func.count())\
    .group_by (sqlalchemy.func.year(worker_table.c.birthday)) \
    .having (sqlalchemy.func.count() > 1)
result = connection.execute(query)
print(result.fetchall())

connection.close()

