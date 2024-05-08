# Personal Bot
- [x] Telegram: https://telegram.me/ames0k0_personal_bot

### `/code` :: Reply to a message to get a code (input example)
```
# Input
https://github.com/krau/kmua-bot/blob/v2/kmua/callbacks/waifu.py#L131-L133

# UrlSwap
https://github.com/krau/kmua-bot/blob/v2/kmua/callbacks/waifu.py#L131-L133
                                                                #L131-L133  <- scope
https://raw.githubusercontent.com/krau/kmua-bot/v2/kmua/callbacks/waifu.py  <- content

# Output
'''python
if user.id == waifu.married_waifu_id:
    text = f"{common.mention_markdown_v2(user)}, 你和 {common.mention_markdown_v2(waifu)} 已经结婚了哦, 还想娶第二遍嘛?"
    waifu_markup = None
'''
```
Supported sites
  - [x] github.com

Supported markdown code
  - [x] python
