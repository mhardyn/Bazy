# Proszę napisać modele obiektów z wykorzystaniem SQlAlchemy ORM dla opisanej bazy danych:
# 1. Użytkownik:
# • Nazwa tabeli: users
# • Każdy User ma jeden adres dostawy (relacja jeden do jednego).
# • Każdy User może mieć wiele koszyków (relacja jeden do wielu).
# • Każdy User posiada zmienne: imię, nazwisko oraz opcjonalnie drugie imię.
# 2. Adres Dostawy:
# • Nazwa tabeli: shipping_addresses
# • Każdy User ma jeden adres dostawy.
# • Adres posiada zmienne: kraj, miasto, kod pocztowy, numer bloku i opcjonalnie
# numer mieszkania.
# 3. Koszyk:
# • Nazwa tabeli: carts
# • Każdy koszyk należy do jednego użytkownika.
# • Koszyk może zawierać wiele produktów (relacja wiele do wielu).
# • Koszyk posiada zmienne: data utworzenia
# 4. Produkt:
# • Nazwa tabeli: products
# • Product posiada zmienne: tytuł, opis i cenę.
# • Produkty mogą być dodawane do wielu koszyków (relacja wiele do wielu).
# • Ponieważ jeden koszyk może zawierać wiele produktów, a jeden produkt może
# znajdować się w wielu koszykach, relacja jest realizowana poprzez tabelę
# asocjacyjną.

from typing import Optional, Annotated, List
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
import datetime

class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
forpk = Annotated[int, mapped_column(Integer, foreign_key=True, autoincrement=True)]
str255 = Annotated[str, mapped_column(String(255))]
int15 = Annotated[str, mapped_column(String(15))]

# 1

class Users(Base):
    id: Mapped[intpk]
    adress: Mapped[str]
    basket: Mapped[str]
    first_name: Mapped[str]
    surname: Mapped[str]
    middlename: Mapped[str]

    carts: Mapped['Carts'] = relationship(back_populates='users', cascade='all, delete, delete-orphan')
    shipping_addressess: Mapped['ShippingAddresses'] = relationship(back_populates='users', cascade='all, delete, delete-orphan')
#2

class ShippingAddresses(Base):
    id: Mapped[intpk]
    country: Mapped[str255]
    city: Mapped[str255]
    postalcode: Mapped[int15]
    block_number: Mapped[int]
    apartament_number: Mapped[Optional[int]]
    user_id: Mapped[forpk]


class Carts(Base):
    user_id: Mapped[intpk]
    cart_id: Mapped[int]
    creation_date: Mapped[datetime]

    carts_products: Mapped['CartsProducts'] = relationship(back_populates='carts', cascade='all, delete, delete-orphan')

class Products(Base):
    product_id: Mapped[intpk]
    title: Mapped[str255]
    description: Mapped[str]
    price: Mapped[float]

    carts_products: Mapped['CartsProducts'] = relationship(back_populates='products', cascade='all,


class CartsProducts(Base):
    cart_id: Mapped[forpk]
    product_id: Mapped[forpk]



