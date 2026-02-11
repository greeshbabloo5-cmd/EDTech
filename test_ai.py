from google import genai

# Use the NEW client structure
client = genai.Client(api_key="AIzaSyBXeBl_HLaMFEOh1pGIDdMxF-njXkuUlr0")

try:
    # Use 'gemini-1.5-flash' with the new client
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents="Is the NexusLearn engine online?"
    )
    print("SUCCESS! AI says:", response.text)
except Exception as e:
    print("FAILED! Error details:", e)