from typing import Iterator, Union, List
from typing import Tuple


class BaseVersion:
    """BaseVersion classMinimal Semantic Versioning library
    This is a minimal Python Semantic Version library.

    Values can be passed as arbitrary number of `int` numbers, for example:

    >>> v = BaseVersion(1, 0, 0)
    >>> str(v)
    '1.0.0'

    Or as strings, which will be converted to versions:

    >>> v = Version.from_string("1.0.0.5322")
    >>> str(v)
    '1.0.0.5322'
    >>> v
    BaseVersion(1, 0, 0, 5322)

    Implementation of comparison operators (`__lt__`, `__gt__`, `__le__`, `__ge__`) allows for
    sorting operations to work. For example:

    >>> versionslist = [
    ...     BaseVersion.from_string("1.0.0"), BaseVersion.from_string("1.0.1"),
    ...     BaseVersion.from_string("0.9.95"), BaseVersion(0, 8, 97),
    ...     BaseVersion(2024, 2, 25, 101), BaseVersion(1, 0, 0, 0)]
    >>> sorted(versionslist)
    [BaseVersion(0, 8, 97), BaseVersion(0, 9, 95), BaseVersion(1, 0, 0), BaseVersion(1, 0, 0, 0), BaseVersion(1, 0, 1), BaseVersion(2024, 2, 25, 101)]
    >>> sorted(versionslist, reverse=True)
    [BaseVersion(2024, 2, 25, 101), BaseVersion(1, 0, 1), BaseVersion(1, 0, 0, 0), BaseVersion(1, 0, 0), BaseVersion(0, 9, 95), BaseVersion(0, 8, 97)]


    Some possible Edge cases tests:

    Open tuple can give weird representation, but logic still works:

    >>> version_edgecase = BaseVersion(1,)
    >>> version_base = BaseVersion(1)
    >>> version_edgecase
    BaseVersion(1,)
    >>> len(version_edgecase)
    1
    >>> version_edgecase == version_base
    True
    >>> version_edgecase < version_base
    False
    >>> version_edgecase > version_base
    False

    You can make your version *really* long. Why tho? No idea.

    >>> version_really_long = BaseVersion(*[x for x in range(9999999)])
    >>> len(version_really_long)
    9999999
    >>> version_really_long  # doctest: +ELLIPSIS
    BaseVersion(0, 1, 2, ..., 9999997, 9999998)
    >>> version_really_long[-1:]
    (9999998,)
    >>> str(version_really_long)  # doctest: +ELLIPSIS
    '0.1.2...9999997.9999998'

    Version parts can be... negative. I am going to rethink this life choice.

    >>> version_with_negative = BaseVersion(-3, 5, -99)
    >>> version_with_negative
    BaseVersion(-3, 5, -99)
    >>> str(version_with_negative)
    '-3.5.-99'
    """

    def __init__(self, *args: int) -> None:
        """Constructor

        >>> v = BaseVersion(2023, 3, 5)
        >>> v
        BaseVersion(2023, 3, 5)
        """
        self.__fill_parts(*args)

    def __fill_parts(self, *args: int) -> None:
        """
        Fills out all version parts into class' internal tuple

        >>> v = BaseVersion("a", 3, 4)  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        TypeError: Parts of semantic version must be all integer, 'a' passed
        """
        __version_parts: List[int] = []
        for part in args:
            if not isinstance(part, int):
                raise TypeError(
                    f"Parts of semantic version must be all integer, '{part}' passed"
                )
            __version_parts.append(part)
        self.__version_parts: Tuple[int, ...] = tuple(__version_parts)

    @staticmethod
    def from_string(version: str) -> "BaseVersion":
        """Create semantic version directly from the string

        >>> vs = Version.from_string("2023.03.05")
        >>> vs  # doctest: +ELLIPSIS
        BaseVersion(2023, 3, 5)
        >>> v = Version.from_string("3.4.5.abc")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: invalid literal for int() with base 10: 'abc'
        """
        parts: list = [int(v) for v in version.split(".")]
        return BaseVersion(*parts)

    def __iter__(self) -> Iterator[int]:
        """Iterate through version parts, used for casting into list, tuple, etc...

        >>> v = BaseVersion(2023, 3, 5)
        >>> version_parts = tuple(v)
        >>> version_parts
        (2023, 3, 5)
        """
        for part in self.__version_parts:
            yield part

    def __len__(self) -> int:
        """Returns number of version items

        >>> len(BaseVersion(1, 2, 3))
        3
        >>> len(BaseVersion(1))
        1
        >>> len(Version.from_string("2023.03.04.05555.0"))
        5
        """
        return len(self.__version_parts)

    def __str__(self) -> str:
        """String representation of semantic version

        >>> v = BaseVersion(2023, 3, 5)
        >>> vs = Version.from_string("2023.03.05")
        >>> str(vs), str(v)
        ('2023.3.5', '2023.3.5')
        """
        return ".".join([str(p) for p in self.__version_parts])

    def __eq__(self, b: object) -> bool:
        """Implementation of "==" internal type method for comparing values of same type

        >>> version_base = BaseVersion(2023, 3, 5)
        >>> version_short = BaseVersion(4)
        >>> version_alternate = Version.from_string("2024.03.05")
        >>> version_with_zero = BaseVersion(2023, 3, 5, 0)
        >>> version_same = Version.from_string("2023.03.05")
        >>> version_base == version_alternate
        False
        >>> version_base == version_same
        True
        >>> version_base == version_with_zero
        False
        >>> version_short == 4
        False
        >>> version_short == version_base
        False
        """
        if not isinstance(b, type(self)):
            return NotImplemented

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)  # type: ignore

        return self_parts == b_parts

    def __gt__(self, b: object) -> bool:
        """Implementation of ">" internal type method for comparing values of same type

        >>> version_base = BaseVersion(2023, 3, 5)
        >>> version_short = BaseVersion(4)
        >>> version_greater_1 = BaseVersion(2023, 3, 5, 0)
        >>> version_greater_2 = BaseVersion(2024, 3, 5)
        >>> version_greater_3 = BaseVersion(2023, 3, 6)
        >>> version_base > version_greater_1, version_base > version_greater_2, version_base > version_greater_3
        (False, False, False)
        >>> version_lesser_1 = BaseVersion(2023, 3, 4)
        >>> version_lesser_2 = BaseVersion(2023, 3)
        >>> version_lesser_3 = BaseVersion(2023, 1, 5)
        >>> version_base > version_lesser_1, version_base > version_lesser_2, version_base > version_lesser_3
        (True, True, True)
        >>> version_same = Version.from_string("2023.3.5")
        >>> version_base > version_same
        False
        >>> version_short > 4  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        TypeError: '>' not supported between instances of 'Version' and 'int'
        >>> version_short > version_base
        False
        """
        if not isinstance(b, type(self)):
            return NotImplemented

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)  # type: ignore

        return self_parts > b_parts

    def __lt__(self, b: object) -> bool:
        """Implementation of "<" internal type method for comparing values of same type

        >>> version_base = BaseVersion(2023, 3, 5)
        >>> version_short = BaseVersion(4)
        >>> version_greater_1 = BaseVersion(2023, 3, 5, 0)
        >>> version_greater_2 = BaseVersion(2024, 3, 5)
        >>> version_greater_3 = BaseVersion(2023, 3, 6)
        >>> version_base < version_greater_1, version_base < version_greater_2, version_base < version_greater_3
        (True, True, True)
        >>> version_lesser_1 = BaseVersion(2023, 3, 4)
        >>> version_lesser_2 = BaseVersion(2023, 3)
        >>> version_lesser_3 = BaseVersion(2023, 1, 5)
        >>> version_base < version_lesser_1, version_base < version_lesser_2, version_base < version_lesser_3
        (False, False, False)
        >>> version_same = Version.from_string("2023.3.5")
        >>> version_base < version_same
        False
        >>> version_short < 4  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        TypeError: '<' not supported between instances of 'Version' and 'int'
        >>> version_short < version_base
        True
        """
        if not isinstance(b, type(self)):
            return NotImplemented

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)  # type: ignore

        return self_parts < b_parts

    def __ge__(self, b: object) -> bool:
        """Implementation of ">=" internal type method for comparing values of same type

        >>> version_base = BaseVersion(2023, 3, 5)
        >>> version_short = BaseVersion(4)
        >>> version_greater_1 = BaseVersion(2023, 3, 5, 0)
        >>> version_greater_2 = BaseVersion(2024, 3, 5)
        >>> version_greater_3 = BaseVersion(2023, 3, 6)
        >>> version_base >= version_greater_1, version_base >= version_greater_2, version_base >= version_greater_3
        (False, False, False)
        >>> version_lesser_1 = BaseVersion(2023, 3, 4)
        >>> version_lesser_2 = BaseVersion(2023, 3)
        >>> version_lesser_3 = BaseVersion(2023, 1, 5)
        >>> version_base >= version_lesser_1, version_base >= version_lesser_2, version_base >= version_lesser_3
        (True, True, True)
        >>> version_same = Version.from_string("2023.3.5")
        >>> version_base >= version_same
        True
        >>> version_short >= 4  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        TypeError: '>=' not supported between instances of 'Version' and 'int'
        >>> version_short >= version_base
        False
        """
        if not isinstance(b, type(self)):
            return NotImplemented

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)  # type: ignore

        return self_parts > b_parts or self_parts == b_parts

    def __le__(self, b: object) -> bool:
        """Implementation of "<=" internal type method for comparing values of same type

        >>> version_base = BaseVersion(2023, 3, 5)
        >>> version_short = BaseVersion(4)
        >>> version_greater_1 = BaseVersion(2023, 3, 5, 0)
        >>> version_greater_2 = BaseVersion(2024, 3, 5)
        >>> version_greater_3 = BaseVersion(2023, 3, 6)
        >>> version_base <= version_greater_1, version_base <= version_greater_2, version_base <= version_greater_3
        (True, True, True)
        >>> version_lesser_1 = BaseVersion(2023, 3, 4)
        >>> version_lesser_2 = BaseVersion(2023, 3)
        >>> version_lesser_3 = BaseVersion(2023, 1, 5)
        >>> version_base <= version_lesser_1, version_base <= version_lesser_2, version_base <= version_lesser_3
        (False, False, False)
        >>> version_same = Version.from_string("2023.3.5")
        >>> version_base <= version_same
        True
        >>> version_short <= 4  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        TypeError: '<=' not supported between instances of 'Version' and 'int'
        >>> version_short <= version_base
        True
        """
        if not isinstance(b, type(self)):
            return NotImplemented

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)  # type: ignore

        return self_parts < b_parts or self_parts == b_parts

    def __repr__(self) -> str:
        """Representation internal method

        >>> v = Version.from_string("1.0.0.5322")
        >>> v
        BaseVersion(1, 0, 0, 5322)
        """
        return f"Version{self.__version_parts}"

    def __getitem__(self, key: Union[int, slice]) -> Union[int, Tuple[int, ...]]:
        """Getitem internal method

        This method allows for cherry-picking version item by "decimal place".

        >>> v = Version.from_string("2023.05.33.3242")
        >>> v[2]
        33
        >>> v[1]
        5
        >>> v[1:]
        (5, 33, 3242)
        >>> v[-3]
        5
        >>> v[-4]
        2023
        >>> v = BaseVersion(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
        >>> k = slice(3, 15, 2)
        >>> v[k]
        (4, 6, 8, 10, 12, 14)
        >>> v[54]  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        IndexError: ...
        >>> v["here be dragons"]  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        TypeError: ...
        >>> v[23.18:"Pete The Duck"]  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        TypeError: ...
        """
        return self.__version_parts[key]


if __name__ == "__main__":
    """
    Execute this file directly to run all the `doctest`s
    """
    import doctest

    doctest.testmod()
