from typing import Iterator, Union
from typing import Tuple


class Version:
    """
    This is a minimal Python Semantic Version library.

    Values can be passed as arbitrary number of `int` numbers, for example:

    >>> v = Version(1, 0, 0)
    >>> str(v)
    '1.0.0'

    Or as strings, which will be converted to versions:

    >>> v = Version.from_string("1.0.0.5322")
    >>> str(v)
    '1.0.0.5322'
    >>> v
    Version(1, 0, 0, 5322)

    Implementation of comparison operators (`__lt__`, `__gt__`, `__le__`, `__ge__`) allows for
    sorting operations to work. For example:

    >>> versionslist = [
    ...     Version.from_string("1.0.0"), Version.from_string("1.0.1"),
    ...     Version.from_string("0.9.95"), Version(0, 8, 97),
    ...     Version(2024, 2, 25, 101), Version(1, 0, 0, 0)]
    >>> sorted(versionslist)
    [Version(0, 8, 97), Version(0, 9, 95), Version(1, 0, 0), Version(1, 0, 0, 0), Version(1, 0, 1), Version(2024, 2, 25, 101)]
    >>> sorted(versionslist, reverse=True)
    [Version(2024, 2, 25, 101), Version(1, 0, 1), Version(1, 0, 0, 0), Version(1, 0, 0), Version(0, 9, 95), Version(0, 8, 97)]
    """

    def __init__(self, *args: int) -> None:
        """Constructor

        >>> v = Version(2023, 3, 5)
        >>> v
        Version(2023, 3, 5)
        """
        self.__fill_parts(*args)

    def __fill_parts(self, *args: int) -> None:
        """
        Fills out all version parts into class' internal tuple

        >>> v = Version("a", 3, 4)  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        TypeError: Parts of semantic version must be all integer, 'a' passed
        """
        __version_parts: list = []
        for part in args:
            if not isinstance(part, int):
                raise TypeError(
                    f"Parts of semantic version must be all integer, '{part}' passed"
                )
            __version_parts.append(part)
        self.__version_parts: Tuple[int] = tuple(__version_parts)

    @staticmethod
    def from_string(version: str) -> "Version":
        """Create semantic version directly from the string

        >>> vs = Version.from_string("2023.03.05")
        >>> vs  # doctest: +ELLIPSIS
        Version(2023, 3, 5)
        >>> v = Version.from_string("3.4.5.abc")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: invalid literal for int() with base 10: 'abc'
        """
        parts: list = [int(v) for v in version.split(".")]
        return Version(*parts)

    def __iter__(self) -> Iterator[int]:
        """Iterate through version parts, used for casting into list, tuple, etc...

        >>> v = Version(2023, 3, 5)
        >>> vparts = tuple(v)
        >>> vparts
        (2023, 3, 5)
        """
        for part in self.__version_parts:
            yield part

    def __len__(self) -> int:
        """Returns number of version items

        >>> len(Version(1, 2, 3))
        3
        >>> len(Version(1))
        1
        >>> len(Version.from_string("2023.03.04.05555.0"))
        5
        """
        return len(self.__version_parts)

    def __str__(self) -> str:
        """String representation of semantic version

        >>> v = Version(2023, 3, 5)
        >>> vs = Version.from_string("2023.03.05")
        >>> str(vs), str(v)
        ('2023.3.5', '2023.3.5')
        """
        return ".".join([str(p) for p in self.__version_parts])

    def __eq__(self, b: object) -> bool:
        """Implementation of "==" internal type method for comparing values of same type

        >>> basev = Version(2023, 3, 5)
        >>> altv = Version.from_string("2024.03.05")
        >>> zerov = Version(2023, 3, 5, 0)
        >>> samev = Version.from_string("2023.03.05")
        >>> basev == altv
        False
        >>> basev == samev
        True
        >>> basev == zerov
        False
        """
        self.__validate(b)

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)

        return self_parts == b_parts

    def __gt__(self, b: object) -> bool:
        """Implementation of ">" internal type method for comparing values of same type

        >>> basev = Version(2023, 3, 5)
        >>> greaterv1 = Version(2023, 3, 5, 0)
        >>> greaterv2 = Version(2024, 3, 5)
        >>> greaterv3 = Version(2023, 3, 6)
        >>> basev > greaterv1, basev > greaterv2, basev > greaterv3
        (False, False, False)
        >>> lesserv1 = Version(2023, 3, 4)
        >>> lesserv2 = Version(2023, 3)
        >>> lesserv3 = Version(2023, 1, 5)
        >>> basev > lesserv1, basev > lesserv2, basev > lesserv3
        (True, True, True)
        >>> samev = Version.from_string("2023.3.5")
        >>> basev > samev
        False
        """
        self.__validate(b)

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)

        return self_parts > b_parts

    def __lt__(self, b: object) -> bool:
        """Implementation of "<" internal type method for comparing values of same type

        >>> basev = Version(2023, 3, 5)
        >>> greaterv1 = Version(2023, 3, 5, 0)
        >>> greaterv2 = Version(2024, 3, 5)
        >>> greaterv3 = Version(2023, 3, 6)
        >>> basev < greaterv1, basev < greaterv2, basev < greaterv3
        (True, True, True)
        >>> lesserv1 = Version(2023, 3, 4)
        >>> lesserv2 = Version(2023, 3)
        >>> lesserv3 = Version(2023, 1, 5)
        >>> basev < lesserv1, basev < lesserv2, basev < lesserv3
        (False, False, False)
        >>> samev = Version.from_string("2023.3.5")
        >>> basev < samev
        False
        """
        self.__validate(b)

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)

        return self_parts < b_parts

    def __ge__(self, b: object) -> bool:
        """Implementation of ">=" internal type method for comparing values of same type

        >>> basev = Version(2023, 3, 5)
        >>> greaterv1 = Version(2023, 3, 5, 0)
        >>> greaterv2 = Version(2024, 3, 5)
        >>> greaterv3 = Version(2023, 3, 6)
        >>> basev >= greaterv1, basev >= greaterv2, basev >= greaterv3
        (False, False, False)
        >>> lesserv1 = Version(2023, 3, 4)
        >>> lesserv2 = Version(2023, 3)
        >>> lesserv3 = Version(2023, 1, 5)
        >>> basev >= lesserv1, basev >= lesserv2, basev >= lesserv3
        (True, True, True)
        >>> samev = Version.from_string("2023.3.5")
        >>> basev >= samev
        True
        """
        self.__validate(b)

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)

        return self_parts > b_parts or self_parts == b_parts

    def __le__(self, b: object) -> bool:
        """Implementation of "<=" internal type method for comparing values of same type

        >>> basev = Version(2023, 3, 5)
        >>> greaterv1 = Version(2023, 3, 5, 0)
        >>> greaterv2 = Version(2024, 3, 5)
        >>> greaterv3 = Version(2023, 3, 6)
        >>> basev <= greaterv1, basev <= greaterv2, basev <= greaterv3
        (True, True, True)
        >>> lesserv1 = Version(2023, 3, 4)
        >>> lesserv2 = Version(2023, 3)
        >>> lesserv3 = Version(2023, 1, 5)
        >>> basev <= lesserv1, basev <= lesserv2, basev <= lesserv3
        (False, False, False)
        >>> samev = Version.from_string("2023.3.5")
        >>> basev <= samev
        True
        """
        self.__validate(b)

        self_parts: tuple = self.__version_parts
        b_parts: tuple = tuple(b)

        return self_parts < b_parts or self_parts == b_parts

    def __validate(self, b: object) -> None:
        """Make base validation for all internal comparison methods - whether types and lengths are the same

        >>> basev = Version(2023, 3, 5)
        >>> samev = Version(2023, 3, 5)
        >>> basev == samev
        True
        >>> basev == 5.53  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        NotImplementedError: Can compare Version only with another Version
        >>> basev > 5.53  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        NotImplementedError: Can compare Version only with another Version
        >>> basev < 5.53  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        NotImplementedError: Can compare Version only with another Version
        >>> basev >= 5.53  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        NotImplementedError: Can compare Version only with another Version
        >>> basev <= 5.53  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        NotImplementedError: Can compare Version only with another Version
        """
        if not isinstance(b, type(self)):
            raise NotImplementedError("Can compare Version only with another Version")

    def __repr__(self) -> str:
        """Representation internal method

        >>> v = Version.from_string("1.0.0.5322")
        >>> v
        Version(1, 0, 0, 5322)
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
        >>> v = Version(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
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
