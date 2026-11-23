# Exercise 3 – OOP problems (slide 67)

| File | Content |
|------|---------|
| `operator_overloading.py` | `Complex` (+, -), `Person` (>), `Vector` (* dot product), `Circle` (all comparisons), `Point2D` (comparisons by distance to origin), `Matrix` (* product) |
| `inheritance.py` | `Vehicle`/`Car`/`Bicycle`, `Person`/`Student`/`Employee`, `BankAccount`/`SavingsAccount` |
| `test_*.py` | unit tests (standard library `unittest`, nothing to install) |

```bash
python3 -m unittest -v
```

Notes
- Operators return `NotImplemented` for unsupported types so Python raises a proper `TypeError`.
- `Point2D` equality is based on the distance from the origin (as in the statement), so `(3, 4) == (4, 3)`.
- `withdraw` and `transfer` return `False` on insufficient funds instead of raising.
- The gist numbering is kept (the operator overloading section has no problem 3).
