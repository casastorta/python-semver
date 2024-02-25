from typing import Iterable
from typing import Tuple


class Version:
    """
    This is a basic Python Semantic Version library.

    >>> ver = Version(3, 4, 5)
    """

    def __init__(self, *args: int) -> None:
        """Constructor

        >>> v = Version(2023, 3, 5)
        >>> v  # doctest: +ELLIPSIS
        <__main__.Version object at ...>
        """
        self.__fill_parts(*args)

    def __fill_parts(self, *args: int) -> None:
        """
        Fills out all version parts into class' internal tuple

        >>> v = Version("a", 3, 4)  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        TypeError: Parts of semantic version must be all integer
        """
        __version_parts: list = []
        for part in args:
            if not isinstance(part, int):
                raise TypeError("Parts of semantic version must be all integer")
            __version_parts.append(part)
        self.__version_parts: Tuple[int] = tuple(__version_parts)

    @staticmethod
    def from_string(version: str) -> "Version":
        """Create semantic version directly from the string

        >>> vs = Version.from_string("2023.03.05")
        >>> vs  # doctest: +ELLIPSIS
        <__main__.Version object at ...>
        >>> v = Version.from_string("3.4.5.abc")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: invalid literal for int() with base 10: 'abc'
        """
        parts: list = [int(v) for v in version.split(".")]
        return Version(*parts)

    def __iter__(self) -> Iterable[int]:
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
        """Implementation of "equals" internal type method for comparing values of same type

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
        """Implementation of "greaterthan" internal type method for comparing values of same type

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
        """Implementation of "lesserthan" internal type method for comparing values of same type

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
        """Implementation of "greaterorequalthan" internal type method for comparing values of same type

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
        """Implementation of "lesserorequalthan" internal type method for comparing values of same type

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


if __name__ == "__main__":
    """
    Execute this file directly to run all the `doctest`s
    """
    import doctest

    doctest.testmod()
