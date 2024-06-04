# Blaze Double Bot

---

## Description

[Watch the explanatory video](https://www.youtube.com/watch?v=CFQfu4DilIE)

This Python script automates the betting process on the Blaze Double website using Selenium and undetected-chromedriver. It monitors the game state, places bets according to a predefined strategy, and handles winnings and losses. Google Chrome browser required.

---

## Installation

```bash

pip install blaze-double-bot

```

## How to use the JSON file in the Blaze Double Bot

To use the Blaze Double Bot, you need to configure your credentials and other settings through a JSON file. Follow the instructions below to set up and use the bot:

1. **Create a `config.json` file** with the following content:

```json
{
    "username": "your blaze username",
    "password": "your blaze password",
    "bet_amount":0.1,
    "stop_loss_ratio":0.9,
    "stop_win_ratio":1.1,
    "wait_after_bet":150,
    "martingale":2,
    "headless": true,
    "language":"en",
    "strategies": {
        "red": [
            ["B", "R", "B", "R", "B"],
            ["B", "B", "B", "B"],
            ["R", "B", "B", "B"]
        ],
        "black": [
            ["R", "B", "R", "B", "R","B","R"],
            ["R", "R", "R", "R", "R"]
        ]
    }
}

```

- **username**: Your username or email registered on Blaze Double.
- **password**: Your password to access Blaze Double.
- **bet_amount**: The amount of the bet to be placed in each round.
- **stop_loss_ratio**: The multiplication factor of the initial balance indicating the loss limit. The bot will stop betting if the balance drops below this limit.
- **stop_win_ratio**: The multiplication factor of the initial balance indicating the win limit. The bot will stop betting if the balance reaches or exceeds this limit.
- **wait_after_bet**: Waiting time, in seconds, to restart analyzes after the bet result.
- **martingale**: MartinGale's strategy doubles the bet after a loss. The bot will do this procedure if the value is different from 0. If the value is 1 it will do the procedure 1 time, if 2 it will do it 2 times and so on. Be very careful with this strategy.
- **headless**: receives true or false. If true the browser will be invisible
- **language**: "en" (English) and "pt" (Portuguese).
- **strategies**: Pre-defined betting strategies with sequences of colors (black = "B", red = "R"). You can add as many strategies as you want here. Lists must have a maximum of 20 items. Put the lists with the largest number of items first.

2. **Create a `blazeBot.py` file** with the following content:

```python

from blaze_double_bot import BlazeDoubleBot

import json

with open('config.json', 'r') as f:
        config = json.load(f)

bot = BlazeDoubleBot(config)

bot.run()

```
---

## Support This Project

If you find this project helpful, consider supporting it by making a donation. Your contribution will help me maintain and improve this bot.

[Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=928TRAX74TYSA)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

© 2024 Rafael Ribeiro.

