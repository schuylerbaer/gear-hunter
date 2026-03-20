import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from backend.app.db_client import supabase

load_dotenv()

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

class EmailNotifier:
    @staticmethod
    def process_and_send(user_email: str, alert_id: int, item_id: int, gear_data: dict):
        existing = supabase.table("sent_notifications").select("*").eq(
            "alert_id", alert_id
        ).eq("item_id", item_id).execute()

        if existing.data:
            print(f"Alert {alert_id} already notified about Item {item_id}.")
            return

        brand = gear_data.get('brand', 'Unknown Brand')
        model = gear_data.get('model', 'Unknown Model')
        price = gear_data.get('price', '0.0')
        size = gear_data.get('size', 'N/A')
        url = gear_data.get('url', '#')

        msg = EmailMessage()
        msg['Subject'] = f"Gear Hunter Alert: {brand} {model} for ${price}!"
        msg['From'] = SENDER_EMAIL
        msg['To'] = user_email
        
        msg.set_content(f"""
Hey there!

Your Gear Hunter alert found a match:

Brand: {brand}
Model: {model}
Size: {size}
Price: ${price}
Condition: {gear_data.get('condition', 'Unknown')}

Check out the post here: {url}

- The Gear Hunter Bot
""")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(SENDER_EMAIL, APP_PASSWORD)
                smtp.send_message(msg)
                
            print(f"Email successfully sent to {user_email} for {brand} {model}!")

            supabase.table("sent_notifications").insert({
                "alert_id": alert_id,
                "item_id": item_id
            }).execute()

        except Exception as e:
            print(f"ERROR --- failed to send email to {user_email}: {e}")
