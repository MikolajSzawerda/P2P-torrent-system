from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class FileId:
    name: str
    md5: str


@dataclass(eq=True, frozen=True)
class File:
    id: FileId
    size: int


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
