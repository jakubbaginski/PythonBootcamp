import typing


def add(*args: float) -> typing.Union[float, None]:
    result: float = 0
    try:
        if len(args) == 0:
            raise TypeError
        for n in args:
            result += n
    except TypeError:
        return None
    return float(result)


print(add(1, 2, 3, 4, 5, 6, -0, -8))
print(add(1, 2, 3, 'A'))
print(add(-1, -3))
print(add())


def calculate(n: float, **kwargs: float) -> float:
    result: float = n
    try:
        result += kwargs['add']
    except KeyError:
        pass
    try:
        result *= kwargs['multi']
    except KeyError:
        pass
    return float(result)


print(calculate(1, add=8, multi=2))
print(calculate(2, add=3))
print(calculate(2, multi=3))
print(calculate(2))


class Test:

    """
    @:parameter [optional] color:str    - color of the car\n
    @:parameter [optional] year: int    - year of registration\n
    @:parameter [optional] length: int  - length in mm
    """
    def __init__(self, **kwargs: typing.Union[int, str]):
        try:
            self.color = kwargs['color']
            if type(self.color) is not str:
                # logging.warning("Wrong type of 'color' argument, assuming default value")
                raise TypeError
        except (KeyError, TypeError):
            self.color = "red"
        try:
            self.length = kwargs['length']
            if type(self.length) is not int:
                # logging.warning("Wrong type of 'length' argument, assuming default value")
                raise TypeError
        except (KeyError, TypeError):
            self.length = 0

        # another way for defaulting - kwargs.get() method returning None if key is not found
        self.year = kwargs.get('year')
        if type(self.year) is not int or self.year is None:
            # logging.warning("Wrong type of 'year' argument, assuming default value")
            self.year = 1900

    def print(self, *args) -> None:
        print(f"{args} Year: {self.year}, Color: {self.color}, Length: {self.length}")


Test(color="orange", length=900, year=1909).print(1)
Test().print(2)
Test(length="orange").print(3)
Test(year="orange").print(4)
Test(color="orange").print(5)
Test(color=22, length="r", year="r").print(6)
Test()
