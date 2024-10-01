import aiofiles
from pathlib import Path

CUR_DIR = Path(__file__).parent.absolute()


async def homepage(request):
    async with aiofiles.open(CUR_DIR / "templates" / "base.html") as file:
        return await file.read()
