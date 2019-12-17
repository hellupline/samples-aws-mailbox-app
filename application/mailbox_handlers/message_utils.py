import dataclasses
import datetime
import decimal
import email
import email.policy
import email.utils
import json
import typing


T_ADDRESS = typing.Tuple[typing.AnyStr, typing.AnyStr]


@dataclasses.dataclass()
class Message:  # pylint: disable=too-many-instance-attributes
    message_id: typing.AnyStr  # message key
    in_reply_to: typing.AnyStr  # message is reply for
    date: datetime.datetime  # when was sent
    email_from: T_ADDRESS  # email source
    email_to: T_ADDRESS  # email target
    carbon_copy: typing.List[T_ADDRESS]  # who received this message
    subject: typing.AnyStr  # message subject
    reply_to: typing.AnyStr  # who to reply

    @classmethod
    def from_bytes(cls, data: bytes):
        m = email.message_from_bytes(data, policy=email.policy.default)
        cls.from_email(m)

    @classmethod
    def from_email(cls, m: email.message.Message):
        return Message(
            message_id=m.get("message-id", ""),
            in_reply_to=m.get("in-reply-to", ""),
            date=_parsedate(m),
            email_from=email.utils.parseaddr(m.get("from", "")),
            email_to=email.utils.parseaddr(m.get("to", "")),
            carbon_copy=email.utils.getaddresses(m.get_all("cc", [])),
            subject=m.get("subject", ""),
            reply_to=m.get("reply-to", ""),
        )


def _parsedate(m: email.message.Message) -> datetime.datetime:
    parsed = email.utils.parsedate_to_datetime(m.get("date", ""))
    return parsed.astimezone(datetime.timezone.utc)


class JSONEncoder(json.JSONEncoder):
    # pylint: disable=method-hidden
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(JSONEncoder, self).default(o)
