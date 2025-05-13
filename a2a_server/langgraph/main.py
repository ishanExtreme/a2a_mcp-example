import logging
import os
import asyncio

import click

from agent import LinuxAgent
from task_manager import AgentTaskManager
from google_a2a.common.server import A2AServer
from google_a2a.common.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from google_a2a.common.utils.push_notification_auth import PushNotificationSenderAuth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(host, port):
    """Starts the Linux Agent server."""
    try:
    
        capabilities = AgentCapabilities(streaming=False, pushNotifications=True)
        skill = AgentSkill(
            id='run_linux_command',
            name='Run Linux Command',
            description='Helps with running linux command from simple english query',
            tags=['run linux command'],
            examples=['Display all files on my desktop'],
        )
        agent_card = AgentCard(
            name='Linux Agent',
            description='Helps with running linux command from simple english query',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            defaultInputModes=LinuxAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=LinuxAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        notification_sender_auth = PushNotificationSenderAuth()
        notification_sender_auth.generate_jwk()
        agent = LinuxAgent()
        # try:
        #     loop = asyncio.get_event_loop()
        # except:
        #     loop = asyncio.new_event_loop()

        # loop.run_until_complete(agent.initialize_agent())
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(
                agent= agent,
                notification_sender_auth=notification_sender_auth,
            ),
            host=host,
            port=port,
        )

        server.app.add_route(
            '/.well-known/jwks.json',
            notification_sender_auth.handle_jwks_endpoint,
            methods=['GET'],
        )

        logger.info(f'Starting server on {host}:{port}')
        server.start()
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)



main("localhost", 10000)

