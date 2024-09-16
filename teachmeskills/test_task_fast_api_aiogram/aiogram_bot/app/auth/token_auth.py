from settings import BASE_URL

async def get_access_token_by_telegram_id(session, telegram_id):
    """
    Retrieves access token by Telegram ID via an API request.

    Args:
    session -- asynchronous session to execute HTTP requests (e.g., aiohttp.ClientSession).
    telegram_id -- Telegram user ID to request the token.

    Returns:
    Access token if the request is successful, otherwise None.
    """
    payload = {'telegram_id': telegram_id}  # Prepare the data for the request
    async with session.post(f'{BASE_URL}/api/v1/get_token_by_telegram', json=payload) as token_resp:
        if token_resp.status == 200:
            token_data = await token_resp.json()  # Parse the response JSON
            return token_data['access_token']  # Return access token
        else:
            return None  # Return None if the request fails

async def validate_access_token(session, access_token):
    """
    Validates the access token by making an API request to check its status.

    Args:
    session -- asynchronous session to execute HTTP requests (e.g., aiohttp.ClientSession).
    access_token -- access token to be validated.

    Returns:
    True if the token is valid (HTTP status 200), otherwise False.
    """
    headers = {'Authorization': f'Bearer {access_token}'}  # Set authorization header with the token
    async with session.get(f'{BASE_URL}/api/v1/users/me', headers=headers) as resp:
        return resp.status == 200  # Return True if the response status is 200 (OK)
