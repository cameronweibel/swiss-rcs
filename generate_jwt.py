import time
import uuid
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


def generate_jwt():
    application_id = os.getenv("VONAGE_APPLICATION_ID")
    private_key_path = os.path.join(os.path.dirname(__file__), os.getenv("VONAGE_PRIVATE_KEY_PATH"))

    with open(private_key_path, "r") as f:
        private_key = f.read()

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (80 * 24 * 60 * 60),
        "jti": str(uuid.uuid4()),
        "application_id": application_id,
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token


if __name__ == "__main__":
    print(generate_jwt())
