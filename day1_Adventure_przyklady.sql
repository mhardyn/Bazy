USE mhardyn

--zeby sprawdzic w jakiej jestem bazie
select db_name()
select schema_name()

create table Customers
(
    customer_id INT PRIMARY KEY,
    first_name  VARCHAR(255) NOT NULL,
    birth_date  DATE         NOT NULL,
    WrongColumnName DATE
)


drop table customers

alter table Customers drop column WrongColumnName

select * from Customers

--uwaga tu pycharm podkresla bo trzeba pamietac ze jak do istniejacej tabelki
--dodajemy kolumne z contraintem not null to powinnismy dodac wartosc domyslna
--gdyby znalazly sie juz tam jakies rekordy
alter table Customers add new_column INT NOT NULL

--procedura skladowana do zmiany nazwy kolumny --tylko w mssql
exec sp_rename 'Customers.new_column', 'changed_column', 'COLUMN'

alter table Customers drop column changed_column

--wpuszczamy dane

INSERT INTO Customers(customer_id, first_name, birth_date)
VALUES (1, 'Anna', '2001-01-01')

INSERT INTO Customers(customer_id, first_name, birth_date)
VALUES (2, 'Mihal', '2001-01-01')

DELETE FROM Customers --leci wiersz po wierszu
TRUNCATE TABLE Customers
--truncate jest szybszy, czysci cale dane , resetuje sekwencje (autoinkrementacje)

CREATE TABLE Test (
    ID INT PRIMARY KEY,
    col2 INT NULL,
    col3 INT NOT NULL
)

insert into Test (ID, col2, col3)
values (1,1,1)

insert into Test (ID,col3)
values (3,1)

create schema sqltest

CREATE TABLE Sqltest.Test (
    ID INT PRIMARY KEY,
    col2 INT NULL,
    col3 INT NOT NULL
)
--nie mozna sie przelaczyc na inny schemat, zawsze jestesmy dbo i trzeba z poziomu usera dodawac nazwe schematu
-- przed jego obiekty

drop table Customers

-- dodajemy IDENTITY co da nam autoinkrementacje na kolunie customer_id
create table Customers
(
    customer_id INT PRIMARY KEY IDENTITY,
    first_name  VARCHAR(255) NOT NULL,
    birth_date  DATE         NOT NULL
)

INSERT INTO Customers(first_name, birth_date)
VALUES ('Anna', '2001-01-01')

INSERT INTO Customers(first_name, birth_date)
VALUES ('Mihal', '2001-01-01')

delete from Customers where customer_id=2

TRUNCATE TABLE Customers

create table Orders (
    order_id INT PRIMARY KEY IDENTITY,
    order_date DATE NOT NULL,
    customer_id INT
)

insert into Orders (order_date, customer_id)
values ('2000-01-01',1)

insert into Orders (order_date, customer_id)
values (getdate(), 10)

drop table Orders

--zakladam klucz obcy
create table Orders (
    order_id INT PRIMARY KEY IDENTITY,
    order_date DATE NOT NULL,
    customer_id INT FOREIGN KEY REFERENCES Customers(customer_id)
)

insert into Orders (order_date, customer_id)
values ('2000-01-01',1)

insert into Orders (order_date, customer_id)
values (getdate(), 10)

drop table Orders


create table Orders (
    order_id INT PRIMARY KEY IDENTITY,
    order_date DATE NOT NULL,
    customer_id INT
)

--dodanie klucza obcego po utworzeniu tabeli
--przy czym oczywiscie nazwa kolumny customer_id nie musi byc taka sama
--nazwa klucza obcego jest nam potrzebna zeby ewentualnie pozniej go usunac

alter table Orders
    add constraint FK_Orders_Customers_customer_id FOREIGN KEY(customer_id)
    references Customers(customer_id)

alter table Orders drop constraint FK_Orders_Customers_customer_id

delete from Orders where customer_id=10

--to nam zalozy klucz z takim warunkiem ze podczas usuwania rekordow z primary key bedzie tez usuwany jego rekord
--z tabeli orders

alter table Orders
    add constraint FK_Orders_Customers_customer_id FOREIGN KEY(customer_id)
    references Customers(customer_id)
        ON DELETE CASCADE

--teraz w momencie usuniecia rekordu z Customes, w orders klucz obcy zostanie ustawiony jako NULL

alter table Orders
    add constraint FK_Orders_Customers_customer_id FOREIGN KEY(customer_id)
    references Customers(customer_id)
        ON DELETE SET NULL

create table Customers
(
    customer_id INT PRIMARY KEY IDENTITY,
    first_name  VARCHAR(255) NOT NULL,
    birth_date  DATE         NOT NULL, DEFAULT Getdate()
)


--dodawanie wartosci defaultowej
ALTER TABLE Customers
    add constraint DF_birth_date DEFAULT GETDATE() FOR birth_date

insert into Customers (first_name, birth_date)
values ('Jan',DEFAULT)

--sprawdzenia - check
--np sprawdzamy czy data urodzenia bedzie z przyszlosci

ALTER TABLE Customers
    add constraint CK_birth_date CHECK (birth_date<getdate())

insert into Customers (first_name, birth_date)
values ('Martyna','2026-01-01')