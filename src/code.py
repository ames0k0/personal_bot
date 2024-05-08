"""
https://github.com/krau/kmua-bot/blob/v2/kmua/callbacks/waifu.py#L131-L133
                                                                #L131-L133  <- scope
https://raw.githubusercontent.com/krau/kmua-bot/v2/kmua/callbacks/waifu.py  <- content


### Output
```python
if user.id == waifu.married_waifu_id:
    text = f"{common.mention_markdown_v2(user)}, 你和 {common.mention_markdown_v2(waifu)} 已经结婚了哦, 还想娶第二遍嘛?"
    waifu_markup = None
```
"""
import os
from re import findall
from urllib.parse import urlparse, urlunparse, ParseResult
from urllib.request import urlopen

from enum import Enum

class HostEnum(str, Enum):
  github = 'github.com'


SUPPORTED_HOSTS = (
  HostEnum.github.value,
)
HOST_SWAP = {
  HostEnum.github.value: 'raw.githubusercontent.com',
}
URL_PATH_CLEAN = {
  HostEnum.github.value: (
    'blob/',
  ),
}
CODE_MARKDOWN = {
  '.py': 'python',
}


def _github_code_scope(
    scope: str, scope_delimiter: str = '-'
) -> tuple[int, int]:
  scopes = scope.split(scope_delimiter)
  for idx, scope in enumerate(scopes):
    line = findall('\d+', scope)
    if not line:
      continue
    scopes[idx] = int(line.pop())
  scopes[0] = scopes[0] - 1
  return scopes


CODE_SCOPE_PARSER = {
  HostEnum.github.value: _github_code_scope
}


def get_code(target: str) -> str:
  """ Returns str: code or error message
  """
  target_url_components = urlparse(target)
  if target_url_components.netloc not in SUPPORTED_HOSTS:
    return f"NotSupportedHost: {target_url_components.netloc}"

  new_target_path = target_url_components.path
  for path_clean in URL_PATH_CLEAN[target_url_components.netloc]:
    new_target_path = new_target_path.replace(path_clean, '')

  code_scopes = target_url_components.fragment
  if not code_scopes:
    return 'Not set a code scope (lines to read)'

  code_scopes = CODE_SCOPE_PARSER[target_url_components.netloc](code_scopes)
  if not code_scopes:
    return 'Could not parse a code scope (lines to read)'

  new_target_url_components = ParseResult(
    scheme=target_url_components.scheme,
    netloc=HOST_SWAP[target_url_components.netloc],
    path=new_target_path,
    params='',
    query='',
    fragment=''
  )
  new_target = urlunparse(new_target_url_components)
  target_code_content = urlopen(new_target)

  if target_code_content.status != 200:
    return 'Could not parse a given url'

  code_lines = target_code_content.readlines()
  if len(code_scopes) == 1:
    code_lines = [code_lines[code_scopes[0]]]
  if len(code_scopes) == 2:
    code_lines = code_lines[code_scopes[0]:code_scopes[1]]

  # TODO: tabs to spaces
  code_spaces = 0
  for char in code_lines[0].decode():
    if char == ' ':
      code_spaces += 1
      continue
    break
  code_spaces = ' ' * code_spaces
  code_markdown = CODE_MARKDOWN.get(
    os.path.splitext(target_url_components.path)[-1],
    ''
  )

  lines = f"```{code_markdown}\n"
  for idx, line in enumerate(code_lines):
    lines += line.decode().replace(code_spaces, '', 1)
  lines += '```'

  return lines
