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
        if custom_id:
            self.custom_id = custom_id
        self.sku_id = sku_id


class ReactiveSelect(discord.ui.Select, Reactive):  # pyright: ignore[reportUnsafeMultipleInheritance,reportMissingTypeArgument]
    """A select menu that can be used with reactive values."""

    def __init__(
        self,
        select_type: discord.ComponentType = discord.ComponentType.string_select,
        *,
        custom_id: str | None = None,
        placeholder: MaybeReactiveValue[str | None] = None,
        min_values: MaybeReactiveValue[int] = 1,
        max_values: MaybeReactiveValue[int] = 1,
        options: MaybeReactiveValue[list[discord.SelectOption] | None] = None,
        channel_types: MaybeReactiveValue[list[discord.ChannelType] | None] = None,
        disabled: MaybeReactiveValue[bool] = False,
        row: MaybeReactiveValue[int | None] = None,
    ):
        discord.ui.Select.__init__(self)
        Reactive.__init__(self)
        self.add_reactive("placeholder", placeholder)
        self.add_reactive("min_values", min_values)
        self.add_reactive("max_values", max_values)
        self.add_reactive("options", options)
        if select_type == discord.ComponentType.channel_select:
            self.add_reactive("channel_types", channel_types)
        self.add_reactive("disabled", disabled)
        self.add_reactive("row", row)
        if custom_id:
            self.custom_id = custom_id
        self.select_type = select_type
