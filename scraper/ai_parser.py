import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

# Pydantic item schema 
class ExtractedGear(BaseModel):
    category: str = Field(description="Must be exactly 'Shoe' or 'Cam'.")
    brand: str = Field(description="The brand of the item (e.g., Black Diamond, La Sportiva).")
    model: str = Field(description="The specific model of the item (e.g., Camalot C4, Solution).")
    price: float = Field(description="The current asking price as a number. If free, use 0.0.")
    condition: str = Field(description="The condition of the item. Use 'Unknown' if not stated.")
    size: str = Field(description="For CAMS ONLY (e.g., '#0.5', '2'). For Shoes, use 'N/A'.")
    eu_size: str = Field(description="For SHOES ONLY: The EU size (e.g., '38.5'). Use 'Unknown' for cams.")
    us_size: str = Field(description="For SHOES ONLY: The US size (e.g., '9'). Use 'Unknown' for cams.")
    gender: str = Field(description="For SHOES ONLY: 'M' or 'W'. Default to 'M' unless explicitly stated as women's sizing.")

# Pydantic post schema
class GearList(BaseModel):
    items: list[ExtractedGear] = Field(description="A list of all available gear items found in the post.")

def parse_gear_with_ai(raw_text: str):
    prompt = f"""
    You are an expert rock climbing gear extractor. 
    Review the following forum post text. 
    Extract every distinct piece of gear being sold.
    
    CRITICAL RULES:
    1. If an item is marked as "SOLD", do not include it in your output.
    2. If a price is missing, estimate it as 0.0.
    3. Infer the brand if it's obvious to a climber (e.g., 'C4' implies Black Diamond).
    4. STRICT FILTER: ONLY extract rock climbing shoes and cams (spring loaded camming devices). Completely ignore all other items (ropes, harnesses, clothing, carabiners, etc.).
    5. FIX ALL TYPOS: for example, if someone lists 'la sportiiva muira', you must change it to 'La Sportiva Miura'. This even applies for making it plural if it isn't officially supposed to be ('Miuras should be Miura'). This applies to brand, model, size, or any other category.

    SIZING RULES:
    1. CAMS: Put the cam size in the 'size' field. Leave 'eu_size', 'us_size', and 'gender' as 'Unknown'.
    2. SHOES: Put 'N/A' in the `size` field. You MUST extract the 'eu_size', 'us_size', and 'gender'.
    7. SHOE CONVERSIONS: If a post only lists a US size (e.g., US Men's 9), you MUST use standard climbing shoe conversions to populate the 'eu_size' (e.g., '42'). If it only lists an EU size, estimate the 'us_size'. 
    8. GENDER: Assume all shoe gender is 'M' for men's unless explicitly stated otherwise or highly probable based on the content of the post.
    
    FORUM TEXT:
    {raw_text}
    """

    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GearList,
                temperature=0.1
            ),
        )
        
        data = json.loads(response.text)
        return data['items']
        
    except Exception as e:
        return []
