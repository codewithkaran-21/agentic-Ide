import uuid

from ddgs import DDGS
from pydantic import BaseModel , Field
from config.config import Config
from tool.base import Tool, ToolInvocation, ToolKind, ToolResult


class TodoParams(BaseModel):
    action : str = Field(..., description = "Action : 'add', 'complete', 'list', 'clear" )
    id : str | None = Field(None , description="Todo ID (for complete)")
    content : str | None = Field(None , description="Todo content (for add)")


class TodoTool(Tool):

    name = "todos"
    description = "Manage a task list for the current session. Use this to track progress"
    kind = ToolKind.MEMORY
    schema = TodoParams

    def __init__(self , config : Config) -> None:
        super.__init__(config)
        self._todos : dict[str,str] = {}

    async def execute(self , invocation : ToolInvocation) -> ToolResult:
        params = TodoParams(**invocation.params)

        if params.action.lower() == "add":
            if not params.content:
                return ToolResult.error_result(f"`content` required for `add` action")
            todo_id = str(uuid.uuid4())[:8]
            self._todos[todo_id] = params.content
            return ToolResult.success_result(f"Added todo [{todo_id}] : {params.content}")
        
        elif params.action.lower() == "complete":
            if not params.id:
                return ToolResult.error_result("`id` required for `complete` action")
            if params.id not in self._todos:
                return ToolResult.error_result(f"Todo Not Found: {params.id}")  

            content = self._todos.pop(params.id)
            return ToolResult.success_result(f"Completed todo [{params.id}] : {content}")

        elif params.action.lower() == "list":
            if not self._todos:
                return ToolResult.error_result(f"No Todos")

            lines = ["Todos:"]

            for todo_id , content in self._todos.items():
                lines.append(f"  [{todo_id}] {content}")
            
            return ToolResult.success_result(f"\n".join(lines))

        elif params.action.lower() == "clear":
            count = len(self._todos)
            self._todos.clear()
            return ToolResult.success_result(f"Cleared {count} todos")
        else:
            return ToolResult.error_result(f"Unknown action: {params.action}")


        if not results:
            return ToolResult.error_result(f"No results for: {params.query}",
                                           metadata = {
                                               "results":0,
                                           })

        output_lines = [f"Search results for: {params.query}"]

        for i , result in enumerate(results,start=1):
            output_lines.append(f"{i}. Title: {result["title"]}")
            output_lines.append(f"   URL: {result['href']}")
            if result.get('body'):
                output_lines.append(f"   Snippet: {result['body']}")

            output_lines.append("")

        return ToolResult.success_result(
            "\n".join(output_lines),
            metadata = { 
                'results' : len(results)
            }
        )
