import hashlib
import re

SECRET = "study-secret"

RE_PAYLOAD = re.compile(r"^id=(\d+);ts=(\d+);sig=([0-9a-f]{64})$")


def sign(user_id, timestamp):
    raw = f"{user_id}:{timestamp}:{SECRET}".encode()
    return hashlib.sha256(raw).hexdigest()


def build_payload(user_id, timestamp):
    if user_id < 0 or timestamp < 0:
        raise ValueError("negative values not allowed")
    return f"id={user_id};ts={timestamp};sig={sign(user_id, timestamp)}"


def parse_payload(payload):
    m = RE_PAYLOAD.match(payload.strip())
    if not m:
        raise ValueError("invalid payload format")
    user_id, timestamp, sig = int(m.group(1)), int(m.group(2)), m.group(3)
    if sig != sign(user_id, timestamp):
        raise ValueError("signature mismatch")
    return user_id, timestamp
