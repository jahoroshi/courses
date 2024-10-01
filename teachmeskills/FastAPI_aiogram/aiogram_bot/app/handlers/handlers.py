from aiogram import Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.auth.token_auth import validate_access_token, get_access_token_by_telegram_id
from app.states import LinkState, NewNoteState
from settings import BASE_URL

# Initialize a router instance to handle bot commands and events
router = Router()


@router.message(Command(commands=['start']))
async def send_welcome(message: Message):
    """
    Sends a welcome message when the user initiates the bot with the /start command.

    Args:
    message -- incoming message containing user data.
    """
    await message.answer(
        f"Hello, {message.from_user.full_name}!\n"
        f"To link your Telegram account with your profile on our service, "
        f"please run the /link command."
    )


@router.message(Command(commands=['link']))
async def link_account(message: Message, state: FSMContext):
    """
    Initiates the process to link the user's Telegram account with the service account.

    Args:
    message -- incoming message containing user data.
    state -- finite state machine to manage the linking process.
    """
    await message.answer("Please enter your access token, which you can get from the website.")
    await state.set_state(LinkState.waiting_for_token)  # Set FSM state to wait for user input


@router.message(LinkState.waiting_for_token)
async def process_token(message: Message, state: FSMContext):
    """
    Processes the access token entered by the user and validates it.

    Args:
    message -- incoming message with the user's token.
    state -- FSM context for managing user states.
    """
    access_token = message.text.strip()
    async with aiohttp.ClientSession() as session:
        is_valid = await validate_access_token(session, access_token)
        if is_valid:
            # Link the Telegram account with the service account
            headers = {'Authorization': f'Bearer {access_token}'}
            payload = {'telegram_id': message.from_user.id}
            async with session.post(f'{BASE_URL}/api/v1/link_telegram', headers=headers, json=payload) as link_resp:
                if link_resp.status == 200:
                    await message.reply("Your Telegram account has been successfully linked!")
                else:
                    await message.reply("Failed to link the account. Please try again.")
        else:
            await message.reply("Invalid access token. Please check and try again.")
    await state.clear()  # Clear FSM state after processing


@router.message(Command(commands=['notes']))
async def get_notes(message: Message):
    """
    Fetches and displays the user's notes if the Telegram account is linked.

    Args:
    message -- incoming message containing user data.
    """
    telegram_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        access_token = await get_access_token_by_telegram_id(session, telegram_id)
        if access_token:
            headers = {'Authorization': f'Bearer {access_token}'}
            async with session.get(f'{BASE_URL}/api/v1/notes/', headers=headers) as resp:
                if resp.status == 200:
                    notes = await resp.json()
                    if notes:
                        notes_text = "\n".join([f"{note['id']}: {note['title']}" for note in notes])
                        await message.reply(f"Your notes:\n{notes_text}")
                    else:
                        await message.reply("You have no notes.")
                else:
                    await message.reply("Failed to retrieve notes.")
        else:
            await message.reply("Your account is not linked. Please use the /link command to link your account.")


@router.message(Command(commands=['new_note']))
async def new_note_start(message: Message, state: FSMContext):
    """
    Starts the process of creating a new note by requesting the note's title.

    Args:
    message -- incoming message containing user data.
    state -- FSM context for managing the new note process.
    """
    await state.set_state(NewNoteState.title)  # Set FSM state to wait for note title
    await message.reply("Please enter the title of your note.")


@router.message(NewNoteState.title)
async def new_note_title(message: Message, state: FSMContext):
    """
    Receives the title of the note and proceeds to request the content.

    Args:
    message -- incoming message containing the note title.
    state -- FSM context for managing the new note process.
    """
    await state.update_data(title=message.text)  # Store the title in FSM state
    await state.set_state(NewNoteState.content)  # Set FSM state to wait for note content
    await message.reply("Now, please enter the content of the note.")


@router.message(NewNoteState.content)
async def new_note_content(message: Message, state: FSMContext):
    """
    Receives the content of the note and proceeds to request the tags.

    Args:
    message -- incoming message containing the note content.
    state -- FSM context for managing the new note process.
    """
    await state.update_data(content=message.text)  # Store the content in FSM state
    await state.set_state(NewNoteState.tags)  # Set FSM state to wait for tags
    await message.reply("Enter tags for the note, separated by commas (or send '-' if no tags).")


@router.message(NewNoteState.tags)
async def new_note_tags(message: Message, state: FSMContext):
    """
    Receives the tags of the note and submits the new note to the service.

    Args:
    message -- incoming message containing tags or no tags.
    state -- FSM context for managing the new note process.
    """
    data = await state.get_data()
    title = data['title']
    content = data['content']
    tags_text = message.text
    tags = [] if tags_text.strip() == '-' else [tag.strip() for tag in tags_text.split(',')]  # Parse tags
    telegram_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        access_token = await get_access_token_by_telegram_id(session, telegram_id)
        if access_token:
            headers = {'Authorization': f'Bearer {access_token}'}
            note_payload = {
                'title': title,
                'content': content,
                'tags': tags
            }
            async with session.post(f'{BASE_URL}/api/v1/notes/', headers=headers, json=note_payload) as resp:
                if resp.status == 200:
                    await message.reply("Note successfully created!")
                else:
                    await message.reply("Failed to create the note.")
        else:
            await message.reply("Your account is not linked. Please use the /link command to link your account.")
    await state.clear()  # Clear FSM state after note creation


@router.message(Command(commands=['search']))
async def search_notes(message: Message):
    """
    Searches for notes by tag specified by the user.

    Args:
    message -- incoming message containing the search tag.
    """
    text = message.text.split()
    args = text[1:]  # Extract tag from command
    if not args:
        await message.reply("Please provide a tag to search for. Example:\n/search important")
        return
    tag_name = ' '.join(args)
    telegram_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        access_token = await get_access_token_by_telegram_id(session, telegram_id)
        if access_token:
            headers = {'Authorization': f'Bearer {access_token}'}
            params = {'tag_name': tag_name}
            async with session.get(f'{BASE_URL}/api/v1/notes/search/', headers=headers, params=params) as resp:
                if resp.status == 200:
                    notes = await resp.json()
                    if notes:
                        notes_text = "\n".join([f"{note['id']}: {note['title']}" for note in notes])
                        await message.reply(f"Notes with the tag '{tag_name}':\n{notes_text}")
                    else:
                        await message.reply(f"No notes found with the tag '{tag_name}'.")
                else:
                    await message.reply("Failed to search notes.")
        else:
            await message.reply("Your account is not linked. Please use the /link command to link your account.")
