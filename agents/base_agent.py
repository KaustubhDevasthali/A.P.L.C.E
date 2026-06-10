from abc import ABC, abstractmethod

from contracts.agent_result import AgentResult
from contracts.task_specs import TaskSpecs
from providers.base import LLMProvider

class BaseAgent(ABC):
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, task_specs: TaskSpecs) -> AgentResult:
        pass