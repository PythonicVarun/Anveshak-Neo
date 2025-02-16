# Anveshak Neo 🤖

Anveshak Neo is an AI-powered chatbot that detects emotions from text input. It provides real-time emotional analysis using a trained model, allowing users to engage in meaningful conversations. The chatbot stores past conversations in a PostgreSQL database using SQLAlchemy ORM, enabling users to revisit and continue previous chats.

## Features ✨

- **Emotion Detection**: Analyzes text input to determine the user's emotional state.
- **Chat History Management**: Stores past conversations in a PostgreSQL database.
- **User-Friendly Interface**: Built with Streamlit for a seamless chat experience.
- **Multi-Session Support**: Allows users to navigate between different chat sessions.
- **AI-Powered Responses**: Utilizes an LLM model to generate intelligent replies.
- **Delete Chat Option**: Users can remove unwanted chat sessions.

## Tech Stack 🛠️

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python, SQLAlchemy ORM
- **Database**: PostgreSQL
- **AI Model**: LLM - Gemini

## Dataset 📊
Anveshak Neo is trained on the [Emotion Raw Dataset](https://huggingface.co/datasets/Rizqi/emotion-raw), which contains labeled emotion data for accurate sentiment analysis.

## Installation 🚀

1. Clone the repository:
   ```sh
   git clone https://github.com/PythonicVarun/Anveshak-Neo.git
   cd Anveshak-Neo
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the PostgreSQL database and update the `.env` configuration.
5. Run the chatbot:
   ```sh
   python run.py
   ```

## Running with Docker 🐳
To run Anveshak Neo using Docker, follow these steps:

1. Ensure you have [Docker](https://www.docker.com/) installed on your system.
2. Build and start the services using Docker Compose:
   ```sh
   docker-compose up --build
   ```
3. The PostgreSQL database and chatbot service will start automatically.
4. Access the chatbot at `http://localhost:8501/`.

## Environment Variables 🌍
Create a `.env` file based on `.env.example` and update the required credentials:
```
# Database Configuration
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db_name

# API Key for Gemini
GEMINI_API_KEY=your_gemini_api_key

# Database URL
DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@localhost:5432/your_postgres_db_name

# Logging
LOG_LEVEL=DEBUG
```

## Usage 📝

### 1️⃣ Starting a New Chat
- Click **"Start New Chat"** in the sidebar to begin a fresh conversation.
- A new chat session is created and stored in the database.

### 2️⃣ Navigating Between Chats
- Previous chats are displayed in the sidebar.
- Click on any chat title to continue a past conversation.

### 3️⃣ Sending Messages
- Type your message in the input box and press enter.
- Anveshak Neo will analyze and respond with an emotion-based reply.

### 4️⃣ Deleting a Chat
- Click the ❌ button next to a chat title in the sidebar to delete it.

## Project Structure 📂

```
Anveshak-Neo/
├── .env.example
├── LICENSE
├── README.md
├── docker-compose.yml
├── models/
│   ├── dataset/
│   │   └── emotion_dataset_raw.csv
│   └── text_emotion.pkl
├── requirements-dev.txt
├── requirements.txt
├── results/
├── run.py
├── src/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── emotions.py
│   │   │   └── llm_response.py
│   │   ├── database/
│   │   │   └── db.py
│   │   ├── main.py
│   │   └── stylesheets/
│   │       └── styles.css
├── train-v2.py
└── train.py
```

## Future Enhancements 🚀
- Implement voice input and output.
- Add support for multiple languages.
- Improve emotion detection with deep learning models.
- Integrate with external APIs for enhanced chatbot capabilities.

## Contributing 🤝
Contributions are welcome! Feel free to submit a pull request or open an issue.

## License 📜
See the [BSD 3-Clause License](https://github.com/PythonicVarun/Anveshak-Neo/blob/master/LICENSE) for more details.

---

This project needs a star️ from you. Don't forget to leave a star✨
Follow my Github for content
<br>
<hr>
<h6 align="center">© Varun Agnihotri 2025 
<br>
All Rights Reserved</h6>
