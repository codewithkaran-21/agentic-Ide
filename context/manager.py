from prompts.system import get_system_prompt


class ConetxtManager:
    def __init__(self) -> None:
        self._system_prompt = get_system_prompt()
        
