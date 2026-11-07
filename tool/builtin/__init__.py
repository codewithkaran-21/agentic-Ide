from tool.builtin.edit_file import EditTool
from tool.builtin.list_dir import ListDirTool
from tool.builtin.read_file import ReadFileTool
from tool.builtin.shell import ShellTool
from tool.builtin.write_file import WriteFileTool

__all__  = ["ReadFileTool","WriteFileTool","EditTool","ShellTool","ListDirTool"]

def get_all_builtin_tools() -> list[type]:
    return [
        ReadFileTool,
        WriteFileTool,
        EditTool,
        ShellTool,
        ListDirTool
    ]