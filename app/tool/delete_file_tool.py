import json
import os

from pydantic import BaseModel, Field

from app.model.tool_definition import ToolDefinition


class DeleteFileInput(BaseModel):
    path: str = Field(description="The path to the file to delete.")


def _delete_file(input_data: str) -> tuple[str, None | str]:
    try:
        input_dict: dict[str, str] = json.loads(input_data)
        path: str = input_dict["path"]

        if not path:
            return "", "Invalid input params"

        if not os.path.exists(path):
            return "", "File not found"

        os.remove(path)

        return f"Successfully deleted file {path}", None
    except Exception as e:
        return "", str(e)


DELETE_FILE_DEFINITION: ToolDefinition = ToolDefinition(
    name="delete_file",
    description="""Delete a file from the working directory.
    Use this when you want to remove a file from the working directory.
    """,
    input_scheme=DeleteFileInput.model_json_schema(),
    function=_delete_file,
)
