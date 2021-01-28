import uuid
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID

from pierogis_live import db


class ReplyType(Enum):
    tweet = 'tweet'
    dm = 'dm'


class Order(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reply_type = db.Column(db.Enum(ReplyType), primary_key=True, default=uuid.uuid4)
    author_id = db.Column(UUID(as_uuid=True))
    tweet_id = db.Column(UUID(as_uuid=True))
