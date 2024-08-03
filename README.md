# Pycord Reactive Views

Pycord Reactive Views is a powerful library that extends [Pycord](https://pycord.dev), bringing reactive programming to Discord bot development. It enables developers to create dynamic, responsive user interfaces for their bots with ease.

## Table of Contents
- [What is Reactivity?](#what-is-reactivity)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## What is Reactivity?

Reactivity is a programming paradigm commonly used in front-end development. It allows for the creation of dynamic user interfaces that update in real-time based on changes in the underlying data. Pycord Reactive Views brings this powerful concept to Discord bot development.

In Pycord, reactivity is implemented through `View` classes. These classes are responsible for:
- Rendering the user interface
- Updating the UI in response to data changes
- Handling user interactions

## Features

- **Reactive Components**: Create buttons, select menus, and other Discord components that automatically update based on your bot's state.
- **Declarative Syntax**: Define your UI logic in a clear, declarative manner.
- **Easy Integration**: Seamlessly integrates with existing Pycord projects.
- **Performance Optimized**: Efficiently updates only the components that have changed.

## Installation

To install Pycord Reactive Views, use pip:

```bash
pip install pycord-reactive-views
```

Ensure you have Pycord installed as well:

```bash
pip install py-cord
```

## Quick Start

Here's a simple example of a reactive counter view:

```python
from pycord_reactive_views import ReactiveView, ReactiveButton, ReactiveValue

class Counter(ReactiveView):
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

# Usage in your bot
@bot.command()
async def counter(ctx):
    view = Counter()
    await Counter().send(ctx)
```

This example demonstrates how to bind a button's label, style, and disabled state to functions that determine their values based on the current state of the counter.

## Documentation

Comprehensive documentation is coming soon. In the meantime, please refer to the examples in the `examples` directory and the inline comments in the source code for guidance on using Pycord Reactive Views.

## Examples

Check out the `examples` directory in our GitHub repository for more detailed examples of how to use Pycord Reactive Views in various scenarios.

## Contributing

We welcome contributions to Pycord Reactive Views! If you'd like to contribute, please:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and write tests if applicable
4. Submit a pull request with a clear description of your changes

For major changes or feature requests, please open an issue first to discuss what you would like to change.

## License

Pycord Reactive Views is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
