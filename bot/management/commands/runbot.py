from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models.category import GoalCategory
from goals.models.goal import Goal
from todolist.settings import TG_BOT_API_TOKEN


class Command(BaseCommand):
    help = 'Runs telegram bot'
    tg_client = TgClient(TG_BOT_API_TOKEN)
    offset = 0

    def choose_category(self, msg: Message, tg_user: TgUser):
        goal_categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False,
        )
        goals_categories_str = '/n'.join([str(goal.id) + '- ' + goal.title for goal in goal_categories])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Выберите категорию (укажите номер):\n {goals_categories_str}'
        )
        is_running = True

        while is_running:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, 'message'):
                    print(msg.text)
                    category = goal_categories.filter(id=int(msg.text))
                    if category:
                        self.create_goal(msg, tg_user, category)
                        is_running = False
                    elif msg.text == '/cancel':
                        self.tg_client.send_message(
                            chat_id=msg.chat.id,
                            text=f'Операция отменена'
                        )
                        is_running = False
                    else:
                        self.tg_client.send_message(
                            chat_id=msg.chat.id,
                            text=f'Категория с номером {msg.text} не существует'
                        )
                        is_running = False

    def create_goal(self, msg: Message, tg_user: TgUser, category: GoalCategory):
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Введите пожалуйста заголовок для создания цели'
        )
        is_running = True
        while is_running:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if item.message.text == '/cancel':
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text=f'Операция отменена'
                    )
                    is_running = False
                else:
                    goal = Goal.objects.create(
                        category=category,
                        user=tg_user.user,
                        title=item.message.text,
                    )
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text=f'Цель = {goal.title} создана'
                    )
                    is_running = False

    def get_goals(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(category__board__participants__user=tg_user.user,
                                    ).exclude(status=Goal.Status.archived)
        goals_str = '/n'.join([goal.title for goal in goals])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Вот список ваших целей:\n {goals_str}'
        )

    def handle_message(self, msg: Message):
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text='LALALA'
        )
        return False
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_ud=msg.message_from.id,
            tg_chat_id=msg.chat.id
        )

        if created or not tg_user.user:
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Подтвердите пожалуйста свой аккаунт."
                     f"Для подтверждения необходимо ввести код:{tg_user.verification_code} на сайте"
            )
        elif msg.text == '/whoami':
            self.tg_client.send_message(chat_id=msg.chat.id, text=f'Вы: {tg_user.user.first_name} '
                                                                  f'{tg_user.user.last_name}, id: {tg_user.user.id}')
        elif msg.text == '/goals':
            self.get_goals(msg, tg_user)
        elif msg.text == '/create':
            self.choose_category(msg, tg_user)
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Не знаю такой команды {msg.text}'
            )

    def handle(self, *args, **options):
        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, 'message'):
                    self.handle_message(item.message)
