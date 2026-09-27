# Poetry Agent

A Python-based AI poetry generator that creates Urdu and English poems using the OpenAI Agents SDK and Gemini models. It includes a Streamlit web app and a FastAPI API server, with built-in guardrails to keep prompts and responses focused on poetry generation.

## Features

- Generate poems in Urdu and English
- Bilingual poetry prompts and outputs
- Streamlit web interface
- FastAPI server endpoint for API access
- Input and output guardrails for poetry-specific requests
- Simple Windows launcher via `run.bat`

## Project Structure

- `main.py` – agent logic, guardrails, and session handling
- `connection.py` – Gemini/OpenAI client configuration
- `streamlit_app.py` – Streamlit UI
- `server.py` – FastAPI API server
- `run.bat` – Windows launcher for starting the app or API
- `requirements.txt` or `pyproject.toml` – project dependencies
- `.env` – local environment variables (not committed)

## Tech Stack

- Python 3.10+
- Streamlit
- FastAPI
- OpenAI Agents SDK
- Gemini API
- Python-dotenv

## Prerequisites

- Python 3.10 or newer
- A valid Gemini API key
- Git installed on your system

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Roshaank20/AI-Poetry.git
   cd AI-Poetry
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Or if you are using Poetry:

   ```bash
   poetry install
   ```

4. Create a `.env` file in the project root:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   You can also copy from `.env.example` if present.

## Run the App

### Option 1: Windows launcher

Double-click `run.bat` or run it from Command Prompt:

```bash
run.bat
```

Then select:
- `1` for the Streamlit app
- `2` for the FastAPI server

### Option 2: Streamlit app directly

```bash
streamlit run streamlit_app.py
```

### Option 3: FastAPI server directly

```bash
python server.py
```

## Example Usage

Open the Streamlit app and enter a prompt like:

```text
Write a short Urdu ghazal about rain.
```

Or send a POST request to the FastAPI endpoint if your API server is running.

## Environment Notes

The app reads the API key from the `GEMINI_API_KEY` environment variable. Make sure it is set before running the app.

## GitHub Upload Checklist

Before uploading to GitHub:

- Ensure your `.env` file is not committed
- Add `.env` to `.gitignore`
- Keep `README.md` updated
- Commit the project files and push to GitHub

Example `.gitignore`:

```gitignore
.env
__pycache__/
.venv/
*.pyc
```

## License

This project is provided for educational and personal use. Add your preferred license if you plan to publish it publicly.

## Author

Your Name

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the proposal.
