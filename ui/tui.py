from pathlib import Path
import re
from typing import Any , Tuple
from rich import box
from rich.console import Console 
from rich.theme import Theme
from rich.rule import Rule
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

from utils.paths import dispaly_path_rel_to_cwd, resolve_path

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
        self.path = Path.cwd()
    
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
        seen = set()
        for key in preferred:
            if key in args:
                ordered.append((key , args[key]))
                seen.add(key)

        remaining_keys = set(args.keys() - seen)
        ordered.extend((key , args[key]) for key in remaining_keys)

        return ordered



    def _render_args_tab(self, tool_name : str , args : dict[str , Any]) -> Table:
        table = Table.grid(padding=(0,1))
        table.add_column(style="muted",justify="right",no_wrap=True)
        table.add_column(style="code",overflow="fold")

        for key , value in self._ordered_args(tool_name,args):
            table.add_row(key , value)

        return table

    def _extract_read_file_code(self , text : str) -> tuple[int , str] | None:
        body = text
        header_match = re.match(r"Showing lines (\d+)-(\d+) of (\d+)\n\n",text)
        if header_match:
            body = text[header_match.end() :]

        code_lines : list[str] = []
        start_lines : int | None = None

        for line in body.splitlines():
            m = re.match(r"")



    def tool_call_complete(self , call_id : str , name : str , tool_kind : str | None,
                          success: bool , output : str , error : str | None,
                           metadata : dict[str,Any] | None,
                           truncated : bool) -> None:
        
        border_style = f"tool.{tool_kind}" if tool_kind else "tool"
        status_icon = '✔️' if success else '✖️'
        status_style = "success" if success else "error"
        title = Text.assemble(
            ("🟡","muted"),
            (name , "tool"),
            (" ","muted"),
            (f"#{call_id[:8]}","muted")
        )

        display_args = dict(arguments)
        for key in ('path','cwd'):
            val = display_args.get(key)
            if isinstance(val , str) and self.cwd:
                display_args[key] = str(dispaly_path_rel_to_cwd(val,self.cwd))

        panel = Panel(
            self._render_args_table(name,display_args) if display_args else Text('no-args' , style="muted"),
            title=title,
            title_align='left',
            subtitle_align='right',
            subtitle=Text('running',style="muted"),
            border_style=border_style,
            box=box.ROUNDED,
            padding=(1,2),
        )

    