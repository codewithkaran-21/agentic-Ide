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
     

