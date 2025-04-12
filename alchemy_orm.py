# modyfikowanie obiektów na relacje - ORM
import uuid

from typing import Optional, Annotated, List
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
import datetime

str255 = Annotated[str, mapped_column(String(255))]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

library_metadata = MetaData(schema='library_orm')

class Base(DeclarativeBase): # klasa base dziedziczy declarative_base
    metadata = library_metadata
    # type_annotation_map = {
    #     str255: String(255)
    # }

class Author(Base):
    __tablename__ = 'author' # nazwa zmiennej __tablename__

    id: Mapped[intpk] # mapped_column(primary_key=True, autoincrement=True) # nazwą kolumny jest id
    name: Mapped[str] # VARCHAR(MAX) można usunąć prawą strone txn mapped_column(string)
    email: Mapped[str255] # można usunąć prawą strone mapped_column(String(255))
    login: Mapped[str] = mapped_column(String(100), default='No Login')
    middle_name: Mapped[Optional[str]] # tak samo można usunąć prawą strone, ponieważ mapped_column() zostaje puste

    books: Mapped[List['Book']] = relationship(back_populates='author', cascade='delete, delete-orphan')


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[intpk]
    title: Mapped[str255]
    description: Mapped[Optional[str]]
    publication_date: Mapped[datetime.date]

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id')) # to będzie kolumną w bazie

    author: Mapped['Author'] = relationship(back_populates='books')# w nawiasach podajemy ciąg znakó klasy

