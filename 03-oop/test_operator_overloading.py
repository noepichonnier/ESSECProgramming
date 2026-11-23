import unittest

from operator_overloading import Circle, Complex, Matrix, Person, Point2D, Vector


class TestComplex(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Complex(1, 2) + Complex(3, -5), Complex(4, -3))

    def test_sub(self):
        self.assertEqual(Complex(1, 2) - Complex(3, -5), Complex(-2, 7))

    def test_str(self):
        self.assertEqual(str(Complex(1, -2)), "1 - 2i")

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            Complex(1, 2) + 3


class TestPerson(unittest.TestCase):
    def test_gt(self):
        old, young = Person("A", 40, "F"), Person("B", 20, "M")
        self.assertTrue(old > young)
        self.assertFalse(young > old)
        self.assertFalse(old > Person("C", 40, "F"))


class TestVector(unittest.TestCase):
    def test_dot_product(self):
        self.assertEqual(Vector(1, 2, 3) * Vector(4, -5, 6), 12)

    def test_orthogonal(self):
        self.assertEqual(Vector(1, 0, 0) * Vector(0, 1, 0), 0)


class TestCircle(unittest.TestCase):
    def test_all_operators(self):
        small, big, twin = Circle(1), Circle(2), Circle(1)
        self.assertTrue(small < big)
        self.assertTrue(big > small)
        self.assertTrue(small <= twin and small >= twin)
        self.assertTrue(small == twin)
        self.assertTrue(small != big)
        self.assertFalse(small != twin)
        self.assertFalse(big < small)


class TestPoint2D(unittest.TestCase):
    def test_compare_by_distance(self):
        near, far = Point2D(1, 1), Point2D(3, 4)
        self.assertTrue(near < far)
        self.assertTrue(far > near)
        self.assertTrue(near != far)
        self.assertTrue(near <= far and far >= near)

    def test_same_distance_is_equal(self):
        self.assertEqual(Point2D(3, 4), Point2D(4, 3))
        self.assertEqual(Point2D(3, 4).distance, 5)


class TestMatrix(unittest.TestCase):
    def test_product(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        self.assertEqual(a * b, Matrix([[19, 22], [43, 50]]))

    def test_rectangular(self):
        a = Matrix([[1, 2, 3]])        # 1x3
        b = Matrix([[1], [2], [3]])    # 3x1
        self.assertEqual(a * b, Matrix([[14]]))
        self.assertEqual((b * a).shape, (3, 3))

    def test_incompatible_shapes(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2]]) * Matrix([[1, 2]])

    def test_ragged_rows(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2], [3]])


if __name__ == "__main__":
    unittest.main()
