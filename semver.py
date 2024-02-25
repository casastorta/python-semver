from typing import Iterable
from typing import Tuple

class Version:
    """
    This is a basic Python Semantic Version library.

    >>> ver = Version(3, 4, 5)
    >>> ver_exception = Version("3", 4, 5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Parts of semantic version must be all integer
    """

    def __init__(self, *args: int) -> None:
        """Constructor

        >>> v = Version(2023, 3, 5)
        >>> v  # doctest: +ELLIPSIS
        <__main__.Version object at ...>
        """
        self.__fill_parts(*args)

    def __fill_parts(self, *args: int) -> None:
        __version_parts: list = []
        for part in args:
            if not isinstance(part, int):
                raise TypeError("Parts of semantic version must be all integer")
            __version_parts.append(part)
        self.__version_parts: Tuple[int] = tuple(__version_parts)

    @staticmethod
    def from_string(version: str) -> "Version":
        """Create semantic version directly from string

        >>> vs = Version.from_string("2023.03.05")
        >>> vs  # doctest: +ELLIPSIS
        <__main__.Version object at ...>
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
        """Implementation of __eq__ internal type method for comparing values of same type

        >>> basev = Version(2023, 3, 5)
        >>> altv = Version.from_string("2024.03.05")
        >>> samev = Version.from_string("2023.03.05")
        >>> basev == altv
        False
        >>> basev == samev
        True
        >>> basev == 5.53  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        TypeError: Can compare Version only with another Version
        """
        if not isinstance(b, type(self)):
            raise TypeError("Can compare Version only with another Version")

        # Different lengths default to different versions, no assumptions made about
        # "N.N.0.0.0.0" vs "N.N" here
        if len(self) != len(b):
            return False

        b_parts: tuple = tuple(b)
        for place in range(0, len(self)):
            if self.__version_parts[place] != b_parts[place]:
                return False

        return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
