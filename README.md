# Physical AI & Humanoid Robotics - Hackathon Project

13-week comprehensive course on Physical AI and Humanoid Robotics, built with Docusaurus, featuring a RAG-powered chatbot and complete Week 1-2 content.

## Project Structure

```
Hackathon/
├── .claude/                          # Claude Code slash commands
│   └── commands/                     # 11 Spec-Kit Plus commands
│       ├── sp.adr.md
│       ├── sp.analyze.md
│       ├── sp.checklist.md
│       ├── sp.clarify.md
│       ├── sp.constitution.md
│       ├── sp.git.commit_pr.md
│       ├── sp.implement.md
│       ├── sp.phr.md
│       ├── sp.plan.md
│       ├── sp.specify.md
│       └── sp.tasks.md
│
├── .specify/                         # Spec-Kit Plus methodology
│   ├── memory/
│   │   └── constitution.md           # Project principles
│   ├── scripts/
│   │   ├── bash/                     # Unix/Linux/Mac scripts
│   │   │   ├── check-prerequisites.sh
│   │   │   ├── common.sh
│   │   │   ├── create-adr.sh
│   │   │   ├── create-new-feature.sh
│   │   │   ├── create-phr.sh
│   │   │   ├── setup-plan.sh
│   │   │   └── update-agent-context.sh
│   │   └── powershell/               # Windows scripts
│   │       ├── check-prerequisites.ps1
│   │       ├── common.ps1
│   │       ├── create-new-feature.ps1
│   │       ├── setup-plan.ps1
│   │       └── update-agent-context.ps1
│   └── templates/                    # Project templates
│       ├── adr-template.md
│       ├── agent-file-template.md
│       ├── checklist-template.md
│       ├── phr-template.prompt.md
│       ├── plan-template.md
│       ├── spec-template.md
│       └── tasks-template.md
│
├── book/                             # Docusaurus textbook
│   ├── docs/
│   │   ├── intro.md
│   │   └── weeks/
│   │       ├── week-01-02-physical-ai/  # ✅ Week 1-2 COMPLETE (9,916 words)
│   │       ├── week-03-05-ros2/         # ✅ Summary complete
│   │       ├── week-06-07-gazebo/       # ✅ Summary complete
│   │       ├── week-08-10-nvidia-isaac/ # ✅ Summary complete
│   │       ├── week-11-12-humanoid/     # ✅ Summary complete
│   │       └── week-13-conversational/  # ✅ Summary complete
│   ├── colab/
│   │   └── week-01-02/                # 5 Jupyter notebooks
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatBot/              # ✅ RAG ChatBot React component
│   │   │       ├── index.tsx
│   │   │       └── styles.module.css
│   │   └── theme/
│   │       └── Root.tsx              # ✅ Global ChatBot wrapper
│   ├── docusaurus.config.ts          # ✅ Configured for GitHub Pages
│   ├── sidebars.ts
│   └── package.json
│
├── chatbot-backend/                  # RAG Chatbot (OpenAI + FastAPI + Qdrant + Neon)
│   ├── main.py                       # FastAPI application
│   ├── ingest.py                     # Vector store ingestion
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   └── README.md                     # Setup instructions
│
├── history/                          # Spec-Kit Plus history
│   ├── adr/                          # Architecture Decision Records
│   └── prompts/                      # Prompt History Records
│       └── week-01-02-physical-ai/
│           ├── 001-week-01-02-spec-clarification.clarify.prompt.md
│           ├── 002-week-01-02-implementation-plan.plan.prompt.md
│           ├── 003-week-01-02-tasks-generation.tasks.prompt.md
│           └── 004-week-01-02-content-implementation.green.prompt.md
│
├── specs/                            # Feature specifications
│   └── main/
│       ├── code-examples/            # Python code examples
│       ├── content-outlines/         # Content planning
│       ├── diagram-sketches/         # Mermaid diagrams
│       ├── plan.md                   # Architecture plan
│       ├── research.md               # Research notes
│       ├── spec.md                   # Feature specification
│       └── tasks.md                  # Implementation tasks
│
├── CLAUDE.md                         # Claude Code configuration
├── IMPLEMENTATION_STATUS.md          # Week 1-2 validation report
└── README.md                         # This file
```

## Hackathon Requirements Met

### 1. Docusaurus Textbook ✅

- **Week 1-2**: 6 pages, 9,916 words (target: 8,000-12,000) ✅
- **Mermaid Diagrams**: 3+ diagrams ✅
- **Code Examples**: 5 Jupyter notebooks with Colab badges ✅
- **Video Embeds**: 5 YouTube videos (robot demos) ✅
- **Deep Dives**: 2+ collapsible admonitions ✅
- **Assessment**: 5 MCQ + 3 short-answer + 1 practical ✅
- **Citations**: 24 official sources (100% official) ✅
- **Build Status**: ✅ Successful (`npm run build`)

### 2. RAG Chatbot ✅

- **FastAPI**: Backend API with `/chat`, `/health`, `/feedback` endpoints ✅
- **OpenAI**: GPT-4o for responses, text-embedding-3-small for vectors ✅
- **Qdrant**: Vector database for semantic search ✅
- **Neon PostgreSQL**: Conversation logging and analytics ✅
- **Structure**: Complete with main.py, ingest.py, requirements.txt, README ✅

### 3. Spec-Kit Plus Structure ✅

- **`.claude/`**: 11 slash commands ✅
- **`.specify/`**: Templates, scripts (bash + PowerShell), constitution ✅
- **`history/`**: Prompt History Records (PHRs) for Week 1-2 ✅
- **`specs/`**: Feature specs, plans, tasks, research ✅

