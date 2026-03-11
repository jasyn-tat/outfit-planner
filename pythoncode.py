from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# Replace with your actual Groq API key
api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)

@app.route('/get-outfit', methods=['POST'])
def get_outfit():
    # EVERYTHING BELOW THIS LINE MUST BE INDENTED
    data = request.json
    vibe = data.get('vibe')
    age = data.get('age')
    brand = data.get('brand')
    gender = data.get('gender')
    
    # Get Weather
    naperville_url = "https://api.open-meteo.com/v1/forecast?latitude=41.7503&longitude=-88.1535&current=temperature_2m&temperature_unit=fahrenheit"
    weather_data = requests.get(naperville_url).json()
    temp = weather_data['current']['temperature_2m']
    
    # Create the Prompt
    prompt = (
        f"It's {temp}°F in Naperville. The user is a {age} year old {gender} "
        f"going to {vibe}. Their favorite brands are {brand}. "
        f"Suggest 3 complete outfits (shirt, pants, shoes, and an outer layer if cold). "
        f"IMPORTANT: Do NOT make up direct product links. They will break. "
        f"Instead, for EVERY item, create a Google Shopping search link formatted as an HTML button. "
        f"Example format: <a href='https://www.google.com/search?q={brand}+baggy+jeans+mens&tbm=shop' target='_blank'>Shop Jeans</a> "
        f"Make sure to include the estimated cost for the total outfit."
        f"Make sure you include the names of each item along with the link. Ex: White and Blue T-Shirt or Yellow Hoodie."
    )
    # Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # This return is now INSIDE the function
    return jsonify({"outfit": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
