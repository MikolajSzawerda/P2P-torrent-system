import dataclasses
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class FileId:
    name: str
    hash: str


@dataclass(eq=True, frozen=True)
class File:
    SEGMENT_SIZE_BYTES = 40000

    id: FileId
    size: int

    @property
    def segments(self) -> int:
        add_one = 1 if self.size % self.SEGMENT_SIZE_BYTES > 0 else 0
        return self.size // self.SEGMENT_SIZE_BYTES + add_one

    @classmethod
    def from_dict(cls, data: dict) -> "File":
        name = data.get("name")
        hash_ = data.get("hash")
        size = data.get("size")

        if any(param is None for param in (name, hash_, size)):
            raise TypeError(f"{data} can not be serialized to {cls.__name__}")

        return cls(id=FileId(name=name, hash=hash_), size=size)

    def asdict(self) -> dict:
        return dataclasses.asdict(self)


@dataclass(eq=True, frozen=True)
class Command:
    route: str
    payload: dict

    @classmethod
    def from_dict(cls, data: dict) -> "Command":
        route = data.get("route")
        payload = data.get("payload", {})

        if route is None:
            raise TypeError(f"{data} can not be serialized to {cls.__name__}")

        return cls(route=route, payload=payload)
