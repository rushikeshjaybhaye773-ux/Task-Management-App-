# Task Management Application — Hairdrama Tech Assignment

## Overview
A full-stack task management application built with Next.js, Flask, Supabase, Google OAuth 2.0, and Gmail API.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                         │
│              Next.js + TypeScript (Frontend)                │
│                    Vercel Deployment                        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP REST API calls
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask REST API (Backend)                  │
│                    Render Deployment                         │
│  Routes:                                                    │
│   POST /api/auth/google  → Google Token Verification        │
│   GET  /api/tasks/       → Fetch Tasks                     │
│   POST /api/tasks/       → Create Task                     │
│   PUT  /api/tasks/<id>/complete → Complete Task             │
│   GET  /api/users/       → Fetch All Users                 │
└──────────┬──────────────────────────┬───────────────────────┘
           │                          │
           ▼                          ▼
┌─────────────────────┐   ┌─────────────────────────────────┐
│  Supabase PostgreSQL │   │        Gmail API                │
│  (Database)          │   │  (Email Notifications)          │
│  Tables:             │   │  - New task assigned email      │
│   - users            │   │  - Task completed email         │
│   - tasks            │   └─────────────────────────────────┘
└─────────────────────┘
           ▲
┌─────────────────────┐
│  Google OAuth 2.0   │
│  (Authentication)   │
│  - ID Token verify  │
└─────────────────────┘
```

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Next.js 16 + TypeScript + Tailwind CSS |
| Backend | Flask (Python 3) |
| Database | Supabase (PostgreSQL) |
| Authentication | Google OAuth 2.0 |
| Email | Gmail API |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |

## Features
- ✅ Google OAuth 2.0 Login (Gmail accounts)
- ✅ Create new tasks with title & description
- ✅ Assign tasks to other registered users
- ✅ Gmail email notification when a task is assigned
- ✅ Mark tasks as completed
- ✅ Gmail email notification when a task is completed
- ✅ Dashboard showing all tasks created by or assigned to user

## Project Structure
```
task-management-app/
├── backend/                  # Flask REST API
│   ├── routes/
│   │   ├── auth.py           # Google OAuth token verification
│   │   ├── tasks.py          # Task CRUD operations
│   │   └── users.py          # User management
│   ├── services/
│   │   ├── supabase_client.py  # Supabase DB connection
│   │   └── gmail_service.py    # Gmail API integration
│   ├── app.py                # Flask app entry point
│   ├── config.py             # Configuration from .env
│   └── requirements.txt      # Python dependencies
├── frontend/                 # Next.js TypeScript app
│   └── src/
│       ├── app/
│       │   ├── login/        # Google OAuth login page
│       │   ├── dashboard/    # Task dashboard
│       │   └── tasks/create/ # Create task form
│       ├── components/
│       │   └── GoogleAuthProvider.tsx
│       └── lib/
│           └── api.ts        # Axios API client
├── migrations/
│   └── 001_initial_schema.sql  # Supabase DB schema
├── .env.example              # Environment variable template
└── README.md
```

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account
- Google Cloud Console project

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp ../.env.example .env  # Fill in your values
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
# Create .env.local with required variables
npm run dev
```

### Database Setup
Run `migrations/001_initial_schema.sql` in your Supabase SQL editor.

## Environment Variables

### Backend (`backend/.env`)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
GOOGLE_CLIENT_ID=your_google_client_id
```

### Frontend (`frontend/.env.local`)
```
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

## Deployment
- **Frontend**: Deployed on [Vercel](https://vercel.com)
- **Backend**: Deployed on [Render](https://render.com)
- **Database**: [Supabase](https://supabase.com) (managed PostgreSQL)
