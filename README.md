# SkillSprint AI 🚀

![AI-Powered](https://img.shields.io/badge/AI-Powered-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-18-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue)
![pgvector](https://img.shields.io/badge/pgvector-enabled-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

**AI-powered learning roadmap generator with intelligent practice recommendations**

SkillSprint AI creates personalized, week-by-week learning plans for any skill using OpenAI GPT-4o-mini, then recommends specific practice problems and resources using semantic search with vector embeddings.

---

## 🌟 Features

### Core Features
- **🤖 AI-Powered Roadmap Generation** - GPT-4o-mini creates personalized learning plans with adaptive clarifying questions
- **🎯 Smart Practice Recommendations** - AI-powered semantic search recommends relevant problems/resources using vector embeddings (pgvector)
- **🌐 Universal Domain Support** - AI automatically detects and supports ANY learning domain (coding, languages, business, etc.)
- **📊 Progress Tracking** - Visual progress bars, statistics, and timeline views with real-time updates
- **📤 Export & Share** - Download professional PDFs and generate shareable read-only links
- **📚 Roadmap Library** - Manage multiple roadmaps with automatic progress persistence
- **🔒 User Authentication** - Secure JWT-based auth with user-specific data isolation
- **🎨 Modern UI/UX** - Clean, responsive design with Tailwind CSS and smooth animations

### Advanced AI Features
- **Topic-Specific Recommendations** - Each week gets unique practice items based on its specific focus (no repetition)
- **Automatic Library Expansion** - System generates new practice items on-demand for any topic
- **Relevance Boosting** - Prioritizes items matching week focus and topics using intelligent scoring
- **Domain Detection** - AI automatically classifies learning goals into appropriate domains

---

## 🏗️ Tech Stack

**Backend**
- FastAPI (Python) - Modern async web framework
- PostgreSQL + pgvector - Database with vector similarity search
- SQLAlchemy - ORM with relationship management
- Alembic - Database migrations
- OpenAI GPT-4o-mini - AI generation & text embeddings
- ReportLab - PDF generation
- JWT Authentication - python-jose + bcrypt

**Frontend**
- React 18 - UI library with hooks
- Vite - Fast build tool
- Tailwind CSS - Utility-first styling
- Axios - HTTP client

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+ with pgvector extension
- OpenAI API key

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/jayesh55555/SkillSprint-AI.git
cd SkillSprint-AI
```

**2. Database Setup**
```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE skillsprint;
\c skillsprint
CREATE EXTENSION vector;
\q
```

**3. Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env
# Edit .env with your credentials:
# - DATABASE_URL=postgresql://user:password@localhost:5432/skillsprint
# - OPENAI_API_KEY=your_openai_api_key_here
# - SECRET_KEY=your_secret_key_here (generate with: openssl rand -hex 32)

# Run database migrations
alembic upgrade head

# Seed practice items (optional - system auto-generates on-demand)
python seed_practice_items.py

# Start backend server
uvicorn app.main:app --reload --port 8000
```

**4. Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**5. Open your browser**
```
http://localhost:3000
```

---

## 📋 API Endpoints

### Public Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `POST /ai/clarify` - Generate clarifying questions
- `GET /share/{public_id}` - View shared roadmap (read-only)

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info (protected)

### Roadmaps (Protected)
- `GET /roadmaps/` - List user's roadmaps with progress
- `POST /roadmaps/create` - Create roadmap manually
- `GET /roadmaps/{id}` - Get roadmap details
- `DELETE /roadmaps/{id}` - Delete roadmap
- `POST /ai/generate-roadmap` - Generate AI-powered roadmap
- `GET /roadmaps/{id}/export/pdf` - Export as PDF
- `POST /roadmaps/{id}/share` - Generate share link

### Progress Tracking (Protected)
- `PATCH /weeks/{id}/complete` - Toggle week completion
- `GET /weeks/{id}/status` - Get week status
- `GET /roadmaps/{id}/progress` - Get progress statistics

### Practice Recommendations (Protected)
- `GET /recommendations/{week_id}` - Get AI-recommended practice items for a week

---

## � User Flow

1. **Landing Page** → Click "Get Started"
2. **Sign Up/Login** → Create account or login
3. **My Roadmaps** → View library or create new roadmap
4. **Enter Goal** → "I want to learn Cybersecurity"
5. **Answer Questions** → AI asks 3-5 clarifying questions
6. **Generate** → AI creates personalized roadmap (10-30s)
7. **Get Recommendations** → AI suggests relevant practice problems/resources per week
8. **Track Progress** → Mark weeks complete as you learn
9. **Export/Share** → Download PDF or share with others

---

## 🎓 Example Use Cases

### Technical Skills
- **DSA & Coding** - Master algorithms for technical interviews
- **Machine Learning** - Build AI models from scratch
- **DevOps & Cloud** - Deploy scalable applications
- **Web Development** - Create modern full-stack apps
- **Mobile Development** - Build iOS & Android apps
- **Cybersecurity** - Learn ethical hacking and security
- **Blockchain** - Smart contracts and Web3 development

### Non-Technical Skills
- **Languages** - Learn German, Japanese, Spanish, etc.
- **Product Management** - Product strategy and execution
- **Business Skills** - Marketing, sales, leadership
- **Creative Skills** - Design, writing, music

**SkillSprint AI works with ANY learning goal!**

---

## 📊 Database Schema

```sql
users
├── id (PK)
├── email (unique)
├── full_name
└── hashed_password

roadmaps
├── id (PK)
├── user_id (FK)
├── goal
├── domain (AI-detected)
├── duration_weeks
├── created_at
└── public_id (unique, for sharing)

weekplans
├── id (PK)
├── roadmap_id (FK)
├── week_number
├── focus_title
├── topics_json (JSON)
├── tasks_json (JSON)
└── target_problems

progress
├── id (PK)
├── weekplan_id (FK)
└── completed (boolean)

practice_items
├── id (PK)
├── title
├── domain
├── topic
├── difficulty
├── link
├── description
├── tags (JSON)
└── embedding (vector(1536))

domain_expansions
├── id (PK)
├── domain
├── items_generated
├── is_expanding
└── created_at
```

---

## 🧠 How AI Recommendations Work

### 1. Domain Detection
When you create a roadmap, AI automatically detects the domain:
```
Goal: "I want to learn Blockchain development"
→ AI detects: "Blockchain"
→ Stored in database for efficient reuse
```

### 2. Topic-Specific Expansion
For each week, the system checks if practice items exist for that specific topic:
```
Week 2: "Smart Contracts"
→ Check: Do we have items tagged with "smart contracts"?
→ If < 3 items: Generate 12 new items specifically for smart contracts
→ Items tagged with "smart contracts" for future matching
```

### 3. Semantic Search with Relevance Boosting
Recommendations use vector similarity + tag matching:
```sql
Priority 3: Exact topic match (e.g., topic = "Smart Contracts")
Priority 2: Tag match (e.g., tags contain "smart contracts")
Priority 1: Domain match only (e.g., domain = "Blockchain")
→ Sort by priority, then by vector similarity
→ Return top 5 most relevant items
```

### Result
Each week gets unique, highly relevant practice items with minimal repetition!

---

## 🚀 Deployment

### Backend (Railway/Render/Heroku)
```bash
# Set environment variables
DATABASE_URL=your_postgres_url_with_pgvector
OPENAI_API_KEY=your_api_key
SECRET_KEY=your_secret_key

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy dist/ folder
```

**Important**: Ensure your production PostgreSQL has the `vector` extension installed.

---

## 📚 Project Structure

```
SkillSprint-AI/
├── backend/
│   ├── alembic/              # Database migrations
│   │   └── versions/         # Migration files (001-007)
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── ai.py         # AI generation & domain detection
│   │   │   ├── auth.py       # Authentication
│   │   │   ├── recommendations.py  # Practice recommendations
│   │   │   ├── roadmaps.py   # Roadmap CRUD
│   │   │   ├── share.py      # Public sharing
│   │   │   └── weeks.py      # Week progress
│   │   ├── core/             # Security, config, dependencies
│   │   ├── crud/             # Database operations
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic
│   │       ├── openai_service.py           # AI generation
│   │       ├── embedding_service.py        # Vector embeddings
│   │       ├── domain_detector.py          # AI domain detection
│   │       ├── practice_library_expander.py # Auto-expansion
│   │       └── pdf_service.py              # PDF export
│   ├── seed_practice_items.py  # Initial seed data
│   ├── .env.example          # Environment template
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Dashboard.jsx      # Main dashboard
│   │   │   ├── RoadmapView.jsx    # Roadmap display
│   │   │   ├── WeekCard.jsx       # Week with recommendations
│   │   │   ├── ClarifyGoal.jsx    # AI clarification
│   │   │   └── ...
│   │   └── context/          # Auth context
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
├── docs/                     # Documentation
│   ├── STEP9_SUMMARY.md      # Practice recommendations guide
│   ├── STEP9.4_SUMMARY.md    # AI domain detection guide
│   ├── STEP9.5_COMPLETE.md   # Topic-specific recommendations
│   ├── TROUBLESHOOTING.md    # Common issues
│   └── tests/                # Test scripts
└── README.md                 # This file
```

---

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/skillsprint
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend**
- API URL is hardcoded to `http://localhost:8000` for development
- Update in production to your backend URL

---


### Manual Testing
1. Create a roadmap with 8+ weeks
2. Get recommendations for different weeks
3. Verify each week gets unique items
4. Check items match week focus

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Jayesh Gulani**
- GitHub: [@jayesh55555](https://github.com/jayesh55555)
- Email: gulanijayesh55@gmail.com

**Project Link**: [https://github.com/jayesh55555/SkillSprint-AI](https://github.com/jayesh55555/SkillSprint-AI)

---

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐

---

## 🚀 What Makes SkillSprint AI Different?

### vs. Generic Roadmap Generators
- ✅ AI-powered clarification questions for personalized plans
- ✅ Specific practice recommendations, not just generic advice
- ✅ Progress tracking with visual feedback
- ✅ Works with ANY domain (not just coding)

### vs. Asking ChatGPT Directly
- ✅ Structured, week-by-week format
- ✅ Persistent roadmaps you can track over time
- ✅ Automatic practice item recommendations
- ✅ PDF export and sharing capabilities
- ✅ Progress tracking and statistics

### vs. Static Learning Platforms
- ✅ Personalized to YOUR goals and experience
- ✅ Adapts to ANY skill or technology
- ✅ AI-curated resources from across the web
- ✅ Flexible duration (1-52 weeks)

---

**Built with ❤️ by Jayesh Gulani**

⭐ Star this repo if you find it helpful!
