from flask import Flask, render_template, request, jsonify
import cohere

app = Flask(__name__)
co = cohere.Client('dSe5i608cTtTQli1JJ15e9N60zmY8uFI8sHRFmau')  # Replace with your Cohere API key

@app.route("/")
def index():
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("question", "")
    
    if not user_input:
        return jsonify({"answer": "Please enter a question!"}), 400
    
    try:
        # Setting max_tokens to a valid number (e.g., 150, 300, etc.)
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=user_input,
            max_tokens=300,  # Set max_tokens to a valid value
            temperature=0.7,
            truncate='NONE'  # Ensures no truncation of the response
        )
        
        # Concatenate the text from all generations if multiple are returned
        answer = "".join(gen.text.strip() for gen in response.generations)
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"answer": "An error occurred while processing your request."}), 500

if __name__ == "__main__":
    app.run(debug=True)
