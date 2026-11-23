"""Exercise 3 (slide 67) - Operator overloading.

Problems 1, 2, 4, 5, 6 and 7 of the "Operator Overloading" section
(the gist has no problem 3).
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence


# --------------------------------------------------------------------------- #
# Problem 1 - Complex numbers: + and -
# --------------------------------------------------------------------------- #
class Complex:
    """A complex number ``real + imag*i`` supporting ``+`` and ``-``."""

    def __init__(self, real: float = 0.0, imag: float = 0.0) -> None:
        self.real = real
        self.imag = imag

    def __add__(self, other: Complex) -> Complex:
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: Complex) -> Complex:
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Complex):
            return NotImplemented
        return (self.real, self.imag) == (other.real, other.imag)

    def __hash__(self) -> int:
        return hash((self.real, self.imag))

    def __repr__(self) -> str:
        return f"Complex({self.real}, {self.imag})"

    def __str__(self) -> str:
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"


# --------------------------------------------------------------------------- #
# Problem 2 - Person: > compares ages
# --------------------------------------------------------------------------- #
class Person:
    """A person; ``p1 > p2`` is ``True`` when ``p1`` is older than ``p2``."""

    def __init__(self, name: str, age: int, gender: str) -> None:
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other: Person) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, age={self.age}, gender={self.gender!r})"


# --------------------------------------------------------------------------- #
# Problem 4 - Vector: * is the dot product
# --------------------------------------------------------------------------- #
class Vector:
    """A 3D vector; ``v1 * v2`` returns the dot product (a number)."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other: Vector) -> float:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"


# --------------------------------------------------------------------------- #
# Problem 5 - Circle: all comparison operators, based on the radius
# --------------------------------------------------------------------------- #
class Circle:
    """A circle compared by radius with ``< > == != >= <=``."""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def __lt__(self, other: Circle) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __gt__(self, other: Circle) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius

    def __le__(self, other: Circle) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius <= other.radius

    def __ge__(self, other: Circle) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius >= other.radius

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        return result if result is NotImplemented else not result

    def __hash__(self) -> int:
        return hash(self.radius)

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"


# --------------------------------------------------------------------------- #
# Problem 6 - Point2D: comparisons based on distance from the origin
# --------------------------------------------------------------------------- #
class Point2D:
    """A 2D point compared by its Euclidean distance ``sqrt(x² + y²)`` to the origin.

    Note: two different points on the same circle around the origin
    (e.g. (3, 4) and (4, 3)) compare as *equal*, as the exercise requires.
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def distance(self) -> float:
        """Euclidean distance to the origin."""
        return math.hypot(self.x, self.y)

    def __lt__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance < other.distance

    def __gt__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance > other.distance

    def __le__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance <= other.distance

    def __ge__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance >= other.distance

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return math.isclose(self.distance, other.distance)

    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        return result if result is NotImplemented else not result

    def __hash__(self) -> int:
        return hash(round(self.distance, 9))

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"


# --------------------------------------------------------------------------- #
# Problem 7 - Matrix: * is the matrix product
# --------------------------------------------------------------------------- #
class Matrix:
    """A matrix of numbers; ``A * B`` is the matrix product."""

    def __init__(self, rows: Iterable[Sequence[float]]) -> None:
        self.rows = [list(row) for row in rows]
        if not self.rows or not self.rows[0]:
            raise ValueError("A matrix must have at least one row and one column")
        width = len(self.rows[0])
        if any(len(row) != width for row in self.rows):
            raise ValueError("All rows must have the same length")

    @property
    def shape(self) -> tuple[int, int]:
        """(number of rows, number of columns)."""
        return len(self.rows), len(self.rows[0])

    def __mul__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        n, m = self.shape
        m2, p = other.shape
        if m != m2:
            raise ValueError(f"Cannot multiply {n}x{m} by {m2}x{p} matrices")
        return Matrix(
            [
                [sum(self.rows[i][k] * other.rows[k][j] for k in range(m)) for j in range(p)]
                for i in range(n)
            ]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    __hash__ = None  # type: ignore[assignment]  # mutable container -> unhashable

    def __repr__(self) -> str:
        return f"Matrix({self.rows})"
