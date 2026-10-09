
from dataclasses import dataclass


@dataclass
class Chunk:
    id: str
    document_id: str
    index: int
    text: str
    page_number: int | None = None
