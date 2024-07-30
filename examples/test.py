import discord
from pycord_reactive_views import ReactiveButton, ReactiveView

bot = discord.Bot()


class Counter(ReactiveView):
    """A simple counter view that increments a counter when a button is clicked."""

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.counter_button = ReactiveButton(value=lambda: self.counter)
        self.counter_button.callback = self._button_callback
        self.add_item(self.counter_button)

    async def _button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.counter += 1
