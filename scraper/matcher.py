from backend.app.db_client import supabase

class GearMatcher:
    @staticmethod
    def check_new_item_against_alerts(new_item_attributes: dict, category_id: int):
        """
        Runs every time a new item is scraped. 
        Pulls active alerts and checks if there's a match.
        """

        response = supabase.table("alerts").select(
            "id", 
            "user_id", 
            "users(email)", 
            "alert_criteria(key, value)"
        ).eq("is_active", True).eq("category_id", category_id).execute()
        
        active_alerts = response.data
        users_to_notify = []

        for alert in active_alerts:
            criteria_list = alert.get("alert_criteria", [])
            
            if not criteria_list:
                continue

            is_match = all(
                new_item_attributes.get(criteria["key"]) == criteria["value"]
                for criteria in criteria_list
            )

            if is_match:
                user_email = alert["users"]["email"]
                users_to_notify.append({
                    "email": user_email,
                    "alert_id": alert["id"]
                })

        return users_to_notify

    @staticmethod
    def check_new_alert_against_items(criteria_dict: dict, category_id: int):
        """
        Runs when a user creates a new alert.
        Searches the database for existing gear that matches their criteria.
        Expects criteria_dict like: {"brand": "La Sportiva", "size": "42"}
        """

        response = supabase.table("items").select("*").eq(
            "category_id", category_id
        ).contains("attributes", criteria_dict).execute()

        return response.data
