from typing import Tuple

class Point:
    coords: Tuple[int, int]
    label: str = '<unknown>'

x: int = 1
a: str = 2
b: int = None
print(x.startswith('d'))
print(x.endsswith('a'))
print(a.startswith('f'))

point = Point()
point.coords = (1, 2)
t = type(point.coords)
print(t)