# ruff: noqa: INP001
import os

import discord
from dotenv import load_dotenv
from pycord_reactive_views import ReactiveButton, ReactiveValue, ReactiveView

load_dotenv()

bot = discord.Bot()


class Counter(ReactiveView):
    """A simple counter view that increments a counter when a button is clicked."""

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.counter_button = ReactiveButton(
            label=ReactiveValue(lambda: f"Count: {self.counter}", "Count: 0"),
            style=ReactiveValue(
                lambda: discord.ButtonStyle.primary if self.counter % 2 == 0 else discord.ButtonStyle.secondary,
                discord.ButtonStyle.primary,
            ),
        )
        self.reset_button = ReactiveButton(
            label="Reset",
            style=discord.ButtonStyle.danger,
            disabled=ReactiveValue(lambda: self.counter == 0, True),
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
    await Counter().send(ctx)


bot.run(os.getenv("TOKEN"))
