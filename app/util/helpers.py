from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

__CONSOLE_LOGGER__ = Console()


class Helpers:
    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        hex_color: str = hex_color.lstrip("#")

        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def print_agent_message(markdown_text: str):
        __CONSOLE_LOGGER__.print(
            Panel(
                Markdown(markdown_text),
                title="Claude Code",
                border_style="#d97757",
            )
        )
