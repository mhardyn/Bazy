from db1 import connection
import datetime

class Account:
    def __init__(self, name: str, opening_balance: float = 0.0):
        self.name = name
        self.balance = opening_balance

        connection.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)",
                           (self.name, self.balance))
        cursor = connection.execute("SELECT @@IDENTITY AS ID")

        self.id = cursor.fetchval()

        connection.commit()

        print(f'Konto zostalo utworzone dla {self.name} z balansem {self.balance}')

    def deposit(self, amount: float, auto_commit:bool = True) -> float:
        if amount > 0:
            self.balance += amount
            connection.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (self.balance, self.id))
            connection.execute("INSERT INTO transactions (account_id, transaction_time, amount) VALUES (?, ?, ?)",
                               (self.id, datetime.datetime.now(), amount))
            if auto_commit:
                connection.commit()

            print(f'Na konto {self.name} zostało dodane {amount} PLN')
        return round(self.balance, 2)

    def withdraw(self, amount: float, auto_commit:bool = True) -> float:
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            connection.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (self.balance, self.id))
            connection.execute("INSERT INTO transactions (account_id, transaction_time, amount) VALUES (?, ?, ?)",
                               (self.id, datetime.datetime.now(), -amount))
            if auto_commit:
                connection.commit()

            print (f'Z konta {self.name} zostało wypłacone {amount} PLN')
        else:
            raise ValueError("Nie masz wystarczajacych srodkow na koncie")

        return round(self.balance, 2)

    def send_founds(self, amount: float, account):
        try:
            self.withdraw(amount, auto_commit=False)
            account.deposit(amount, auto_commit=False)
            connection.commit()
        except:
            connection.rollback()
            print("Brak wystarczających środków")

#uzupelnic kod o zadanie drugie
    def transaction_log(self,type:str , transaction_time, amount:float):
        if amount !=0:
            transaction_time = connection.execute("SELECT transaction_time FROM transactions WHERE account_id = ?", (self.id),)
            print(f'{self.type} {transaction_time} {amount}')


# if __name__ == '__main__':
#     account = Account('Anna')
#     account.deposit(10)
#     account.deposit(0.1)
#     balance = account.withdraw(5)
#     print(balance)

if __name__ == '__main__':
    account_tomek = Account('Tomek',10)
    account_ola = Account ('Ola', 10)
    account_tomek.send_founds (5, account_ola)

