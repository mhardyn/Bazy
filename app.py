import customtkinter as ctk # alias skrótowe odwołanie
from alchemy_orm import Author
from orm_connection import Session
from sqlalchemy import select
from CTkTable import CTkTable

session = Session()

def add_author_to_db(author: Author):
    session.add(author)
    session.commit()

def add_author():
    add_author_popup = ctk.CTkToplevel(master=app)
    add_author_popup.title("Dodaj autora")
    add_author_popup.geometry("800x600")

    add_author_popup.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(add_author_popup, text="Dodanie nowego autora", font=ctk.CTkFont(size=30, weight='bold')) \
        .grid(row=0, column=0, padx=20, pady=20)

# inputs

    ctk.CTkLabel(add_author_popup, text='Imię i Nazwisko') \
        .grid(row=1, column=0, padx=20, pady=(20, 0), sticky='w')
    name_input = ctk.CTkEntry(add_author_popup)
    name_input.grid(row=2, column=0, padx=20, sticky='ew')

    ctk.CTkLabel(add_author_popup, text='Email') \
        .grid(row=3, column=0, padx=20, pady=(20, 0), sticky='w')
    email_input = ctk.CTkEntry(add_author_popup)
    email_input.grid(row=4, column=0, padx=20, sticky='ew')

    ctk.CTkLabel(add_author_popup, text='Login') \
        .grid(row=5, column=0, padx=20, pady=(20, 0), sticky='w')
    login_input = ctk.CTkEntry(add_author_popup)
    login_input.grid(row=6, column=0, padx=20, sticky='ew')

    ctk.CTkLabel(add_author_popup, text='Drugie imię') \
        .grid(row=7, column=0, padx=20, pady=(20, 0), sticky='w')
    middle_name_input = ctk.CTkEntry(add_author_popup)
    middle_name_input.grid(row=8, column=0, padx=20, sticky='ew')

    # add author button
    ctk.CTkButton(add_author_popup, text='Dodaj authora',
                  command=lambda: add_author_to_db(Author(
                      name=name_input.get(),
                      middle_name=middle_name_input.get(),
                      email=email_input.get(),
                      login=login_input.get(),
                  ))).grid(row=9, column=0, padx=20, pady=20, sticky='ew')


if __name__ == '__main__':
    ctk.set_appearance_mode('dark') # ustawienie ciemnego okna
    app = ctk.CTk()
    app.title('Biblioteka')
    app.geometry('1024x700')

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    menu_bar = ctk.CTkFrame(app, corner_radius=20)
    menu_bar.grid_columnconfigure(0, weight=1)
    menu_bar.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    app_title = ctk.CTkLabel(menu_bar, text='Biblioteka', font=ctk.CTkFont(size=15, weight='bold'))
    app_title.grid(row=0, column=0, padx=25, pady=10, sticky='w')

    add_author_button = ctk.CTkButton(menu_bar, text='Dodaj autora', command=add_author)
    add_author_button.grid(row=0, column=1, padx=25, pady=10)

    app_content = ctk.CTkFrame(app)
    app_content.grid_columnconfigure(0, weight=1)
    app_content.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    authors = session.execute(select(Author)).scalars().all()
    authors_data = [['ID', 'Imię', 'Drugie imię', 'Email', 'Login']] + \
                   [[a.id, a.name, a.middle_name, a.email, a.login] for a in authors]
    authors_table = CTkTable(master=app_content, row=len(authors), values= authors_data, column=len(authors_data[0]))

    authors_table.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

    app.mainloop() # okna się otwiera i nie zamyka

