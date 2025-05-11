# Aramco Chat 📊🛢️

A Streamlit-based chat application that allows users to interact with Aramco's yearly reports from 2019 to 2024. This application uses advanced natural language processing and document search capabilities to provide insights from Aramco's annual reports.

## Features

- 💬 Interactive chat interface for querying Aramco's yearly reports
- 🔍 Semantic search across reports from 2019 to 2024
- 📅 Year-specific filtering of information
- 🤖 AI-powered responses using GPT-4.1-mini
- 📚 Document retrieval using ChromaDB and Sentence Transformers

## Prerequisites

- Python 3.x
- OpenAI API key
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aramco_chat
```

2. Install the required packages:
```bash
pip install streamlit openai chromadb sentence-transformers python-dotenv
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run aramco.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Start chatting with the application! You can:
   - Ask questions about specific years (2019-2024)
   - Query financial information
   - Request insights about operations
   - Get information about specific topics

## Features in Detail

- **Chat Interface**: A clean, user-friendly interface for interacting with the reports
- **Year Filtering**: Automatically detects and filters by year when mentioned in queries
- **Document Search**: Uses semantic search to find relevant information from the reports
- **Context-Aware Responses**: Maintains chat history for more coherent conversations
- **Reset Capability**: Option to start a new chat session at any time

## Technical Details

- Uses `sentence-transformers` with the "all-mpnet-base-v2" model for document embeddings
- Implements ChromaDB for persistent vector storage
- Leverages OpenAI's GPT-4.1-mini for generating responses
- Built with Streamlit for a responsive web interface

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your license information here]
