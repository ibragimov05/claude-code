import json

from pydantic import BaseModel, Field

from app.model.tool_definition import ToolDefinition


class ReadFileInput(BaseModel):
    path: str = Field(
        description="The relative path of a file in the working directory"
    )


def _read_file(input_data: str) -> tuple[str, None | str]:
    input_dict: dict[str, str] = json.loads(input_data)
    path: str = input_dict["path"]

    try:
        with open(path, "r") as file:
            content: str = file.read()

        return content, None
    except Exception as e:
        return "", str(e)


READ_FILE_DEFINITION: ToolDefinition = ToolDefinition(
    name="read_file",
    description="Read the contents of a given relative path. Use this when you want to see what's inside a file. Do not use this with directory names.",
    input_scheme=ReadFileInput.model_json_schema(),
    function=_read_file,
)
