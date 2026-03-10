import os
from dotenv import load_dotenv
from supabase import create_client, Client
from backend.app.schemas.item import ItemCreate

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def save_scraped_item(item_data: ItemCreate):
    """
    Takes a validated Pydantic ItemCreate object and saves it 
    across the listings, items, and item_attributes tables in Supabase.
    """
    try:
        # Check if the URL already exists
        existing = supabase.table('listings').select('id').eq('url', item_data.url).execute()
        if existing.data:
            print(f"Skipping: Listing already exists for URL: {item_data.url}")
            return None

        # Insert the listing container
        listing_res = supabase.table('listings').insert({
            'source_id': item_data.source_id,
            'url': item_data.url,
            'raw_text': item_data.raw_text,
            'author': item_data.author
        }).execute()
        
        # Insert the item
        listing_id = listing_res.data[0]['id']

        item_res = supabase.table('items').insert({
            'listing_id': listing_id,
            'category_id': item_data.category_id
        }).execute()
        
        item_id = item_res.data[0]['id']

        # Insert the item attributes
        attributes_data = [
            {'item_id': item_id, 'key': k, 'value': v} 
            for k, v in item_data.attributes.items()
        ]
        
        if attributes_data:
            supabase.table('item_attributes').insert(attributes_data).execute()

        print(f"✅ Successfully saved new gear! Item ID: {item_id}")
        return item_id

    except Exception as e:
        print(f"❌ Error saving to Supabase: {e}")
        return None
