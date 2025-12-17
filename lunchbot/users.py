import os
import json
from typing import Any, Dict
from lunchbot.config import USER_PROFILES


def load_user_profile(user: str) -> Dict[str, Any]:
    '''Load or create empty json profile'''
    if user is None:
        return {}

    os.makedirs(USER_PROFILES, exist_ok=True)
    path = os.path.join(USER_PROFILES, f"{user}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # not exist -> create empty profile
    profile = {}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    return profile
