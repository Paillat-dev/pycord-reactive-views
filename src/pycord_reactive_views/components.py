from typing import Any

import discord

from .utils import MaybeReactiveValue, ReactiveValue, is_reactive


class Reactive:
    """A class that can be used with reactive values."""

    def __init__(self):
        super().__init__()
        self.reactives: dict[str, ReactiveValue[Any]] = {}
        self.super_kwargs: dict[str, Any] = {}

    def add_reactive(self, key: str, value: MaybeReactiveValue[Any]) -> None:
        """Add a reactive value to the view."""
        if is_reactive(value):
            self.reactives[key] = value
            if value.default:
                setattr(self, key, value.default)
        else:
            setattr(self, key, value)

    async def refresh(self) -> None:
        """Refresh the reactive values."""
        for key, value in self.reactives.items():
            setattr(self, key, await value())


class ReactiveButton(discord.ui.Button, Reactive):  # pyright: ignore[reportUnsafeMultipleInheritance,reportMissingTypeArgument]
    """A button that can be used with reactive values."""

    def __init__(
        self,
        *,
        style: MaybeReactiveValue[discord.ButtonStyle] = discord.ButtonStyle.secondary,
        label: MaybeReactiveValue[str | None] = None,
        disabled: MaybeReactiveValue[bool] = False,
        custom_id: str | None = None,
        url: MaybeReactiveValue[str | None] = None,
        emoji: MaybeReactiveValue[str | discord.Emoji | discord.PartialEmoji | None] = None,
        sku_id: int | None = None,
        row: MaybeReactiveValue[int | None] = None,
    ):
        discord.ui.Button.__init__(self)
        Reactive.__init__(self)
        self.add_reactive("style", style)
        self.add_reactive("label", label)
        self.add_reactive("disabled", disabled)
        self.add_reactive("url", url)
        self.add_reactive("emoji", emoji)
        self.add_reactive("row", row)
