# How To Use Eloria AI Assistant

This guide explains how to set up and use Eloria, even if you have **no technical or AI experience**.

---

## 1. Requirements

Before you start, you need:

- A computer (Windows, macOS, or Linux)
- Python 3 installed (https://www.python.org/downloads/)
- A web browser (Chrome, Firefox, Edge, etc.)
- Internet connection for initial setup (optional for local-only AI)

---

## 2. Download Eloria

1. Go to the GitHub repository:
   https://github.com/your-username/eloria

2. Click the green **Code** button and select **Download ZIP**

   OR

   If you know Git, clone the repo with:

   git clone https://github.com/your-username/eloria.git

3. Extract the ZIP file (if downloaded as ZIP) to a folder you can easily find.

---

## 3. Install Python Dependencies

Open a terminal or command prompt:

- Windows: Press Win + R, type cmd, hit Enter
- macOS: Press Cmd + Space, type Terminal, hit Enter
- Linux: Open your preferred terminal

Navigate to the folder where Eloria is located, for example:

cd path/to/eloria

Install required Python packages:

pip install -r requirements.txt

This will install Flask and any other necessary libraries.

---

## 4. Configure API Key

Open the config.yaml file in a text editor (Notepad, VS Code, Sublime, etc.)

Replace the placeholder with your API key:

litellm_api_key: "YOUR_KEY_HERE"

Save the file.

Note: Keep your key private — do not share it publicly.

---

## 5. Run Eloria

In the terminal, ensure you are in the Eloria folder.

Run the Flask app:

python app.py

Wait for it to start. You should see a message like:

* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Open your browser and go to:

http://localhost:5000

---

## 6. Using Eloria

- Type your message in the chat input and press Enter
- Use the emoji picker to add emojis
- Click the + button to inject memory JSON files
- Explore the side drawer for history, settings, prompts, and memory
- The splash screen appears when the app loads

---

## 7. Exiting Eloria

- Close the browser tab to stop interacting
- Stop the server in the terminal with CTRL + C

---

## 8. Tips for Non-Technical Users

- Keep the terminal open while using Eloria
- Only modify config.yaml for API keys
- Do not change other files unless instructed by the project owner
- Read LICENSE_AND_USAGE.md for full rules on usage and contributions.
