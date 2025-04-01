# MyAI Chatbot

A simple AI chatbot built with Flask and Transformers, featuring a beautiful HTML interface. This project allows users to interact with a language model (`distilgpt2`) to generate text responses, such as stories or answers to questions.

## Features

- **Interactive Chat Interface**: A modern, responsive HTML interface with a gradient design.
- **AI-Powered Responses**: Uses the `distilgpt2` model from Hugging Face to generate text.
- **Real-time Streaming**: Responses are streamed word-by-word for a smooth user experience.
- **CORS Support**: Handles cross-origin requests for seamless browser integration.

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.10 or higher
- Git
- A Linux server (e.g., Ubuntu) with root access
- A web server (e.g., Apache or Nginx) to serve the HTML file

---

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your server:

```sh
git clone https://github.com/<your-username>/myai-project.git
cd myai-project
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment to manage dependencies:

```sh
python3 -m venv ai_env
source ai_env/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```sh
pip install -r requirements.txt
```

### 4. Download the Pretrained Model

Download the `distilgpt2` model from Hugging Face and save it to the `/root/myai/pretrained_model` directory. Use the following script:

```python
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
```

Save this script as `install_pretrained_model.py` and run it:

```sh
python3 install_pretrained_model.py
```

### 5. Run the Flask Server

Start the Flask server on port `5001`:

```sh
python3 app.py
```

Alternatively, set it up as a **systemd** service for automatic startup:

```sh
nano /etc/systemd/system/myai.service
```

Add the following content:

```ini
[Unit]
Description=MyAI Flask API Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/myai-project
ExecStart=/root/myai-project/ai_env/bin/python3 /root/myai-project/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```sh
systemctl daemon-reload
systemctl enable myai.service
systemctl start myai.service
```

### 6. Serve the HTML Interface

Copy the `index.html` file to your web server's directory (e.g., for Apache):

```sh
cp index.html /var/www/html/index.html
```

### 7. Open Ports

Ensure port `5001` (for Flask) and port `80` (for the web server) are open in your firewall:

#### If using UFW:

```sh
ufw allow 5001
ufw allow 80
ufw status
```

#### If using IPTables:

```sh
iptables -A INPUT -p tcp --dport 5001 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables-save
```

---

## 8. Access the Chatbot

Open your browser and go to:

```
http://<your-server-ip>/
```

Type a message (e.g., **"Tell me a story about a dragon"**) and click **Send**. You should see a response from the AI.

---

## Troubleshooting

- **Flask Server Not Running**: Check the status of the Flask server:

  ```sh
  systemctl status myai.service
  ```

- **Port Not Open**: Verify that port `5001` is open:

  ```sh
  netstat -tuln | grep 5001
  ```

- **CORS Issues**: Ensure `flask-cors` is installed and configured in `app.py`.

- **Model Not Found**: Verify that the `distilgpt2` model is downloaded to `/root/myai/pretrained_model`.

---

## Contributing

Feel free to fork this repository, make improvements, and submit a pull request! 🚀

---

## License

This project is licensed under the **MIT License**.
