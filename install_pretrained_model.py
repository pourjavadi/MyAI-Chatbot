from transformers import AutoModelForCausalLM, AutoTokenizer
import os

model_name = "distilgpt2"
model_path = "/root/myai/pretrained_model"

# Create the directory if it doesn't exist
if not os.path.exists(model_path):
    os.makedirs(model_path)

# Download and save the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)

print(f"Model and tokenizer saved to {model_path}")
