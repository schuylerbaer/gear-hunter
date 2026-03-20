class EmailNotifier:
    @staticmethod
    def process_and_send(user_email, alert_id, item_id, gear_data):
        print(f"    [STUB] 📧 Pretending to send email to {user_email} for item ID: {item_id}")
        print(f"    [STUB] ⚙️ Gear details: {gear_data['brand']} {gear_data['model']}")
