from orm_connection import Session
from sqlalchemy import *
from sqlalchemy.orm import joinedload
from alchemy_orm import Author, Book, Address
import datetime

session = Session()

# select_authors = select(Author).options(joinedload(Author.books), joinedload(Author.address)).filter_by(id=1) # ostatnie można zastąpić .where(Author.id = 1)
# all_authors = session.execute(select_authors).scalars().unique().all()
# print(all_authors)
#
# for a in all_authors:
#     print(f'Author {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')

# Jeden autor - pierwszy sposób

select_authors = select(Author).options(joinedload(Author.books), joinedload(Author.address)).filter_by(id=1)
a = session.execute(select_authors).unique().scalar_one()

print(f'Author {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')

# Jeden autor - drugi sposób

a = session.get(Author, 1)
print(f'Author {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')

# Insert

# author = Author(name='Andrzej', email='email', login='login', middle_name='middle')
# author.adress = Address(country='Litwa', city='Wilno')
# author.books = [
#         Book(title='Jeden', publication_date=datetime.date.today()),
#         Book(title='Dwa', publication_date=datetime.date.today())
# ]
# session.add(author)
# session.commit()


# Update

author = session.get(Author, 7)
author.middle_name = 'Jan'
for b in author.books:
    if b.title == 'Jeden':
        b.description = 'To jest pierwsza książka!'

session.add(author)
session.commit()

# Delete
author = session.get(Author, 7)
session.delete(author)
session.commit()








