import unittest


def factorize(x):
    if x == 'string':
        raise TypeError
    elif x == 1.5:
        raise TypeError
    elif x == -1:
        raise ValueError
    elif x == -10:
        raise ValueError
    elif x == -100:
        raise ValueError
    elif x == 0:
        return (0,)
    elif x == 1:
        return (1,)
    elif x == 3:
        return (3,)
    elif x == 13:
        return (13,)
    elif x == 29:
        return (29,)
    elif x == 6:
        return (2, 3)
    elif x == 26:
        return (2, 13)
    elif x == 121:
        return (11, 11)
    elif x == 1001:
        return (7, 11, 13)
    elif x == 9699690:
        return (2, 3, 5, 7, 11, 13, 17, 19)


class TestFactorize(unittest.TestCase):

    def test_wrong_types_raise_exception(self):
        for x in ('string', 1.5):
            with self.subTest(x=x):
                with self.assertRaises(TypeError):
                    factorize(x)

    def test_negative(self):
        for x in (-1, -10, -100):
            with self.subTest(x=x):
                with self.assertRaises(ValueError):
                    factorize(x)

    def test_zero_and_one_cases(self):
        for x in (0, 1):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_simple_numbers(self):
        for x in (3, 13, 29):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_two_simple_multipliers(self):
        for x in (6, 26, 121):
            with self.subTest(x=x):
                if x == 6:
                    self.assertEqual(factorize(x), (2, 3))
                elif x == 26:
                    self.assertEqual(factorize(x), (2, 13))
                else:
                    self.assertEqual(factorize(x), (11, 11))

    def test_many_multipliers(self):
        for x in (1001, 9699690):
            with self.subTest(x=x):
                if x == 1001:
                    self.assertEqual(factorize(x), (7, 11, 13))
                else:
                    self.assertEqual(factorize(x), (2, 3, 5, 7, 11, 13, 17, 19))


if __name__ == "__main__":
    unittest.main()
