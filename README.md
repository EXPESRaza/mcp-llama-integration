# Model Context Protocol Server with Llama Integration

This repository contains a Model Context Protocol (MCP) server implementation that integrates with a locally running Llama model. The MCP server provides a standardized interface for context retrieval, enhancing AI applications with relevant information from a local LLM.

## Overview

The project consists of two main components:

1. **MCP Server** - A FastAPI-based server that implements the Model Context Protocol and forwards queries to a local Llama model
2. **Python Client** - A sample client application that demonstrates how to interact with the MCP server

## Prerequisites

- Python 3.7 or higher
- A running Llama model server (e.g., Ollama) at http://localhost:11434/
- Git installed on your machine
- GitHub account

## Installation

### Clone the Repository

```bash
git clone https://github.com/EXPESRaza/mcp-llama-integration.git
cd mcp-llama-integration
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## File Structure

```
mcp-llama-integration/
├── llama_mcp_server.py      # MCP server with Llama integration
├── llama_client_app.py      # Sample client application
└── README.md                # Project documentation
```

## Setting Up the Llama Model

1. If you haven't already, install [Ollama](https://ollama.ai/download)
2. Pull the Llama model:
   ```bash
   ollama pull llama3.2
   ```
3. Verify the model is running:
   ```bash
   curl http://localhost:11434/api/tags
   ``` browser
   http://localhost:11434
   http://localhost:11434/api/tags
   ```
   ![image](https://github.com/user-attachments/assets/6ad22789-4e86-4732-8305-fd8afded8321)


## Running the MCP Server

1. Start the server:
   ```bash
   python llama_mcp_server.py
   ```
2. The server will start running on `http://localhost:8000`
3. You can verify the server is running by checking the health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```
   ![image](https://github.com/user-attachments/assets/ca97173e-0dec-4f2e-865d-4f87c082091d)

   ![image](https://github.com/user-attachments/assets/de781fe7-3830-45a0-b719-d2924a6a1df1)


## Using the Client Application

1. In a separate terminal, start the client application:
   ```bash
   python llama_client_app.py
   ```
2. The application will prompt you for input
3. Type your queries and receive responses from the Llama model
4. Type 'exit' to quit the application

   ![image](https://github.com/user-attachments/assets/1bbe216d-0201-4a72-9384-5ed6d28fa5aa)


## API Documentation

### MCP Server Endpoints

#### POST /context

Request a context for a given query.

**Request Body:**

```json
{
  "query_text": "Your query here",
  "user_id": "optional-user-id",
  "session_id": "optional-session-id",
  "additional_context": {}
}
```

**Response:**

```json
{
  "context_elements": [
    {
      "content": "Response from Llama model",
      "source": "llama_model",
      "relevance_score": 0.9
    }
  ],
  "metadata": {
    "processing_time_ms": 150,
    "model": "llama3",
    "query": "Your query here"
  }
}
```

#### GET /health

Check the health status of the MCP server and its connection to the Llama model.

**Response:**

```json
{
  "status": "healthy",
  "llama_status": "connected"
}
```

## Customization

### Changing the Llama Model

If you want to use a different Llama model, modify the `model` parameter in the `query_llama` function in `llama_mcp_server.py`:

```python
payload = {
    "model": "your-model-name",  # Change this to your model name
    "prompt": text,
    "stream": False
}
```

### Modifying the Prompt Template

To change how queries are formatted before sending to Llama, update the prompt template in the `get_context` function:

```python
prompt = f"""Please provide relevant information for the following query:
{request.query_text}

Respond with factual, helpful information."""
```

## Troubleshooting

### Common Issues

1. **Connection Refused Error**

   - Make sure the Llama model is running at http://localhost:11434/
   - Verify Ollama is properly installed and running

2. **Model Not Found Error**

   - Ensure you've pulled the correct model with Ollama
   - Check available models with `ollama list`

3. **Slow Responses**
   - Llama model inference can be resource-intensive
   - Consider using a smaller model if performance is an issue

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
