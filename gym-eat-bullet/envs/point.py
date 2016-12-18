from functools import total_ordering
import collections

@total_ordering
class Point:
    def __init__(self, x=0, y=0) -> None:
        if isinstance(x, collections.Iterable):
            self.x, self.y = x
            return
        self.x = x
        self.y = y

    def __add__(self, he: 'Point'):
        return Point(self.x + he.x, self.y + he.y)

    def __minus__(self, he: 'Point'):
        return Point(self.x - he.x, self.y - he.y)

    def __mul__(self, v):
        return Point(v * self.x, v * self.y)

    def __rmul__(self, v):
        return self.__mul__(v)

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __lt__(self, he: 'Point'):
        return self.to_tuple() < he.to_tuple()

    def __eq__(self, he: 'Point'):
        return self.to_tuple() == he.to_tuple()

    def __hash__(self):
        return hash(self.to_tuple())


if __name__ == '__main__':
    print(Point(1, 3) >= Point(1, 2.0))
    s = (Point(1, 2), Point(3, 4))
    print(s)
    print(Point((1, 2)), Point(x for x in (3, 4)))
    print(Point(1, 2) in [Point(1, 2), Point(3, 4)])
