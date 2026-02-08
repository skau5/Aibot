# AI English Tutor Bot

A Flask-based AI agent that helps users learn English using OpenAI's GPT-4o-mini model.

## Features

- 🤖 AI-powered English tutoring
- 💬 Conversation memory per user
- 🛡️ Robust error handling
- 🔐 Secure API key management

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your OpenAI API key
4. Run: `python app.py`

## API Usage

### Health Check
```
GET /
```

### Chat with AI Agent
```
POST /agent
Content-Type: application/json

{
    "user_id": "unique_user_id",
    "message": "Your message here"
}
```

## Production Deployment

### Deploy to Railway
1. Fork this repository
2. Sign up at [Railway](https://railway.app)
3. Create new project from GitHub repo
4. Add environment variable: `OPENAI_API_KEY=your-key`
5. Deploy automatically

### Deploy to Render
1. Fork this repository
2. Sign up at [Render](https://render.com)
3. Create new Web Service from GitHub repo
4. Add environment variable: `OPENAI_API_KEY=your-key`
5. Deploy automatically

### Deploy to Heroku
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `heroku config:set OPENAI_API_KEY=your-key`
4. `git push heroku main`

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `PORT` - Port number (optional, defaults to 5000)