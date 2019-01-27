from functools import wraps
import json


def to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    return wrapper


@to_json
def get_data():
    return {
        'data': 42
        }
  
print(get_data())
