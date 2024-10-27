from typing import TypeVar, Generic

T = TypeVar("T")


class PageResponse(Generic[T]):
    content: list[T]
    page: int
    size: int
    total: int

    def __init__(self, content: list[T], page: int, size: int, total: int):
        self.content = content
        self.page = page
        self.size = size
        self.total = total
