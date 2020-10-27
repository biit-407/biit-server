import asyncio
import os
from datetime import datetime
from typing import List
import discord


def mock_dev(return_value):
    """
    Decorator for mocking the return value of a function when
    in a dev environment

    Args:
        return_value (any): the value to have the function return
            when run from inside a dev environment
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            stage = os.getenv("STAGE", "dev")
            if stage == "dev":
                return return_value

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def utcToInt(availability: List[List[str]]) -> List[List[int]]:
    """Converts POSIX time into int time

    Args:
        availability (List[List[str]]): List of POSIX times

    Returns:
        List[List[int]]: List of Int times
    """
    intTimes = []
    for s0, s1 in availability:
        s0datetime = datetime.utcfromtimestamp(s0)
        s1datetime = datetime.utcfromtimestamp(s1)
        s0time = s0datetime.hour + s0datetime.weekday() * 24
        s1time = s1datetime.hour + s1datetime.weekday() * 24
        intTimes += (s0time, s1time)
    return intTimes


__TOKEN = os.getenv('DISCORD_BOT', 'awwgeezrickidkaboutthis')
__BACKEND_CHANNEL_ID = 748341103173828689
__GENERAL_CHANNEL_ID = 747450218836000791
__FRONTEND_CHANNEL_ID = 748341084794388530
__LOGGERS_ID = 770727483585724485

client = discord.Client()


@client.event
async def on_ready():
    channel_id, message = client.__dict__['__biit_server_message__']
    
    channel = client.get_channel(channel_id)

    if channel == None:
        raise KeyboardInterrupt(f'Failed to send message [{message}] to server channel [{channel_id}].')
    
    await channel.send(message)
    
    await client.close()


def _send_discord_message(bot_token: str, channel: int, message: str):
    if 'message_queue' in client.__dict__:
        client.__dict__['__biit_server_message__'] = (channel, message)
    else:
        client.__dict__['__biit_server_message__'] = (channel, message)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.login(bot_token))
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        print ('Exception was raised, ending loop function.')
        loop.run_until_complete(client.logout())
        # cancel all tasks lingering
    finally:
        loop.close()

def send_biit_general(message: str):
    """
    Sends a message to the biit general discord

    Args:
        message (str): The message to send the discord channel
    """
    _send_discord_message(__TOKEN, __GENERAL_CHANNEL_ID, message)


def send_biit_backend(message: str):
    """
    Sends a message to the biit backend discord

    Args:
        message (str): The message to send the discord channel
    """
    _send_discord_message(__TOKEN, __BACKEND_CHANNEL_ID, message)

def send_biit_frontend(message: str):
    """
    Sends a message to the biit frontend discord

    Args:
        message (str): The message to send the discord channel
    """
    _send_discord_message(__TOKEN, __FRONTEND_CHANNEL_ID, message)

def send_biit_loggers(message: str):
    """
    Sends a message to the biit loggers discord

    Args:
        message (str): The message to send the discord channel
    """
    _send_discord_message(__TOKEN, __LOGGERS_ID, message)