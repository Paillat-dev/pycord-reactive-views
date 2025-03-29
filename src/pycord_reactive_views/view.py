# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

from typing import Any, Self

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
        self.ctx: discord.ApplicationContext | discord.Interaction | discord.WebhookMessage | None = None

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
        editable = self.ctx or self.message
        if not editable:
            raise ValueError("View has no editable (not yet sent?), can't refresh")
        kwargs: dict[str, Any] = {"view": self, "content": await self._get_content()}  # pyright: ignore[reportExplicitAny]
        if embeds := await self._get_embeds():
            kwargs["embeds"] = embeds
        await editable.edit(**kwargs)  # pyright: ignore[reportUnknownMemberType]

    async def send(self, ctx: discord.ApplicationContext | discord.Interaction, ephemeral: bool = False) -> None:
        """Send the view to a context."""
        self.ctx = ctx
        kwargs: dict[str, Any] = {"content": await self._get_content(), "ephemeral": ephemeral, "view": self}  # pyright: ignore[reportExplicitAny]
        if embeds := await self._get_embeds():
            kwargs["embeds"] = embeds
        r = await ctx.respond(**kwargs)  # pyright: ignore[reportUnknownMemberType]
        if isinstance(ctx, discord.Interaction):
            self.ctx = r
