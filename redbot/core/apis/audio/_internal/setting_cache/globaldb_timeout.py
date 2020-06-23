from __future__ import annotations

from typing import Dict, Optional, Union

import discord

from redbot.core import Config
from redbot.core.bot import Red


class GlobalDBTimeoutManager:
    def __init__(self, bot: Red, config: Config, enable_cache: bool = True):
        self._config: Config = config
        self.bot = bot
        self.enable_cache = enable_cache
        self._cached_global: Dict[None, Union[float, int]] = {}

    async def get_global(self) -> Union[float, int]:
        ret: Union[float, int]
        if self.enable_cache and None in self._cached_global:
            ret = self._cached_global[None]
        else:
            ret = await self._config.global_db_get_timeout()
            self._cached_global[None] = ret
        return ret

    async def set_global(self, set_to: Optional[Union[float, int]]) -> None:
        if set_to is not None:
            await self._config.global_db_get_timeout.set(set_to)
            self._cached_global[None] = set_to
        else:
            await self._config.global_db_get_timeout.clear()
            self._cached_global[None] = self._config.defaults["GLOBAL"]["global_db_get_timeout"]

    async def get_context_value(self, guild: discord.Guild = None) -> Union[float, int]:
        return await self.get_global()
