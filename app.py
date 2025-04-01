from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
from transformers import pipeline, AutoTokenizer
import os
import torch

torch.set_num_threads(120)

app = Flask(__name__)
CORS(app)

model_path = "/root/myai/pretrained_model"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at path {model_path}!")

print("Loading model...")
try:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    generator = pipeline("text-generation", model=model_path, tokenizer=tokenizer, device=-1)
    print("Model loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Error loading model: {str(e)}")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    try:
        output = generator(
            prompt,
            max_new_tokens=50,
            num_beams=5,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            no_repeat_ngram_size=3,
            truncation=True,
            return_full_text=False
        )[0]["generated_text"]
        lines = output.split("\n")
        limited_output = "\n".join(lines[:5])
        words = limited_output.split()
        def generate():
            for word in words:
                yield word + " "
        return Response(stream_with_context(generate()), mimetype="text/plain")
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return Response("Error processing request: " + str(e), status=500, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
