import json
import os
from typing import Optional

from pydantic import BaseModel, Field

from app.model.tool_definition import ToolDefinition


class ListFilesInput(BaseModel):
    path: Optional[str] = Field(
        description="Optional relative path to list files from. Defaults to the current working directory if not provided.",
        default=None,
    )


def _list_files(input_data: str) -> tuple[str, None | str]:
    input_dict: dict[str, str] = json.loads(input_data) if input_data else {}
    base_path: str = input_dict.get("path", ".")

    try:
        results: list[str] = []

        for root, _, file_names in os.walk(base_path):
            if base_path == ".":
                relative_dir: str = "."
            else:
                relative_dir: str = os.path.relpath(root, base_path)

            if relative_dir != ".":
                results.append(f"{relative_dir}/")

            for filename in file_names:
                if relative_dir == ".":
                    results.append(filename)
                else:
                    results.append(os.path.join(relative_dir, filename))

        return json.dumps(results), None
    except Exception as e:
        return "", str(e)


LIST_FILES_DEFINITION: ToolDefinition = ToolDefinition(
    name="list_files",
    description="List files and directories at a given path. If no path is provided, list files in the current working directory.",
    input_scheme=ListFilesInput.model_json_schema(),
    function=_list_files,
)
