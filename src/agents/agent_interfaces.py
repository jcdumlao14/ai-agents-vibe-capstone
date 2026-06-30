from abc import ABC, abstractmethod
from typing import Any, Dict


class AgentInterface(ABC):
    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
