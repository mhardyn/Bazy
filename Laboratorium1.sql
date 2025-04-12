create table business_trips (
    trip_id INT PRIMARY KEY,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    destination varchar(255),
    description varchar(4000)
)

create table employees(
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    hireDate DATE,
    salary FLOAT,
    department_id INT
)

create table department(
    department_id INT PRIMARY KEY,
    name VARCHAR(1000)
)

alter table employees
    add constraint FK_employees_department_department_id FOREIGN KEY(department_id)
    references department(department_id)

create table cars(
    car_id INT PRIMARY KEY,
    millage BIGINT,
    brand VARCHAR(100),
    engine_type VARCHAR(100),
    employee_id INT FOREIGN KEY REFERENCES employees(employee_id)
)

create table address(
    address_id INT PRIMARY KEY,
    street VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255),
    employee_id INT FOREIGN KEY REFERENCES employees(employee_id)
)

create table contracts(
    contract_id INT PRIMARY KEY,
    start_date DATE NOT NULL DEFAULT GETDATE(),
    end_date DATE NOT NULL,
    type VARCHAR(100),
    employee_id INT FOREIGN KEY REFERENCES employees(employee_id)
)

create table business_trip_employees(
    employee_id INT FOREIGN KEY REFERENCES employees(employee_id),
    trip_id INT FOREIGN KEY REFERENCES business_trips(trip_id)
)



