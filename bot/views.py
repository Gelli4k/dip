
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class BotVerifyView(generics.UpdateAPIView):
    model = TgUser
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class(request.data).data
        tg_client = TgClient('5806733281:AAGBZWpPnL-qRs8OTY7dyx0Xz3J_cwsJJYg')
        tg_user = TgUser.objects.filter(verification_code=data['verification_code']).exists()
        if not tg_user:
            raise Exception
        tg_user.user = request.user
        tg_user.save()
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text='Успешно!')
        return Response(data=data)

