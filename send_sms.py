import sys
import vonage
from vonage_messages import RcsText, RcsCustom
from dotenv import load_dotenv
import os

load_dotenv()

client = vonage.Vonage(
    auth=vonage.Auth(
        application_id=os.getenv("VONAGE_APPLICATION_ID"),
        private_key=os.path.join(os.path.dirname(__file__), os.getenv("VONAGE_PRIVATE_KEY_PATH")),
    )
)

SENDER = os.getenv("RCS_SENDER_ID")
TO = os.getenv("TO_NUMBER")
UPGRADE_IMAGE_URL = "https://i0.wp.com/theluxurytravelexpert.com/wp-content/uploads/2022/10/lufthansa-business-class-2.jpg?resize=678%2C381&ssl=1"
BOOKING_URL = "https://cameronweibel.github.io/swiss-rcs/upgrade-lh.html"


def send_text(text="Hello from Vonage RCS API"):
    message = RcsText(from_=SENDER, to=TO, text=text, client_ref="push_notification")
    response = client.messages.send(message)
    print(f"Text sent. UUID: {response.message_uuid}")
    return response


def send_upgrade_offer():
    message = RcsCustom(
        from_=SENDER,
        to=TO,
        custom={
            "contentMessage": {
                "richCard": {
                    "standaloneCard": {
                        "cardOrientation": "VERTICAL",
                        "thumbnailImageAlignment": "LEFT",
                        "cardContent": {
                            "title": "Upgrade to Business Class Allegris",
                            "description": (
                                "Good news! A Business Class upgrade is available "
                                "for your upcoming FRA \u2192 JFK flight on June 12. "
                                "Enjoy the Allegris suite with sliding door, gourmet dining, "
                                "and Lufthansa lounge access from just EUR 99.00."
                            ),
                            "media": {
                                "height": "TALL",
                                "contentInfo": {
                                    "fileUrl": UPGRADE_IMAGE_URL,
                                    "forceRefresh": False,
                                },
                            },
                            "suggestions": [
                                {
                                    "action": {
                                        "text": "View Upgrade",
                                        "postbackData": "ignore",
                                        "openUrlAction": {
                                            "url": BOOKING_URL,
                                        },
                                    }
                                },
                            ],
                        },
                    }
                }
            }
        },
        client_ref="push_notification",
    )
    response = client.messages.send(message)
    print(f"Upgrade offer sent. UUID: {response.message_uuid}")
    return response


def send_confirmation():
    message = RcsText(
        from_=SENDER,
        to=TO,
        text=(
            "Upgrade Confirmed!\n\n"
            "Your Business Class Allegris upgrade for flight LH400 "
            "FRA \u2192 JFK on June 12, 2025 has been confirmed.\n\n"
            "Seat: 3A | Terminal 1 Gate B22\n"
            "Total: EUR 99.00\n\n"
            "Thank you for choosing Lufthansa."
        ),
        client_ref="push_notification",
    )
    response = client.messages.send(message)
    print(f"Confirmation sent. UUID: {response.message_uuid}")
    return response


if __name__ == "__main__":
    choice = sys.argv[1] if len(sys.argv) > 1 else None

    if choice == "text":
        send_text()
    elif choice == "upgrade":
        send_upgrade_offer()
    elif choice == "confirm":
        send_confirmation()
    else:
        print("Usage: python send_sms.py [text|upgrade|confirm]")
        print("  text    - Send a simple RCS text message")
        print("  upgrade - Send a rich card upgrade offer")
        print("  confirm - Send an upgrade confirmation message")
