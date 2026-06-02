import json
from typing import Any

import anthropic
from anthropic.types import ToolParam
from dotenv import load_dotenv
from termcolor import colored

from app.model.tool_definition import ToolDefinition
from app.tool.delete_file_tool import DELETE_FILE_DEFINITION
from app.tool.edit_file_tool import EDIT_FILE_DEFINITION
from app.tool.list_files_tool import LIST_FILES_DEFINITION
from app.tool.read_file_tool import READ_FILE_DEFINITION
from app.util.helpers import Helpers

load_dotenv()


class ClaudeAgent:
    def __init__(self) -> None:
        self.client: anthropic.Anthropic = anthropic.Anthropic()
        self.tools: list[ToolDefinition] = [
            READ_FILE_DEFINITION,
            LIST_FILES_DEFINITION,
            EDIT_FILE_DEFINITION,
            DELETE_FILE_DEFINITION,
        ]

    def get_message(self) -> tuple[str, bool | str]:
        try:
            user_input: str = input()

            return user_input, bool(user_input)
        except EOFError as e:
            return "", str(e)
        except KeyboardInterrupt as e:
            return "", str(e)

    def run(self) -> None:
        conversation: list[dict[str, Any]] = []

        print("Chat with  Claude (use 'ctrl-d to quit')")

        read_user_input: bool = True
        while True:
            if read_user_input:
                print(
                    colored("Type your message: ", Helpers.hex_to_rgb("#1f1f1e")),
                    end="",
                )

                user_input, ok = self.get_message()

                if not ok:
                    print(
                        colored(
                            "\n\nGoodbye! Thanks for chatting.\n",
                            Helpers.hex_to_rgb("#d97757"),
                        )
                    )
                    break

                user_message: dict[str, Any] = {
                    "role": "user",
                    "content": [{"type": "text", "text": user_input}],
                }

                conversation.append(user_message)

            message = self.run_inference(conversation)
            conversation.append({"role": "assistant", "content": message.content})

            tool_results: list[dict[str, Any]] = []

            for content in message.content:
                if content.type == "text":
                    Helpers.print_agent_message(content.text)
                elif content.type == "tool_use":
                    result = self.execute_tool(
                        content.id, content.name, json.dumps(content.input)
                    )
                    tool_results.append(result)

            if not tool_results:
                read_user_input = True
                continue

            read_user_input = False
            conversation.append(
                {
                    "role": "user",
                    "content": tool_results,
                }
            )

    def execute_tool(self, tool_id: str, name: str, input_data: str) -> dict[str, Any]:
        for tool in self.tools:
            if tool.name == name:
                print(
                    colored(
                        f"tool: {name}({input_data})", Helpers.hex_to_rgb("#808080")
                    ),
                )
                result, error = tool.function(input_data)

                if error:
                    return {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": error,
                        "is_error": True,
                    }

                return {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result,
                    "is_error": False,
                }

        return {
            "type": "tool_result",
            "tool_use_id": tool_id,
            "content": "Tool not found",
            "is_error": False,
        }

    def run_inference(self, conversation: list[dict[str, Any]]):
        tools: list[ToolParam] = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_scheme,
            }
            for tool in self.tools
        ]

        return self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=conversation,
            tools=tools,
        )


def main():
    claude_agent: ClaudeAgent = ClaudeAgent()
    claude_agent.run()


if __name__ == "__main__":
    main()
