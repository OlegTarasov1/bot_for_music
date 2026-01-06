import logging
import aiohttp
import os


async def show_advert(user_id: int) -> None:
    """
    This sends ad to user by user's id in chat with the bot
    """
    async with aiohttp.ClientSession() as session:

        async with session.post(
            'https://api.gramads.net/ad/SendPost',
            headers={
                'Authorization': f'Bearer {os.getenv("AD_TOKEN")}',
                'Content-Type': 'application/json',
            },
            json={'SendToChatId': user_id},
        ) as response:

            if not response.ok:

                logging.error(str(await response.json()))




