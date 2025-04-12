import pyodbc
import os

#for driver in pyodbc.drivers():
#    print(driver)

#bedziemy sie laczyc do bazy ale najpierw musimy sobie zahaszowac haslo
#haslo mozemy sobie ustawic jako zmienna srodowiskowa : prawym klawiszem na plik python -> Run/Debug
# -> Modify Run configuration -> Environmental variables

#print(os.environ.get('DATABASE_PASSWORD'))

from dotenv import load_dotenv

load_dotenv()

#(os.environ.get('DATABASE_PASSWORD'))

#przypisujemy nasze haslo do zmiennej

database_password = os.environ.get('DATABASE_PASSWORD')
user = 'karkosz' #u nas akurat baza ma taka sama nazwe jak user
server = 'morfeusz.wszib.edu.pl'

#z dokumentacji :
#conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password')

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={user};'
    f'UID={user};'
    f'PWD={database_password};'
    'Encrypt=no'
)

connection=pyodbc.connect(connection_string)

if __name__ == '__main__':
    #wykonywanie komend w naszej bazie z poziomu pythona

    #connection.execute("CREATE TABLE users (id int identity, name varchar(255), age int) ")
    #connection.execute("INSERT INTO users (name, age) VALUES ('Anna', 37),('Mariusz',55)")
    #connection.commit()

    #cursor jest obiektem iterowalnym pythona i obiketem bazodanowym
    #to jest troche inny obiekt niz lista bo jak go iterujemy i skonczyly mu sie dane to juz ich kolejny raz nie wyswietli
    #gdy cursor dojdzie do konca to juz nic wiecej nie wyswietli co jest wazne dla performancu bazy

    cursor = connection.cursor()


    new_name = input('Podaj nowe imię: ')
    old_name = input('Podaj stare imie: ')
    # cursor.execute("UPDATE users SET name='{new_name}' where name='Ola'")
    # cursor.commit()

    #ponizej mamy ochrone przed atakiem sql incjection i tak powinnismy robic zawsze gdy pozwalamy
    #komus zmienic dane - uzywamy "prepare statement"
    cursor.execute("UPDATE users SET name=? where name=?", (new_name,old_name))
    cursor.commit()

    print(f'{cursor.rowcount} wierszy zmienionych')  #to zadziala tylko razem od orazu z updatem , puszczone drugi raz juz pokaze 0

    cursor.execute("SELECT * FROM users")

    #for row in cursor:
    #    print(row)

    #z zapytania sql do bazy otrzymujemy krotke ktora mozemy sobie podzielic

    # for user_id, name, age in cursor:
    #     print(user_id, name, age, sep='\n')

    # result = cursor.fetchall()
    # print(result)
    #
    # for row in result:
    #     print(row)
    #
    # for row in result:
    #     print(row)

    # result = cursor.fetchone()
    # print(result)
    # print(cursor.fetchone())
    # print(cursor.fetchone())

    #metody fetchall , fetchone, fathmany - to sa metody ktore operuja na kursorze dlatego za ktoryms razem dostajemy none

    # result = cursor.fetchmany(2)
    # print(result)

    # for row in cursor:
    #     print(row[0])

    #print(cursor.fetchval())

    #wazne jest tez zamykanie cursora i polaczenia do bazy
    #jesli w kazdym z miejsc gdzie mamy cursor wpisalibysmy slowko connection to:
    # - niektore metody nie zadzialaja np fetchall, fetchval, fetchmamny itp.

    # for row in connection.execute("SELECT * FROM users"):
    #     print(row)

    cursor.close()
    connection.close()