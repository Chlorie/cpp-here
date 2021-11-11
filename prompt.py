from typing import Optional
import PyInquirer as inq


def input(message: str, default: Optional[str] = None) -> str:
    prompt = {
        "type": "input",
        "name": "name",
        "message": message
    }
    if default is not None:
        prompt["default"] = default
    return inq.prompt([prompt])["name"]


def choices(message: str, *choices: str) -> int:
    prompt = {
        "type": "list",
        "name": "name",
        "message": message,
        "choices": [
            {"name": choice, "value": i}
            for i, choice in enumerate(choices)
        ]
    }
    return inq.prompt([prompt])["name"]


def confirm(message: str, default: bool = False) -> bool:
    return inq.prompt([{
        "type": "confirm",
        "name": "name",
        "message": message,
        "default": default
    }])["name"]
