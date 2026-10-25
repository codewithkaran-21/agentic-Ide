import os
from pathlib import Path

from pydantic import BaseModel , Field 


class ModelConfig(BaseModel):
    name : str = "mistralai/devstral-2512:free"
    temperature : float = Field(default=1,ge=0.0,le=2.0)
    context_window : int = 256_000

class Config(BaseModel):
    model : ModelConfig = Field(default_factory=ModelConfig)
    cwd :  Path = Field(default_factory=Path.cwd)

    max_turns : int = 100
    max_tool_output_tokens : int = 50000
    devloper_instructions : str | None = None
    user_instructions : str | None = None 
    debug : bool =  False 


    @property
    def api_key(self)->str:
        return os.environ.get("API_KEY")

    @property
    def base_url(self) -> str | None:
        return os.environ.get("BASE_URL")

    @property
    def model_name(self) -> str:
        return self.model.name

    @model_name.setter
    def model_name(self,value:str) -> None:
        self.model.name = value

    @property
    def temperature(self) -> float:
        return self.model.temperature

    @model_name.setter
    def model_name(self,value:str) -> None:
        self.model.temperature = value

    def validate(self) -> list[str]:
        error : list[str] = [] 

        if not self.api_key:
            error.appen("No API Key found, Set API_KEY environment variable")
        if not self.cwd.exists():
            error.append(f"Working directory does not exist {self.cwd}")

        return error


