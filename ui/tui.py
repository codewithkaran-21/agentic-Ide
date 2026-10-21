from typing import Any , Tuple

from rich.console import Console 
from rich.theme import Theme
from rich.rule import Rule
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

AGENT_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "dim": "dim",
    "muted": "grey50",
    "border": "grey35",
    "highlight": "bold cyan",
    "user": "bright_blue bold",
    "assistant": "bright_white",
    "tool": "bright_magenta bold",
    "tool.read": "cyan",
    "tool.write": "yellow",
    "tool.shell": "magenta",
    "tool.network": "bright_blue",
    "tool.memory": "green",
    "tool.mcp": "bold cyan",
})


_console : Console | None = None

def get_console() -> Console:
    global _console
    if _console is None:
        _console = Console(theme=AGENT_THEME,highlight=False)

    return _console

class TUI:
    def __init__(self , console : Console | None = None) -> None:
        self.console = console or get_console()
        self._assistant_strem_open = False
        self._tool_args_by_call_id : dict[str,dict[str , Any]] = {}
    
    def begin_assistant(self) -> None:
        self.console.print()
        self.console.print(Rule(Text("Assistant",style="assistant")))
        self._assistant_strem_open = True

    def end_assistant(self) -> None:
        if self._assistant_strem_open:
            self.console.print()
            self._assistant_strem_open = False

    def stream_assistant_delta(self , content : str) -> None:
        self.console.print(content , end= "",markup=False)

    def _ordered_args(self , tool_name : str , args : dict[str,Any]) -> list[tuple]:
        _PREFERRED_ORDER = {
            "read_file" : ['path' , 'offset','limnit']
        }

        preferred = _PREFERRED_ORDER.get(tool_name,[])
        ordered : list[tuple[str,Any]] = []
        for key in preferred:
            if key in args:
                


    def _render_args_tab(tool_name : str , arguments : dict[str , Any]) -> Table:
        table = Table.grid(padding=(0,1))
        table.add_column(style="muted",justify="right",no_wrap=True)
        table.add_column(style="code",overflow="fold")

    def tool_call_start(self , call_id : str , name : str , arguments : dict[str,Any], tool_kind : str | None) -> None:
        self,self._tool_args_by_call_id[call_id] = arguments
        border_style = f"tool.{tool_kind}" if tool_kind else "tool"

        title = Text.assemble(
            ("🟡","muted"),
            (name , "tool"),
            (" ","muted"),
            (f"#{call_id[:8]}","muted")
        )

        panel = Panel(

        )

    