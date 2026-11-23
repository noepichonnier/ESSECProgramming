"""Exercise 3 (slide 67) - Inheritance (problems 1, 2 and 3)."""
from __future__ import annotations


# --------------------------------------------------------------------------- #
# Problem 1 - Vehicle, Car, Bicycle
# --------------------------------------------------------------------------- #
class Vehicle:
    def drive(self) -> str:
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self) -> str:
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self) -> str:
        return "Riding a bicycle"


# --------------------------------------------------------------------------- #
# Problem 2 - Person, Student, Employee
# --------------------------------------------------------------------------- #
class Person:
    def __init__(self, name: str, age: int, address: str) -> None:
        self.name = name
        self.age = age
        self.address = address

    def introduce(self) -> str:
        return f"Hi, I'm {self.name}, {self.age} years old, and I live at {self.address}."


class Student(Person):
    def __init__(self, name: str, age: int, address: str, field_of_study: str) -> None:
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self) -> str:
        return f"{super().introduce()} I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name: str, age: int, address: str, company: str) -> None:
        super().__init__(name, age, address)
        self.company = company

    def introduce(self) -> str:
        return f"{super().introduce()} I work at {self.company}."


# --------------------------------------------------------------------------- #
# Problem 3 - BankAccount, SavingsAccount
# --------------------------------------------------------------------------- #
class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0) -> None:
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Add ``amount`` to the balance (must be strictly positive)."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        """Remove ``amount``; return ``False`` (and change nothing) if funds are insufficient."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination: BankAccount, amount: float) -> bool:
        """Move ``amount`` to ``destination``; ``False`` if the balance is insufficient."""
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, balance: float = 0.0, interest_rate: float = 0.0) -> None:
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate  # e.g. 0.02 for 2 %

    def add_interest(self) -> float:
        """Credit one period of interest and return the amount added."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def check_balance(self) -> float:
        return self.balance
