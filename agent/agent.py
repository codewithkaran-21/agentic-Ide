from typing import AsyncGenerator
from agent.events import AgentEvent
from client import LLMClient


class Agent:
    def __init__(self):
        self.client = LLMClient()

    async def _agentic_loop(self) -> AsyncGenerator[AgentEvent , None]:
        pass