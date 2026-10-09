
from dataclasses import dataclass, field


@dataclass
class Document:
    id: str
    title: str
    content: str
    source: str
    date: str
    pages: list[str] = field(default_factory=list)
