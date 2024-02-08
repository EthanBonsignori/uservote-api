import re
from uuid import UUID


def to_lower_camel_case(string: str) -> str:
    split_str = string.split('_')
    return split_str[0] + ''.join(word.capitalize() for word in split_str[1:])


def uuid_masker(exposed_uuid: str | UUID) -> str:
    uuid_str = str(exposed_uuid)
    return re.sub(
        r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-",
        '********-****-****-****-',
        uuid_str
    )
