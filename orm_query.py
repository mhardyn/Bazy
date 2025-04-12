from orm_connection import Session
from sqlalchemy import *
from sqlalchemy.orm import joinedload
from alchemy_orm import Author

session = Session()

# select_authors = select(Author).options(joinedload(Author.books), joinedload(Author.address)).filter_by(id=1) # ostatnie można zastąpić .where(Author.id = 1)
# all_authors = session.execute(select_authors).scalars().unique().all()
# print(all_authors)
#
# for a in all_authors:
#     print(f'Author {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')

select_authors = select(Author).options(joinedload(Author.books), joinedload(Author.address)).filter_by(id=1)
a = session.execute(select_authors).unique().scalar_one()

print(f'Author {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')

a = session.get(Author, 1)
print(f'Author {a.name} napisał {len(a.books)} książek i mieszka w {a.address.country} {a.address.city}')




