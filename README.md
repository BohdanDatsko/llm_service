# LLM Client Manager Service

This project implements a simple FastAPI service that manages multiple Large Language Model (LLM) clients. The service exposes a single HTTP endpoint (`/generate`) that forwards a prompt to the selected LLM client and returns the generated response in a unified JSON format.

## Features

* **REST API**: Built with FastAPI for high‑performance asynchronous processing.
* **Extensible LLM clients**: A factory pattern is used to register and instantiate LLM clients based on a name. Adding new clients is as easy as creating a new class that implements the common interface and updating the registry.
* **Single endpoint**: The `/generate` endpoint accepts a prompt and client name, then returns the generated text in JSON format.
* **SOLID principles**: Each client is isolated behind a shared interface, promoting the Open/Closed principle. The manager uses a factory pattern to decouple client selection from request handling.

## Getting Started

### Prerequisites

* Python 3.9 or newer

### Installation

Clone this repository and install the dependencies:

```bash
git clone https://github.com/yourusername/llm_service.git
cd llm_service
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuration

API keys for external providers (such as OpenAI) are loaded from environment variables. You can set them in a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The service uses `python‑dotenv` to load environment variables automatically when the application starts.

### Running the Service

To start the development server on port 8000, run:

```bash
uvicorn llm_service.main:app --reload
```

The API will be available at `http://localhost:8000`. You can open the automatically generated documentation at `http://localhost:8000/docs`.

### Example Request

Send a POST request to `/generate` with JSON body containing a `prompt` and the `client_name` you want to use. For example, using `curl`:

```bash
curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, world!", "client_name": "dummy"}'

# Response:
{
  "response": "Echo: Hello, world!"
}
```

If you have configured an OpenAI API key and select the `openai` client, the service will forward the prompt to OpenAI and return the model's answer.

### Adding New Clients

1. Create a new class in `llm_service/clients` that inherits from `LLMClient` and implements the `generate` method.
2. Register the class in the `_clients` dictionary of `llm_service/manager.py` with an appropriate key.
3. No changes to the existing API or business logic are necessary.

### Running Tests

Tests are written with `pytest`. To run them, install the development dependencies and invoke `pytest`:

```bash
pip install -r dev-requirements.txt
pytest
```

### Docker

An example `Dockerfile` is provided. Build and run the image as follows:

```bash
docker build -t llm_service .
docker run -p 8000:8000 --env-file .env llm_service
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.