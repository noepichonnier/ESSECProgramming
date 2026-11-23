import unittest

from inheritance import (
    BankAccount, Bicycle, Car, Employee, SavingsAccount, Student, Vehicle,
)


class TestVehicle(unittest.TestCase):
    def test_drive(self):
        self.assertEqual(Vehicle().drive(), "Driving a vehicle")
        self.assertEqual(Car().drive(), "Driving a car")
        self.assertEqual(Bicycle().drive(), "Riding a bicycle")

    def test_polymorphism(self):
        results = [v.drive() for v in (Vehicle(), Car(), Bicycle())]
        self.assertEqual(results, ["Driving a vehicle", "Driving a car", "Riding a bicycle"])


class TestPeople(unittest.TestCase):
    def test_student(self):
        s = Student("Ana", 20, "1 rue X", "AI")
        self.assertIn("Ana", s.introduce())
        self.assertIn("I study AI", s.introduce())

    def test_employee(self):
        e = Employee("Bob", 30, "2 rue Y", "ACME")
        self.assertIn("I work at ACME", e.introduce())


class TestBank(unittest.TestCase):
    def test_deposit_withdraw(self):
        acc = BankAccount("FR1", 100)
        acc.deposit(50)
        self.assertTrue(acc.withdraw(30))
        self.assertEqual(acc.balance, 120)

    def test_withdraw_insufficient(self):
        acc = BankAccount("FR1", 10)
        self.assertFalse(acc.withdraw(11))
        self.assertEqual(acc.balance, 10)

    def test_invalid_amounts(self):
        acc = BankAccount("FR1", 10)
        with self.assertRaises(ValueError):
            acc.deposit(-1)
        with self.assertRaises(ValueError):
            acc.withdraw(0)

    def test_transfer(self):
        a, b = BankAccount("A", 100), SavingsAccount("B", 0, 0.1)
        self.assertTrue(a.transfer(b, 60))
        self.assertEqual((a.balance, b.balance), (40, 60))
        self.assertFalse(a.transfer(b, 100))
        self.assertEqual((a.balance, b.balance), (40, 60))

    def test_savings(self):
        s = SavingsAccount("S", 1000, 0.05)
        self.assertEqual(s.add_interest(), 50)
        self.assertEqual(s.check_balance(), 1050)
        self.assertIsInstance(s, BankAccount)


if __name__ == "__main__":
    unittest.main()
