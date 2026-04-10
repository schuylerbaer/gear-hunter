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
        def check_alert_against_recent_items(alert_criteria: list, category_id: int):
            """
            Fetches the last 30 items in the category and checks for a match.
            """
            response = supabase.table("items").select(
                "id, listings(url), item_attributes(key, value)"
            ).eq("category_id", category_id).order("id", desc=True).limit(30).execute()
        
            matches = []
            for item in response.data:
                attrs = {attr["key"]: attr["value"] for attr in item.get("item_attributes", [])}
            
                is_match = all(
                    attrs.get(c["key"]) == c["value"]
                    for c in alert_criteria
                )
            
                if is_match:
                    matches.append({
                        "item_id": item["id"],
                        "url": item["listings"]["url"] if item.get("listings") else "#",
                        "attributes": attrs
                    })
            return matches
