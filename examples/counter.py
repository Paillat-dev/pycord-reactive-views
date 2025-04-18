# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

import os

import discord
from dotenv import load_dotenv

from pycord_reactive_views import ReactiveButton, ReactiveValue, ReactiveView

load_dotenv()

bot = discord.Bot()


class Counter(ReactiveView):
    """A simple counter view that increments a counter when a button is clicked."""

    def __init__(self) -> None:
        super().__init__()
        self.counter: int = 0
        self.counter_button: ReactiveButton = ReactiveButton(
            label=ReactiveValue(lambda: f"Count: {self.counter}", "Count: 0"),
            style=ReactiveValue(
                lambda: discord.ButtonStyle.primary if self.counter % 2 == 0 else discord.ButtonStyle.secondary,
                discord.ButtonStyle.primary,
            ),
        )
        self.reset_button: ReactiveButton = ReactiveButton(
            label="Reset",
            style=discord.ButtonStyle.danger,
            disabled=ReactiveValue(lambda: self.counter == 0, default=True),
        )
        self.counter_button.callback = self._increment
        self.reset_button.callback = self._reset
        self.add_item(self.counter_button)
        self.add_item(self.reset_button)

    async def _increment(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.counter += 1
        await self.update()

    async def _reset(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.counter = 0
        await self.update()


@bot.slash_command()
async def counter(ctx: discord.ApplicationContext) -> None:
    """Send the counter view."""
    await Counter().send(ctx, ephemeral=True)


bot.run(os.getenv("TOKEN_2"))
