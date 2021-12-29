from marshmallow import Schema, fields


class ChatSchema(Schema):
    """Схема чата."""

    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    username = fields.Str()
    type = fields.Str()


class FromSchema(Schema):
    """Схема бот, пользователь."""

    id = fields.Int()
    is_bot = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    username = fields.Str()
    language_code = fields.Str()


class MessageSchema(Schema):
    """Схема сообщения."""

    message_id = fields.Int()
    from_in = fields.Nested(FromSchema())
    chat = fields.Nested(ChatSchema())
    date = fields.Int()
    text = fields.Str()


class InSchema(Schema):
    """Схема входящего запроса."""

    update_id = fields.Int()
    message = fields.Nested(MessageSchema())
