import json
import os
from pathlib import Path

from pydantic import BaseModel, Field

from app.model.tool_definition import ToolDefinition


class EditFileInput(BaseModel):
    path: str = Field(
        description="The path to the file. If it doesn't exist, the tool creates it automatically.",
    )
    old_str: str = Field(
        description="Test to search for - must match exactly and must only have one match exactly."
    )
    new_str: str = Field(description="Text to replace old_str with.")


def _edit_file(input_data: str) -> tuple[str, None | str]:
    input_dict: dict[str, str] = json.loads(input_data)

    path: str = input_dict["path"]
    old_str: str = input_dict["old_str"]
    new_str: str = input_dict.get("new_str", "")

    if not path or old_str == new_str:
        return "", "Invalid input params"

    file_path: Path = Path(path)

    try:
        if not os.path.exists(file_path) and old_str == "":
            if file_path.parent != Path("."):
                file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(new_str)

            return f"Successfully created file {path}", None

        content: str = file_path.read_text()
        if old_str not in content and old_str != "":
            return "", "old_str not found in the file"

        new_content: str = content.replace(old_str, new_str)
        file_path.write_text(new_content)

        return f"Successfully edited file {path}", None
    except Exception as e:
        return "", str(e)


EDIT_FILE_DEFINITION: ToolDefinition = ToolDefinition(
    name="edit_file",
    description="""Make edits to a file.
    Replaces `old_str` with `new_str` in the given file. `old_str` and `new_str` MUST be different from each other.
    If the file specified with path does not exist, it will be created automatically.
    """,
    input_scheme=EditFileInput.model_json_schema(),
    function=_edit_file,
)
