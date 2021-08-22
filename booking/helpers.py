import functools
from typing import List


def singleton(cls):
    previous_instances = {}

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls in previous_instances and previous_instances.get(cls, None).get(
            "args"
        ) == (args, kwargs):
            return previous_instances[cls].get("instance")
        else:
            previous_instances[cls] = {
                "args": (args, kwargs),
                "instance": cls(*args, **kwargs),
            }
            return previous_instances[cls].get("instance")

    return wrapper


def flatten_list(original: List[list]):
    return [item for sublist in original for item in sublist]