### 4. Bonus Features (Optional)

- [ ] **Subagents**: Specialized agents for different topics
- [ ] **Better-Auth**: User authentication system
- [ ] **Personalization**: User progress tracking
- [ ] **Urdu Translation**: Multilingual support

## Getting Started

### Prerequisites

- **Node.js 18+** (for Docusaurus)
- **Python 3.10+** (for chatbot backend)
- **Git** (for version control)

### 1. Setup Docusaurus Textbook

```bash
cd book
npm install
npm run start  # Development server at http://localhost:3000
npm run build  # Production build
```

### 2. Setup RAG Chatbot

```bash
cd chatbot-backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# Ingest course content
python ingest.py

# Start backend server
uvicorn main:app --reload  # http://localhost:8000
```

### 3. Deploy to GitHub Pages

**Automatic Deployment** (Recommended):
```bash
# Push to main branch - GitHub Actions will auto-deploy
git add .
git commit -m "Deploy updates"
git push origin main

# Site will be available at: https://khizra-iqbal.github.io/My_Hackathon_Book/
```

**Manual Deployment** (Alternative):
```bash
cd book
npm run build
GIT_USER=KHIZRA-IQBAL npm run deploy
```

**GitHub Pages Setup**:
1. Go to repository Settings → Pages
2. Set Source to "GitHub Actions"
3. The `.github/workflows/deploy.yml` workflow will handle deployment

**Live Demo**: https://khizra-iqbal.github.io/My_Hackathon_Book/ (after first deployment)

## Week 1-2 Content Verification

✅ **All Requirements Met**

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Pages | 6 | 6 | ✅ |
| Word Count | 8,000-12,000 | 9,916 | ✅ |
| Mermaid Diagrams | ≥3 | 3 | ✅ |
| Code Examples | ≥5 | 5 | ✅ |
| Colab Badges | ≥5 | 5 | ✅ |
| Video Embeds | ≥5 | 5 | ✅ |
| Deep Dives | ≥2 | 2 | ✅ |
| MCQ Questions | 5 | 5 | ✅ |
| Short Answer | 3 | 3 | ✅ |
| Practical Exercise | 1 | 1 | ✅ |
| Official Citations | ≥10 | 24 | ✅ |
| Citation % Official | ≥70% | 100% | ✅ |

## Remaining Weeks (3-13)

✅ **Overview summaries created for all weeks:**

- **Week 3-5**: ROS 2 Programming for Physical AI (intro.md - 300 words)
- **Week 6-7**: Simulation with Gazebo (intro.md - 300 words)
- **Week 8-10**: NVIDIA Isaac Sim & Isaac Lab (intro.md - 300 words)
- **Week 11-12**: Full-Stack Humanoid Robot Development (intro.md - 300 words)
- **Week 13**: Conversational AI for Humanoid Robots (intro.md - 350 words)

📝 **Full detailed content coming soon** - Each week will be expanded following the same quality standards as Week 1-2 (6 pages, 8,000-12,000 words, code examples, videos, assessments).

## Spec-Kit Plus Methodology

This project follows Spec-Driven Development (SDD) principles:

1. **Constitution First**: Define project principles in `.specify/memory/constitution.md`
2. **Spec → Plan → Tasks**: Clear progression from requirements to implementation
3. **Prompt History Records (PHRs)**: Every user interaction logged in `history/prompts/`
4. **Architecture Decision Records (ADRs)**: Significant decisions documented in `history/adr/`
5. **Slash Commands**: Standardized workflows via `.claude/commands/`

### Available Slash Commands

- `/sp.specify` - Create/update feature specification
- `/sp.plan` - Generate implementation plan
- `/sp.tasks` - Create actionable task list
- `/sp.implement` - Execute implementation
- `/sp.clarify` - Ask clarification questions
- `/sp.adr` - Create Architecture Decision Record
- `/sp.phr` - Create Prompt History Record
- `/sp.analyze` - Analyze cross-artifact consistency
- `/sp.checklist` - Generate feature checklist
- `/sp.constitution` - Update project constitution
- `/sp.git.commit_pr` - Git workflow automation

## Testing

### Docusaurus Build

```bash
cd book
npm run build
# Should complete without errors
```

### Chatbot Backend

```bash
cd chatbot-backend
pytest
# Run integration tests
```

### Structure Validation

```bash
# Check prerequisites (bash/PowerShell)
bash .specify/scripts/bash/check-prerequisites.sh
# or
powershell .specify/scripts/powershell/check-prerequisites.ps1
```

## Contributing

Follow the Spec-Kit Plus workflow:

1. Create new feature: `.specify/scripts/bash/create-new-feature.sh "Feature description"`
2. Write specification: Edit `specs/<feature>/spec.md`
3. Run `/sp.plan` to create plan
4. Run `/sp.tasks` to generate tasks
5. Implement following tasks
6. Document decisions with `/sp.adr`
7. Create PHR with `/sp.phr`

## License

MIT License - See LICENSE file for details

## Acknowledgments

- **Hackathon PDF**: Physical AI & Humanoid Robotics course requirements
- **Spec-Kit Plus**: Systematic development methodology
- **Docusaurus**: Static site generator by Meta
- **FastAPI**: Modern Python web framework
- **OpenAI**: LLM and embeddings API
- **Qdrant**: Vector database for semantic search
- **Neon**: Serverless PostgreSQL database
