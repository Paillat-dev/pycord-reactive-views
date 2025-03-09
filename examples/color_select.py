# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

import os

import discord
from dotenv import load_dotenv
from typing_extensions import override

from pycord_reactive_views import ReactiveSelect, ReactiveValue, ReactiveView

load_dotenv()

bot = discord.Bot()

colors: dict[str, list[discord.Colour]] = {
    "red": [discord.Colour.red(), discord.Colour.dark_red(), discord.Colour.brand_red()],
    "green": [discord.Colour.green(), discord.Colour.dark_green(), discord.Colour.brand_green()],
    "blue": [discord.Colour.blue(), discord.Colour.dark_blue()],
    "yellow": [discord.Colour.gold(), discord.Colour.dark_gold()],
    "purple": [
        discord.Colour.purple(),
        discord.Colour.dark_purple(),
        discord.Colour.blurple(),
        discord.Colour.og_blurple(),
    ],
    "gray": [discord.Colour.greyple(), discord.Colour.dark_grey(), discord.Colour.light_grey()],
    "teal": [discord.Colour.teal(), discord.Colour.dark_teal()],
    "magenta": [discord.Colour.magenta(), discord.Colour.dark_magenta()],
    "orange": [discord.Colour.orange(), discord.Colour.dark_orange()],
}


class ColourSelector(ReactiveView):
    """A simple view that allows you to select a colour and shade and updates the embed based on the selection."""

    def __init__(self) -> None:
        super().__init__()
        self.colour: str = "red"
        self.shade: discord.Colour = discord.Colour.red()
        self.colour_select: discord.ui.Select[ColourSelector] = discord.ui.Select(
            options=[
                discord.SelectOption(
                    label=colour.capitalize(),
                    value=colour,
                )
                for colour in colors
            ],
            placeholder="Select a colour",
        )
        self.shade_select: ReactiveSelect = ReactiveSelect(
            placeholder="Select a shade",
            options=ReactiveValue(
                lambda: [
                    discord.SelectOption(
                        label=str(shade.value),
                    )
                    for shade in colors[self.colour]
                ],
                [
                    discord.SelectOption(
                        label=str(shade.value),
                    )
                    for shade in colors[self.colour]
                ],
            ),
        )
        self.colour_select.callback = self._colour_select_callback
        self.shade_select.callback = self._shade_select_callback
        self.add_item(self.colour_select)
        self.add_item(self.shade_select)

    async def _colour_select_callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.colour = str(self.colour_select.values[0])
        self.shade = colors[self.colour][0]
        await self.update()

    async def _shade_select_callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        selected_shade = int(self.shade_select.values[0])
        self.shade = discord.Colour(selected_shade)
        await self.update()

    @override
    async def _get_embed(self) -> discord.Embed | None:
        return discord.Embed(
            title=f"{self.colour.capitalize()} {self.shade}",
            colour=self.shade,
        )


@bot.slash_command()
async def colours(ctx: discord.ApplicationContext) -> None:
    """Send the colour selector view."""
    await ColourSelector().send(ctx)


bot.run(os.getenv("TOKEN"))
