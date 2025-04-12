CREATE TABLE accounts(
    account_id INT PRIMARY KEY IDENTITY,
    name VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL
)

CREATE TABLE transactions(
    transactions_id INT PRIMARY KEY IDENTITY,
    account_id INT FOREIGN KEY REFERENCES accounts(account_id),
    transaction_time DATETIME,
    amount FLOAT
)


CREATE TABLE workers(
    pesel VARCHAR(11) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL CHECK (birthday < GETDATE()),
    address_id INT FOREIGN KEY REFERENCES address(address_id)
)

ALTER TABLE workers ADD address_id INT

INSERT INTO workers(pesel, first_name, last_name, birthday)
VALUES ('444444', 'Monika', 'Nowak', '2000-01-01')

DROP TABLE address

CREATE TABLE address(
    address_id INT PRIMARY KEY IDENTITY,
    country VARCHAR(255) NOT NULL ,
    city VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL,
    postal_code VARCHAR(25) NOT NULL
)

TRUNCATE TABLE workers


INSERT INTO address (country, city, street, postal_code) VALUES('Polska', 'Warszawa', 'Marszałkowska 10', '00-001'),('Polska', 'Kraków', 'Floriańska 15', '31-019'),('Polska', 'Wrocław', 'Świdnicka 20', '50-066'),('Polska', 'Gdańsk', 'Długa 5', '80-831'),('Polska', 'Poznań', 'Półwiejska 8', '61-888'),('Polska', 'Łódź', 'Piotrkowska 50', '90-001'),('Polska', 'Katowice', 'Chorzowska 25', '40-101'),('Polska', 'Lublin', 'Krakowskie Przedmieście 30', '20-002'),('Polska', 'Szczecin', 'Aleja Wojska Polskiego 12', '70-471'),('Polska', 'Bydgoszcz', 'Gdańska 60', '85-005');-- Insert employees with addressesINSERT INTO workers (pesel, first_name, last_name, birthday, address_id) VALUES('90010112345', 'Jan', 'Kowalski', '1990-01-01', 1),('85051567890', 'Anna', 'Nowak', '1985-05-15', 2),('92030345678', 'Piotr', 'Wiśniewski', '1992-03-03', 3),('89090998765', 'Katarzyna', 'Dąbrowska', '1989-09-09', 4),('81070711223', 'Tomasz', 'Lewandowski', '1981-07-07', 5),('95010133445', 'Agnieszka', 'Wójcik', '1995-01-01', 6),('88050555667', 'Marcin', 'Kamiński', '1988-05-05', 7),('93020277889', 'Monika', 'Zielińska', '1993-02-02', 8),('87080899001', 'Paweł', 'Szymański', '1987-08-08', 9),('96060611234', 'Magdalena', 'Woźniak', '1996-06-06', 10);-- Insert employee without an address (NULL address_id)INSERT INTO workers (pesel, first_name, last_name, birthday, address_id) VALUES('97070722334', 'Marek', 'Kozłowski', '1997-07-07', NULL);

INSERT INTO workers (pesel, first_name, last_name, birthday, address_id) VALUES('90010112345', 'Jan', 'Kowalski', '1990-01-01', 1),('85051567890', 'Anna', 'Nowak', '1985-05-15', 2),('92030345678', 'Piotr', 'Wiśniewski', '1992-03-03', 3),('89090998765', 'Katarzyna', 'Dąbrowska', '1989-09-09', 4),('81070711223', 'Tomasz', 'Lewandowski', '1981-07-07', 5),('95010133445', 'Agnieszka', 'Wójcik', '1995-01-01', 6),('88050555667', 'Marcin', 'Kamiński', '1988-05-05', 7),('93020277889', 'Monika', 'Zielińska', '1993-02-02', 8),('87080899001', 'Paweł', 'Szymański', '1987-08-08', 9),('96060611234', 'Magdalena', 'Woźniak', '1996-06-06', 10);-- Insert employee without an address (NULL address_id)INSERT INTO workers (pesel, first_name, last_name, birthday, address_id) VALUES('97070722334', 'Marek', 'Kozłowski', '1997-07-07', NULL);

-- Insert addresses
INSERT INTO address (country, city, street, postal_code)
VALUES ('Polska', 'Warszawa', 'Marszałkowska 10', '00-001'),
       ('Polska', 'Kraków', 'Floriańska 15', '31-019'),
       ('Polska', 'Wrocław', 'Świdnicka 20', '50-066'),
       ('Polska', 'Gdańsk', 'Długa 5', '80-831'),
       ('Polska', 'Poznań', 'Półwiejska 8', '61-888'),
       ('Polska', 'Łódź', 'Piotrkowska 50', '90-001'),
       ('Polska', 'Katowice', 'Chorzowska 25', '40-101'),
       ('Polska', 'Lublin', 'Krakowskie Przedmieście 30', '20-002'),
       ('Polska', 'Szczecin', 'Aleja Wojska Polskiego 12', '70-471'),
       ('Polska', 'Bydgoszcz', 'Gdańska 60', '85-005');

-- Insert employees with addresses
INSERT INTO workers (pesel, first_name, last_name, birthday, address_id)
VALUES ('90010112345', 'Jan', 'Kowalski', '1990-01-01', 1),
       ('85051567890', 'Anna', 'Nowak', '1985-05-15', 2),
       ('92030345678', 'Piotr', 'Wiśniewski', '1992-03-03', 3),
       ('89090998765', 'Katarzyna', 'Dąbrowska', '1989-09-09', 4),
       ('81070711223', 'Tomasz', 'Lewandowski', '1981-07-07', 5),
       ('95010133445', 'Agnieszka', 'Wójcik', '1995-01-01', 6),
       ('88050555667', 'Marcin', 'Kamiński', '1988-05-05', 7),
       ('93020277889', 'Monika', 'Zielińska', '1993-02-02', 8),
       ('87080899001', 'Paweł', 'Szymański', '1987-08-08', 9),
       ('96060611234', 'Magdalena', 'Woźniak', '1996-06-06', 10);

-- Insert employee without an address (NULL address_id)
INSERT INTO workers (pesel, first_name, last_name, birthday, address_id)
VALUES ('97070722334', 'Marek', 'Kozłowski', '1997-07-07', NULL);