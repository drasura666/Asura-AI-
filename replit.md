# Asura-AI Chat Application

## Overview

This is a Flask-based web application featuring an AI chatbot named "Asura-AI" that specializes in advanced scientific topics. The system provides an interactive chat interface where users can ask questions about cutting-edge physics, space technology, and futuristic scientific concepts.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python
- **Structure**: Simple three-file backend structure
  - `app.py`: Main Flask application with routes
  - `chatbot.py`: Core AI chatbot logic and knowledge processing
  - `main.py`: Application entry point
- **API Design**: RESTful API with JSON responses
- **Error Handling**: Comprehensive try-catch blocks with proper HTTP status codes

### Frontend Architecture
- **Template Engine**: Jinja2 templates (Flask default)
- **Styling**: Bootstrap 5 with custom CSS for dark theme
- **JavaScript**: Vanilla JavaScript for chat functionality
- **Responsive Design**: Mobile-friendly interface using Bootstrap grid system

### Knowledge Base System
- **Storage**: JSON files organized by scientific topics
- **Topics Covered**: 
  - Black holes and dimensional physics
  - Space-time manipulation
  - Prāṇika technology (fictional multi-form substances)
  - Space colonization
  - Advanced renewable energy
  - Waste processing systems
- **Matching Algorithm**: Pattern matching and keyword-based response selection

## Key Components

### Chat Interface (`app.py`)
- Route handlers for main interface and API endpoints
- Session management with secret key configuration
- Error handling with appropriate HTTP status codes
- JSON-based communication between frontend and backend

### AI Processing Engine (`chatbot.py`)
- Knowledge base loader that reads JSON files from `/knowledge` directory
- Text preprocessing with regex cleaning and normalization
- Response matching using keywords and patterns
- Similarity scoring for finding best matches (using difflib)

### Frontend Components
- Real-time chat interface with message history
- Typing indicators and loading states
- Auto-resizing input fields
- Topic information display bar

### Knowledge System
Each JSON file contains:
- Topic metadata (name, description, context)
- Response patterns with keywords and exact phrase matches
- Detailed technical responses about fictional advanced technologies

## Data Flow

1. **User Input**: User types message in web interface
2. **Frontend Processing**: JavaScript validates input and sends POST request to `/api/chat`
3. **Backend Processing**: Flask receives request and passes message to AsuraAI chatbot
4. **Knowledge Matching**: Chatbot preprocesses text and searches knowledge base for matching patterns
5. **Response Generation**: Best matching response is selected based on keyword similarity
6. **Response Delivery**: JSON response sent back to frontend
7. **UI Update**: JavaScript displays both user message and AI response in chat interface

## External Dependencies

### Python Packages
- Flask: Web framework
- Standard library modules: `os`, `logging`, `json`, `re`, `difflib`, `typing`

### Frontend Dependencies
- Bootstrap 5: UI framework (loaded via CDN)
- Font Awesome: Icons (loaded via CDN)
- No JavaScript frameworks - uses vanilla JS

### Development Dependencies
- No database system currently implemented
- No external AI APIs - uses local knowledge base
- No authentication system

## Deployment Strategy

### Current Configuration
- **Host**: Configured for `0.0.0.0` (all interfaces)
- **Port**: 5000
- **Debug Mode**: Enabled for development
- **Session Secret**: Environment variable with fallback default

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key (optional, has default)

### File Structure Requirements
- `/static/`: CSS and JavaScript files
- `/templates/`: HTML templates
- `/knowledge/`: JSON knowledge base files
- All knowledge files must be valid JSON with specific schema

### Scaling Considerations
- Stateless design allows for easy horizontal scaling
- Knowledge base is loaded into memory on startup
- No persistent data storage currently implemented
- Session management uses Flask's built-in system

## Recent Changes

### July 31, 2025
- **XSS Security Fix**: Replaced unsafe innerHTML usage with secure DOM manipulation methods in chat.js
- **Custom Knowledge Integration**: Added comprehensive knowledge base for user's research projects including:
  - STORMCORE Reactor (lightning energy harvesting)
  - A's Binder (sustainable road composite)
  - The Colour of Emptiness (vacuum perception theory)
  - MDMG Theory (magnetic dark matter generation)
  - Hidden Nature of Light (electromagnetic field analysis)
- **Knowledge Base Expansion**: System now loads 8 knowledge topics (up from 7)
- **Enhanced AI Capability**: AI can now discuss user's independent research work in detail

## Notes for Development

- The application currently uses a local JSON-based knowledge system instead of a traditional database
- All responses are pre-written and matched using pattern recognition
- The AI persona combines fictional advanced scientific concepts with real user research projects
- Error handling includes both technical logging and user-friendly responses
- The chat interface supports real-time conversation flow with proper UX indicators
- Security: XSS vulnerability resolved using safe DOM methods instead of innerHTML