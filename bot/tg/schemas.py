from dataclasses import field
from typing import List, Optional

import marshmallow_dataclass
from marshmallow_dataclass import dataclass
from marshmallow import EXCLUDE


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: Optional[str | None]
    last_name: Optional[str | None]
    username: Optional[str | None]

    class Meta:
        unknown = EXCLUDE


@dataclass
class MessageChat:
    id: int
    first_name: Optional[str | None]
    username: Optional[str | None]
    last_name: Optional[str | None]
    type: str
    title: Optional[str | None]


@dataclass
class Message:
    message_id: int
    message_from: MessageFrom = field(metadata={'data_key': 'from'})
    chat: MessageChat
    date: int
    text: Optional[str | None]

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE


GET_UPDATES_SCHEMA = marshmallow_dataclass.class_schema(GetUpdatesResponse)()
SEND_MESSAGES_RESPONSE_SCHEMA = marshmallow_dataclass.class_schema(SendMessageResponse)()
