import unittest

from pilgram.classes import Player
from pilgram.globals import GlobalSettings
from pilgram.strings import Strings
from ui.telegram_bot import (
    PilgramBot,
    _delimit_markdown_entities,
    get_event_notification_string_and_targets,
)
from ui.utils import UserContext


class TestTelegram(unittest.TestCase):

    def test_event_handling(self):
        context = UserContext({"id": 1234, "username": "ombro"})
        self.assertIsNone(context.get_event_data())
        player = Player.create_default(1234, "ombro", "A really cool guy")
        context.set_event("donation", {"donor": player, "amount": 100, "recipient": player})
        event = context.get_event_data()
        result = get_event_notification_string_and_targets(event)
        self.assertEqual(result, (Strings.donation_received.format(donor=player.name, amm=100), player))

    def test_delimit_markdown_entities(self):
        text = "*a_b_c_d*"
        result = _delimit_markdown_entities(text)
        self.assertEqual(result, "\\*a\\_b\\_c\\_d\\*")
        text = "aa__bb"
        result = _delimit_markdown_entities(text)
        self.assertEqual(result, "aa\\_\\_bb")

    def test_telegram_notify(self):
        bot = PilgramBot(GlobalSettings.get("Telegram bot token"))
        player = Player.create_default(633679661, "Ombro", "A really cool guy")
        bot.notify(player, "test" * 4000)

    def test_telegram_send_file(self):
        bot = PilgramBot(GlobalSettings.get("Telegram bot token"))
        player = Player.create_default(633679661, "Ombro", "A really cool guy")
        bot.send_file(player, "AAA.txt", b"AAAAA", "AAAAA")
