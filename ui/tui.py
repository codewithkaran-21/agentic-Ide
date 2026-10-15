from rich.console import Console 
from rich.theme import Theme

AGENT_THEME = Theme({
    "info":"cyan",
    "warning":"yellow",
    "error": "bright_red_bold",
    "success":"green",
    "dim":"dim",
    "muted":"grey50",
    "border":"grey35",
    "highlight":"bold cyan",
    "user": "bright_blue bold",
    "assistant":"bright_white",
    "tool":"bright_magenta bold",
    "tool.read" : "cyan",
    "tool.write":"yellow",
    "tool.shell":"magenta",
    "tool.network":"bright_blue",
    "tool.memory" : "green",
    "tool.mcp" : "bright cyan"
})


_console : Console | None = None

def get_console() -> Console:
    if _console is None:
        _console = Console(theme=AGENT_THEME,highlight=False)

    return _console

class TUI:
    def __init__(self , console : Console | None = None) -> None:
        self.console = console or get_console()