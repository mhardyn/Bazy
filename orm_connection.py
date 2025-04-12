import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from alchemy_orm import Base

load_dotenv()

database_password = os.environ.get('DATABASE_PASSWORD')
suszi_login = 'mhardyn'
server = 'morfeusz.wszib.edu.pl'
driver = 'ODBC+Driver+17+for+SQL+Server'

# dialect+driver://username:password@host:port/database?dodatkowe_opcje_klucz_wartość
engine = create_engine(
    f'mssql+pyodbc://{suszi_login}:{database_password}@{server}/{suszi_login}?driver={driver}&Encrypt=no',
    echo=False
)

Session = sessionmaker(engine) # metoda z alchemy orm sessionmaker

if __name__ == '__main__': # zablokowanie żeby nie odpalić sobie tego w innym pliku
    # session = Session()
    # session.execute(CreateSchema('library_orm'))
    # session.commit()

    Base.metadata.create_all(engine)

