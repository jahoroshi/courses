import time
from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
from typing import Dict, Any, Callable, Awaitable


class RateLimitMiddleware(BaseMiddleware):
    """
    Middleware to limit the frequency of requests from a user in a Telegram bot.

    Args:
    limit -- Time in seconds between requests from the same user (default is 1 second).
    """

    def __init__(self, limit=1):
        super().__init__()
        self.rate_limit = limit  # Time limit in seconds between requests
        self.users = {}  # Dictionary to store the last request time for each user

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        """
        The main logic for rate limiting user requests.

        Args:
        handler -- The function to be executed if the rate limit is not exceeded.
        event -- The incoming update (message or callback query).
        data -- Additional data passed to the handler.

        Returns:
        The handler's result if the rate limit is respected; otherwise, a warning is sent to the user.
        """
        # Check if the event is a message
        if event.message:
            message = event.message
            user_id = message.from_user.id
        elif event.callback_query:
            # If it's a CallbackQuery (e.g., button click)
            message = event.callback_query.message
            user_id = event.callback_query.from_user.id
        else:
            # If the event is unsupported, just call the handler without changes
            return await handler(event, data)

        current_time = time.time()
        if user_id in self.users:
            # If the user has sent a request too recently, send a warning message
            if current_time - self.users[user_id] < self.rate_limit:
                await message.answer("Too many requests! Please wait a moment.")
                return  # Do not call the handler if rate limit exceeded

        # Update the last request time for the user
        self.users[user_id] = current_time
        return await handler(event, data)  # Call the handler if the rate limit is respected
