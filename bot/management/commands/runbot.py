from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message


class Command(BaseCommand):
    help = 'Runs telegram bot'
    tg_client = TgClient('5806733281:AAGBZWpPnL-qRs8OTY7dyx0Xz3J_cwsJJYg')

    def handle_unverified_user(self, msg: Message, tg_user: TgUser):
        code = '123'
        tg_user.verification_code = code
        tg_user.save()
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'{code}'
        )

    def handle_user(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.message_from.id,
            tg_chat_id=msg.chat.id
        )

        if created:
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Подтвердите пожалуйста свой аккаунт."
                     f"Для подтверждения необходимо ввести код:{tg_user.verification_code} на сайте"
            )

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_user(item.message)