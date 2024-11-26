import aiohttp
from typing import List

from src.config import settings
from .contracts import Result


async def fetch_repository_contents(repo_url: str) -> Result:
    owner_repo = repo_url.rstrip('/').split('/')[-2:]
    repo_api_url = f"{settings.integrations.github.api.github.api_url}/repos/{owner_repo[0]}/{owner_repo[1]}/contents"

    headers = {
        "Authorization": f"token {settings.integrations.github.api.github.api_key}",
        "Accept": f"{settings.integrations.github.api.github.accept}",
    }

    async with aiohttp.ClientSession() as session:
        code_files = []
        await fetch_files_recursively(session, repo_api_url, headers, code_files)

    # Fetch file contents
    code_contents = ""
    file_contents = []
    for file_info in code_files:
        file_url = file_info['download_url']
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    code_contents += f"\n\n# File: {file_info['path']}\n"
                    file_contents.append(file_info['path'])
                    code_contents += await response.text()

    return Result(code_contents=code_contents, file_contents=file_contents)


async def fetch_files_recursively(session, url: str, headers: dict, code_files: List[dict]):
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            raise Exception(f"Failed to fetch repository contents from {url}")
        contents = await response.json()

    for item in contents:
        if item['type'] == 'file' and item['name'].endswith(('.py', '.js', '.java', '.cpp')):
            code_files.append(item)
        elif item['type'] == 'dir':
            await fetch_files_recursively(session, item['url'], headers, code_files)
