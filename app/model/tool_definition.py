from typing import Any, Callable


class ToolDefinition:
    def __init__(
        self,
        name: str,
        description: str,
        input_scheme: dict[str, Any],
        function: Callable[[str], tuple[str, None | str]],
    ) -> None:
        self.name = name
        self.description = description
        self.input_scheme = input_scheme
        self.function = function

    def __str__(self) -> str:
        return f"ToolDefinition(name={self.name}, description={self.description}, input_scheme={self.input_scheme}, function={self.function})"
