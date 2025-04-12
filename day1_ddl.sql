use AdventureWorks2014

select * from Person.Person

use master

select * from AdventureWorks2014.Person.Person where FirstName='Dylan'

select Name, Color, ProductNumber, ProductID
FROM Production.Product
order by Color Desc , Name

select * from Production.Product
where Color='Black'

--yyyy-MM-dd HH:mi:ss.millis

select SellStartDate, Name , Color FROM Production.Product
where SellStartDate = '2008-04-30'

select ProductID, Name, Color from Production.Product
where ProductID <= 317

select * from Production.Product
where Color like '%B%'

select *
from Production.Product
where Name like 'Half-Finger Gloves, _'

select *
from Production.Product
where Name like 'Half-Finger Gloves, [MS]'

select *
from Production.Product
where Name like 'Half-Finger Gloves, [A-Z]'

select *
from Production.Product
where Name in ('Half-Finger Gloves, S','Classic Vest, S')

--AND
--OR

select ProductID, Name, Color from Production.Product
where color ='Black' or color = 'Red'

--UWAGA : ADN wykonuje sie w pierwszej kolejnosci, jesli potrzeba mozemy uzyc nawiasu
select ProductSubcategoryID, Name, Color from Production.Product
where (color ='Black' or color = 'Red') AND ProductSubcategoryID = 14

--jak uzyskac aktualna date
select getdate()

select ProductSubcategoryID, Name, Color from Production.Product
where ProductSubcategoryID >=10 and ProductSubcategoryID <=20

--to powyzej to jest to samo co to:

select ProductSubcategoryID, Name, Color from Production.Product
where ProductSubcategoryID BETWEEN 10 and 20

select ProductSubcategoryID, SellStartDate, Name, Color from Production.Product
where SellStartDate BETWEEN '2011-05-31' AND '2012-05-30'

--do NULL uzywamy :
--IS
--IS NOT

select ProductSubcategoryID, SellStartDate, Name, Color from Production.Product
where Color is NULL

--tu korzystamy z rozszerzenia TSQL ,ktore jest funkcja microsoftowa dla MSSQL
select Name, Color, ISNULL(Color, 'No Color') as Supercolor
from Production.Product

--distinct usuwa duplikaty
select distinct Color from Production.Product

--aliasy do nazw kolumn (nie nadpisuja oryginalnych kolumn tylko zmieniaja mi tabelke wynikową)
select Name as Imię, Color as 'Nowy Kolor' FROM Production.Product

--pobieranie pierwszych iluś wartości
select TOP 10 Name as Imię, Color as 'Nowy Kolor' FROM Production.Product

--pobieranie pierwszych 10% wartości
select TOP 10 PERCENT Name as Imię, Color as 'Nowy Kolor' FROM Production.Product

--konkatenacja dwoch kolumn
select FirstName, LastName , FirstName + ' ' + LastName as FULL_NAME
from Person.Person

--T-SQL
select FirstName,
       LEFT (FirstName, 1) AS FirstLetter,
       LEFT (FirstName, 3) AS First3Letters,
       RIGHT (FirstName, 1) AS LastLetter,
       SUBSTRING (FirstName, 1,2),
       SUBSTRING (FirstName, 1,4)
FROM Person.Person

--ustawienie jezyka na polski

SET LANGUAGE 'Polish'

--T-SQL
SELECT SellStartDate,
       YEAR(SellStartDate) AS year,
       DATENAME(mm, SellStartDate) AS month,


--join (to jest inner join , inne mozna pominac , czyli czesc wspolna dwoch tabel)
select p.Name, Color, psc.Name
from Production.Product p
join Production.ProductSubcategory psc
on p.ProductSubcategoryID = psc.ProductSubcategoryID

--full outer join ale tylko elementy rozne
select p.Name, Color, psc.Name
from Production.Product p
full outer join Production.ProductSubcategory psc
on p.ProductSubcategoryID = psc.ProductSubcategoryID
where p.ProductSubcategoryID  is NULL
or psc.ProductSubcategoryID is NULL

--join z wieksza iloscia tabel
select p.Name, Color, psc.Name, pc.Name
from Production.Product p
join Production.ProductSubcategory psc
on p.ProductSubcategoryID = psc.ProductSubcategoryID
join Production.ProductCategory pc
on psc.ProductCategoryID=pc.ProductCategoryID

--left albo right outer join
select p.Name, Color, psc.Name, pc.Name
from Production.Product p
left join Production.ProductSubcategory psc
on p.ProductSubcategoryID = psc.ProductSubcategoryID
left join Production.ProductCategory pc
on psc.ProductCategoryID=pc.ProductCategoryID
where pc.Name like '%Clo%'
order by psc.Name desc

select p.Name,p.ProductSubcategoryID, psc.Name
from Production.Product p
left join Production.ProductSubcategory psc
on p.ProductSubcategoryID = psc.ProductSubcategoryID


select p.Name, Color, psc.Name, pc.Name
from Production.Product p
right join Production.ProductSubcategory psc
on p.ProductSubcategoryID = psc.ProductSubcategoryID
right join Production.ProductCategory pc
on psc.ProductCategoryID=pc.ProductCategoryID
where pc.Name like '%Clo%'
order by psc.Name desc

--Grupowanie i funkcje agregujace

select count(*) as ProductCnt,
       count(ProductSubcategoryID) as Subcategories,
       AVG (Weight) as AvgWeight,
       MAX (Weight) as MaxWeight,
       MIN (Weight) as Minweight
from Production.Product

SELECT p.Color, psc.Name, count(*) as ProductCnt
FROM Production.Product p
inner join Production.ProductSubcategory psc ON p.ProductSubcategoryID=psc.ProductSubcategoryID
where p.Color IS NOT NULL
group by p.Color, psc.Name
having Count(*) > 10
order by ProductCnt DESC

