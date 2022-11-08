from typing import Optional, overload, TypeVar, Generic, Union


Arg = TypeVar("Arg")
Default = TypeVar("Default")


class command_parser(Generic[Arg]):
    def __init__(self, *args: Arg) -> None:
        self._args = [*args]

    @overload
    def get(self, index: int) -> Optional[Arg]:
        ...

    @overload
    def get(self, index: int, default: Default) -> Union[Arg, Default]:
        ...

    def get(self, index: int, default: Optional[Default] = None):
        try:
            return self._args[index]
        except IndexError:
            return default
