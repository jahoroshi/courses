import chttp.render.tag_patterns as tags
import aiofiles
import re
from pathlib import Path
from chttp.services import catch_exception
CUR_DIR = Path(__file__).parent.parent.absolute()

@catch_exception
async def get_template(name):
    async with aiofiles.open(CUR_DIR / 'templates' / name) as file:
        return await file.read()

@catch_exception
async def render(template_name, request=None):

    html_content = await get_template(template_name)
    for pattern in tags.patterns:
        match = re.search(pattern[0], html_content)
        if match:
            base_template = await get_template(match.group(1))
            content = html_content.split(match.group(0))[1].strip()
            template = base_template.replace(pattern[1], content)
            return template

    return 'Empty template'