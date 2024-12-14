import json
from dataclasses import is_dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

from rest_framework.utils.encoders import JSONEncoder

from apps.shared.value_objects import Id


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format datetime objects as strings in your desired format
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, Enum):
            return obj.value
        elif is_dataclass(obj) and hasattr(obj, "to_dict"):  # supposing we use dataclasses-json
            return obj.to_dict()  # type: ignore
        elif isinstance(obj, Id):
            return obj.value
        elif isinstance(obj, Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
