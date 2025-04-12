from typing import Optional, Annotated, List
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
import datetime

str255 = Annotated[str, mapped_column(String(255))]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

library_metadata = MetaData(schema='library_orm')


# moja klasa bazowa to jest declarative base

class Base(DeclarativeBase):
    metadata = library_metadata
    # type_annotation_map = {
    #    str255: String(255)
    # }


class Author(Base):
    __tablename__ = 'author'  # mapowanie typow danych python vs baza

    id: Mapped[intpk]
    name: Mapped[str]  # jak nie podajemy dlugosci stringa to nie musimy miec prawej strony
    email: Mapped[str255] = mapped_column(String(255))  # a tu mamy dlugosc wiec musimy
    login: Mapped[str] = mapped_column(String(100), default='No login')
    middle_name: Mapped[Optional[str]]  # optional obsluguje wartosc default

    books: Mapped[List['Book']] = relationship(back_populates='author', cascade='all, delete, delete-orphan')  # nie bedzie istniec ksiazka ktora nie ma autora
    address: Mapped['Address'] = relationship(back_populates='author', cascade='all, delete, delete-orphan')

    def __str__(self):
        return f'{self.name} {self.middle_name}'
    def __repr__(self):
        return f'{self.name} {self.middle_name}'

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[intpk]  # kolumna w bazie a atrybut w pythonie
    title: Mapped[str255]
    description: Mapped[Optional[str]]
    publication_date: Mapped[datetime.date]
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))

    author: Mapped['Author'] = relationship(back_populates='books')


# w alchemy ORM zeby polaczyc sie do bazy skorzystamy z sesji
# ona bedzie utrzymywala stany obiektow i zarzadzala transakcja
# sesja zarzadza nam ktore polaczenia z puli moze wykorzystac i cos zrobic w bazie

# Relacje:
# one to one
# one to many
# many to one

# one to many - jeden autor moze miec napisanych wiele ksiazek - klucz obcy trzymamy u dziecka
# one to one - jeden autor bedzie mial jeden adres -

class Address(Base):
    __tablename__ = 'address'

    id: Mapped[intpk]
    country: Mapped[str255]
    city: Mapped[str255]
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))

    # i robimy sobie znowu relacje

    author: Mapped['Author'] = relationship(back_populates='address')


# many to many - wielu autorow moze uczestniczyc w wielu eventach

events_authors = Table(
    'events_authors',
    Base.metadata,
    Column('author_id', ForeignKey('author.id')),
    Column('event_id', ForeignKey('event.id')),
)


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[intpk]
    name: Mapped[str255]

    participants: Mapped[List['Author']] = relationship(secondary=events_authors)

# teraz nie bedziemy tworzyc takiej bezpośredniej relacji ale przy pomocy tabeli pomocniczej






