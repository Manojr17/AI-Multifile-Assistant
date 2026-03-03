# 🤖 AI-Based Smart File Assistant

An intelligent document management and query system that uses RAG (Retrieval-Augmented Generation) to help users extract information from multiple documents efficiently.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Milestones](#milestones)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The AI-Based Smart File Assistant is a web application that allows users to upload multiple documents (PDF, DOCX, TXT) and query them using natural language. The system uses advanced AI techniques including:

- **RAG (Retrieval-Augmented Generation)** for accurate context-aware responses
- **Vector embeddings** for semantic search
- **Pinecone** for efficient vector storage and retrieval
- **OpenAI GPT** for intelligent response generation
- **User authentication** for personalized document management

## ✨ Features

### Core Features
- 📁 **Multi-format Document Upload** - Support for PDF, DOCX, TXT, and more
- 🔍 **Intelligent Query System** - Ask questions in natural language
- 🎯 **Context-Aware Responses** - Get accurate answers based on your documents
- 👤 **User Authentication** - Secure login and registration system
- 📊 **Document Management** - View, organize, and delete uploaded documents
- 💬 **Chat History** - Track all your queries and responses
- 🔐 **Individual User Indexes** - Each user has their own isolated document space

### Advanced Features
- **Semantic Search** - Uses MiniLM embeddings for accurate document retrieval
- **Chunk-based Processing** - Efficiently handles large documents
- **Source Attribution** - Shows which documents were used for each answer
- **Real-time Processing** - Instant document processing and indexing
- **Responsive UI** - Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **SQLite** - Database for user and document management
- **Pinecone** - Vector database for embeddings
- **OpenAI API** - GPT-3.5-turbo for response generation
- **LangChain** - RAG pipeline orchestration
- **Sentence Transformers** - Document embeddings (MiniLM)

### Frontend
- **HTML5/CSS3**
- **JavaScript (Vanilla)**
- **Responsive Design**

### Document Processing
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX processing
- **LangChain Document Loaders** - Multi-format support

## 📁 Project Structure

```
AI-Multifile-Assistant/
├── Milestone1/                 # Basic Python implementations
│   ├── main.py                # Main entry point
│   ├── task2.py               # File operations
│   ├── task3.py               # Data structures
│   └── task4.py               # Advanced concepts
│
├── Milestone2/                 # RAG system development
│   ├── prompt_template.py     # LLM prompt engineering
│   ├── task5.py               # Document loading
│   ├── task6.py               # Text chunking
│   ├── task7.py               # Embeddings generation
│   └── task8.py               # Vector storage
│
├── Milestone3/                 # Full web application
│   ├── app_new.py             # Flask application
│   ├── auth.py                # Authentication system
│   ├── config.py              # Configuration management
│   ├── database.py            # Database operations
│   ├── document_processor.py  # Document processing pipeline
│   ├── embeddings.py          # Embedding generation
│   ├── pinecone_manager.py    # Pinecone operations
│   ├── rag_system.py          # RAG implementation
│   ├── requirements.txt       # Python dependencies
│   │
│   ├── routes/                # API routes
│   │   ├── api_routes.py      # Document and query APIs
│   │   ├── auth_routes.py     # Authentication APIs
│   │   └── main_routes.py     # Page rendering routes
│   │
│   ├── static/                # Frontend assets
│   │   ├── script.js          # JavaScript functionality
│   │   ├── styles.css         # Styling
│   │   └── uploads/           # Uploaded documents
│   │
│   └── templates/             # HTML templates
│       ├── auth.html          # Login/Register page
│       ├── dashboard_page.py  # Dashboard template
│       ├── landing_page.py    # Home page template
│       └── profile_page.py    # User profile template
│
└── .env                       # Environment variables (not in repo)
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- OpenAI API key
- Pinecone API key

### Step 1: Clone the Repository
```bash
git clone https://github.com/Manojr17/AI-Multifile-Assistant.git
cd AI-Multifile-Assistant
```

### Step 2: Install Dependencies
```bash
cd Milestone3
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the `Milestone3` directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_pinecone_index_name_here
```

### Step 4: Run the Application
```bash
python app_new.py
```

The application will be available at `http://127.0.0.1:5000`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `PINECONE_API_KEY` | Your Pinecone API key | Yes |
| `PINECONE_INDEX_NAME` | Name for your Pinecone index | Yes |

### Application Settings (config.py)

```python
# Document processing configuration
CHUNK_CONFIG = {
    "chunk_size": 2000,        # Characters per chunk
    "chunk_overlap": 200,      # Overlap between chunks
    "min_chunk_length": 100,   # Minimum chunk size
    "max_chunks_per_doc": 500  # Maximum chunks per document
}

# Supported file formats
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 
                      'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'}
```

## 📖 Usage

### 1. Register/Login
- Navigate to `http://127.0.0.1:5000`
- Create a new account or login with existing credentials

### 2. Upload Documents
- Click on the "Upload" tab
- Select one or multiple documents
- Wait for processing to complete

### 3. Query Your Documents
- Go to the "Query" tab
- Type your question in natural language
- Get AI-powered responses with source citations

### 4. Manage Documents
- View all uploaded documents in the dashboard
- Delete documents you no longer need
- Check processing statistics

## 🎯 Milestones

### Milestone 1: Python Fundamentals
- Basic Python programming concepts
- File operations and data structures
- Object-oriented programming
- Error handling and best practices

### Milestone 2: RAG System Development
- Document loading and processing
- Text chunking strategies
- Embedding generation with Sentence Transformers
- Vector storage with Pinecone
- Prompt engineering for legal documents

### Milestone 3: Full-Stack Web Application
- Flask web application
- User authentication and authorization
- Document upload and processing pipeline
- RAG-based query system
- Responsive web interface
- Database management
- API development

## 🔌 API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout

### Document Management
- `POST /api/upload` - Upload documents
- `GET /api/documents` - Get user's documents
- `DELETE /api/documents/<id>` - Delete document

### Query System
- `POST /api/query` - Query documents
- `GET /api/chat-history` - Get chat history
- `POST /api/clear-chat-history` - Clear chat history

### Statistics
- `GET /api/pinecone-stats` - Get Pinecone statistics

## 📸 Screenshots

### Landing Page
The home page with login/register options.

### Dashboard
View all uploaded documents and their processing status.

### Query Interface
Ask questions and get AI-powered responses with source citations.

### Document Upload
Easy drag-and-drop interface for uploading multiple documents.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is part of the Springboard Internship Program 2025.

## 👨‍💻 Author

**Manoj R**
- GitHub: [@Manojr17](https://github.com/Manojr17)
- Email: manoravi39@gmail.com

## 🙏 Acknowledgments

- Springboard Internship Program 2025
- OpenAI for GPT API
- Pinecone for vector database
- LangChain community
- Sentence Transformers team

## 📞 Support

For support, email manoravi39@gmail.com or open an issue in the GitHub repository.

---

**Note:** Make sure to keep your API keys secure and never commit them to the repository. Always use environment variables for sensitive information.
