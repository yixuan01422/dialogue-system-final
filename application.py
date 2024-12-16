import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import re

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
dsa
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

client = InferenceClient(api_key="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")

basic_prompt = "You should always assume that we are in a multi-user chatroom environment. You will participate as one member of the chatroom, 'G'. All messages sent to you will start with '<name>:', where <name> is the actual name of the user chatting in the chatroom. For example, for message 'A: G, do you know who I am?', It means somebody named A said:'G, do you know who I am?'. Other users in the chatroom may call your name, and you should respond accordingly. You’re expected to join the conversation when it seems appropriate. If you have nothing to add, respond only with <token:skip>. Remember your name is 'G', if somebody calls you by name, you must reply! The message starts below:"

@app.route("/get_reply", methods=["POST"])
def get_reply():
    logging.info(f"Received request: {request.json}")
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid request format"}), 400

        user_message = request.json.get("message", "")
        USER = request.json.get("user", "")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        logging.info(f"Calling Hugging Face API for reply generation with input: {user_message}")
        try:
            new_prompt = f"{basic_prompt}\n{USER}: {user_message}"
            logging.info(f"Prompt: {new_prompt}")
            messages = [
                {
                    "role": "user",
                    "content": new_prompt
                }
            ]

            completion = client.chat.completions.create(
                model="meta-llama/Llama-3.2-3B-Instruct",
                messages=messages,
                max_tokens=512
            )

            response = completion.choices[0].message

            if not response:
                logging.error("Received empty or invalid response from Hugging Face API")
                return jsonify({"error": "Empty response from API"}), 500

            assistant_response = response['content']

        except Exception as e:
            logging.error(f"Error in Hugging Face API call for reply generation: {str(e)}")
            return jsonify({"error": "Failed to generate reply"}), 500
        logging.info(f"Generated response: {assistant_response}")
        if assistant_response.strip().lower() == "<token:skip>" or "skip" in assistant_response.lower():
            response = {}
        else:
            if ":" in assistant_response:
                assistant_response = assistant_response.split(":", 1)[1].strip() 
            else:
                 assistant_response = assistant_response.strip()
            assistant_response = re.sub(r"[<>]", "", assistant_response)
            response = {
                "reply": assistant_response
            }
        return jsonify(response)
    except Exception as e:
        logging.error(f"Unexpected error in get_reply: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')

    logging.info(f"CORS Headers Set: {response.headers.get('Access-Control-Allow-Origin')}")
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)