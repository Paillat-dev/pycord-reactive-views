# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

from typing import Self

import discord
from typing_extensions import override

from .components import Reactive


class ReactiveView(discord.ui.View):
    """A view that can be used with reactive components."""

    def __init__(
        self,
        *,
        timeout: float | None = 180.0,
        disable_on_timeout: bool = False,
    ) -> None:
        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout)  # pyright: ignore[reportUnknownMemberType]
        self._reactives: list[Reactive] = []

    @override
    def add_item(self, item: discord.ui.Item[Self]) -> None:
        if isinstance(item, Reactive):
            self._reactives.append(item)
        super().add_item(item)  # pyright: ignore [reportUnknownMemberType]

    async def _get_embed(self) -> discord.Embed | None:
        """Get the discord embed to be displayed in the message."""
        return None

    async def _get_embeds(self) -> list[discord.Embed]:
        """Get the discord embeds to be displayed in the message."""
        if embed := await self._get_embed():
            return [embed]
        return []

    async def _get_content(self) -> str | None:
        """Get the content to be displayed in the message."""
        return None

    async def update(self) -> None:
        """Update the view with new components.

        :raises ValueError: If the view has no message (not yet sent?), can't update
        """
        for reactive in self._reactives:
            await reactive.refresh()
        if not self.message:
            raise ValueError("View has no message (not yet sent?), can't refresh")
        if embeds := await self._get_embeds():
            await self.message.edit(content=await self._get_content(), embeds=embeds, view=self)
        else:
            await self.message.edit(content=await self._get_content(), view=self)

    async def send(self, ctx: discord.ApplicationContext | discord.Interaction) -> None:
        """Send the view to a context."""
        if embeds := await self._get_embeds():
            await ctx.respond(content=await self._get_content(), embeds=embeds, view=self)  # pyright: ignore [reportUnknownMemberType]
        else:
            await ctx.respond(content=await self._get_content(), view=self)  # pyright: ignore [reportUnknownMemberType]
