from abc import ABC, abstractmethod
from typing import Any

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, *, system: str | None = None) -> str:
        pass

    @abstractmethod
    def generate_json(self, prompt: str, schema: dict[str, Any], *, system: str | None = None) -> dict[str, Any]:
        pass