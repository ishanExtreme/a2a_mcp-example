import logging

from collections.abc import AsyncIterable
from typing import Any, Literal

import httpx

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables.config import (
    RunnableConfig,
)
from langchain_core.tools import tool  # type: ignore
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent  # type: ignore
from pydantic import BaseModel
from langchain_mcp_adapters.client import MultiServerMCPClient

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools




logger = logging.getLogger(__name__)

memory = MemorySaver()


# @tool
# def execute_linux_command(
#     command_to_execute: str,
# ):
#     """Use this to execute the linux command on terminal

#     Args:
#         command_to_execute: Linux command to be executed on terminal

#     Returns:
#         A string containing the output of the command
#     """
#     return f"Output of command {command_to_execute} is hello!"

class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str


class LinuxAgent:
    """Linux Agent Example."""

    SYSTEM_INSTRUCTION = (
        'You are a specialized assistant for executing linux command from simple english user query. '
        "Your purpose is to use the given tools to run the appropriate command and display the output "
        "If any input is required or user has given incomplete instruction for completing the command ask it to user"
        'If the user asks about anything other than running linux commands '
        'politely state that you cannot help with that topic and can only assist with running linux command queries. '
        'Do not attempt to answer unrelated questions or use tools for other purposes.'
    )

    RESPONSE_FORMAT_INSTRUCTION: str = (
        'Select status as completed if the request is complete'
        'Select status as input_required if the input is a question to the user'
        'Set response status to error if the input indicates an error'
    )

    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o", temperature=0.5)
        self.graph = None
        

    async def invoke(self, query: str, sessionId: str) -> dict[str, Any]:
        async with MultiServerMCPClient(
            {
                "linux": {
                    # Ensure your start your weather server on port 8000
                    "url": "http://localhost:8000/sse",
                    "transport": "sse",
                }
            }
        ) as client:
            self.graph = create_react_agent(
                self.model,
                tools=client.get_tools(),
                checkpointer=memory,
                prompt=self.SYSTEM_INSTRUCTION,
                response_format=(self.RESPONSE_FORMAT_INSTRUCTION, ResponseFormat),
                debug=True
            )
            config: RunnableConfig = {'configurable': {'thread_id': sessionId}}
            await self.graph.ainvoke({'messages': [('user', query)]}, config)
            return self.get_agent_response(config)

    async def stream(
        self, query: str, sessionId: str
    ) -> AsyncIterable[dict[str, Any]]:
        pass

    def get_agent_response(self, config: RunnableConfig) -> dict[str, Any]:
        current_state = self.graph.get_state(config)

        structured_response = current_state.values.get('structured_response')
        if structured_response and isinstance(
            structured_response, ResponseFormat
        ):
            if structured_response.status in {'input_required', 'error'}:
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': structured_response.message,
                }
            if structured_response.status == 'completed':
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': structured_response.message,
                }

        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': 'We are unable to process your request at the moment. Please try again.',
        }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
