# ⚡ QUICK REFERENCE - Essential Commands & Guides

Quick access to all essential commands and instructions for finalizing and pushing your project.

---

## 🚀 30-SECOND QUICK START

```bash
# 1. Navigate to project
cd "c:\Users\rahul\Desktop\4th project"

# 2. Initialize git
git init

# 3. Configure git (do this once)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 4. Check what will be committed
git status

# 5. Add all files
git add .

# 6. Commit
git commit -m "feat: Initial production-ready release"

# 7. Copy this from GitHub after creating the repo:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## 📋 VERIFICATION COMMANDS

```bash
# ✅ Check git status
git status

# ✅ Verify folder structure
ls -la

# ✅ Verify .env is NOT included
git status | findstr ".env"
# Should show: nothing or .env.example only

# ✅ Verify __pycache__ is ignored
git status | findstr "__pycache__"
# Should show: nothing

# ✅ Test the application
python test_pipeline.py

# ✅ Start the API
uvicorn backend.main:app --reload --port 8000

# ✅ Check API is working
# Visit: http://localhost:8000/api/health
# or: curl http://localhost:8000/api/health

# ✅ Run tests
pytest tests/ -v

# ✅ View recent commits
git log --oneline -5
```

---

## 🔐 SECURITY COMMANDS

```bash
# ✅ Search for API keys (should find NONE)
grep -r "api_key\|sk_\|password=" . --include="*.py"

# ✅ Verify secrets not in git history
git log -p | grep -i "api_key\|password\|secret"

# ✅ Check .env file (should NOT exist)
ls -la .env
# Should show: "cannot find the path specified"

# ✅ Check .env.example (should exist with dummy values)
cat .env.example | head -20
```

---

## 🌐 GITHUB WORKFLOW

### Step 1: Create GitHub Repo
1. Go to: https://github.com/new
2. Name: `Real-Time-Automated-Micro-Influencer-Discovery-Contextual-Outreach-System`
3. Visibility: **Public**
4. ❌ Do NOT initialize with README
5. Click: **Create repository**

### Step 2: Copy Commands
GitHub shows:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 3: Execute Commands

```bash
# Navigate to project
cd "c:\Users\rahul\Desktop\4th project"

# Initialize (only if not done)
git init

# Add files
git add .

# Commit
git commit -m "feat: Initial production-ready release"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Verify Push
1. Visit: `https://github.com/YOUR_USERNAME/YOUR_REPO`
2. Should see:
   - ✅ All folders (backend/, config/, tests/, ui/)
   - ✅ All files (README.md, requirements.txt, etc.)
   - ✅ README displayed
   - ✅ "main" branch selected

---

## 🐛 TROUBLESHOOTING COMMANDS

### Issue: "origin already exists"
```bash
git remote rm origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Issue: Authentication failed
```bash
# Use GitHub Personal Access Token, not password
# Get it from: https://github.com/settings/tokens

# When prompted:
# Username: YOUR_USERNAME
# Password: YOUR_PERSONAL_ACCESS_TOKEN
```

### Issue: Need to remove .env from git
```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

### Issue: File already committed accidentally
```bash
# Remove from git history
git rm --cached FILENAME
git commit -m "Remove FILENAME from tracking"
git add .gitignore
git commit -m "Update gitignore"
git push
```

---

## 📁 PROJECT STRUCTURE

```
✅ COMPLETE STRUCTURE:
c:\Users\rahul\Desktop\4th project\
├── .env.example              ✅ Configuration template
├── .gitignore                ✅ Git ignore rules
├── README.md                 ✅ Complete documentation (1000+ lines)
├── requirements.txt          ✅ Dependencies
├── requirements-dev.txt      ✅ Dev dependencies
├── pytest.ini                ✅ Test configuration
│
├── ARCHITECTURE.md           ✅ Technical docs (800+ lines)
├── DEPLOYMENT.md             ✅ Deployment guide (600+ lines)
├── UPGRADE_SUMMARY.md        ✅ Changes made (500+ lines)
├── GITHUB_SETUP.md           ✅ GitHub guide (400+ lines)
├── PRODUCTION_CHECKLIST.md   ✅ Final checklist
│
├── backend/
│   ├── main.py              ✅ FastAPI entry point
│   ├── __init__.py
│   ├── api/
│   │   ├── routes.py
│   │   └── __init__.py
│   ├── middleware/          ✅ NEW: Error handling
│   │   ├── error_handler.py
│   │   └── __init__.py
│   ├── utils/               ✅ NEW: Shared utilities
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   ├── helpers.py
│   │   └── __init__.py
│   ├── discovery/
│   ├── filtering/
│   ├── enrichment/
│   ├── nlp/
│   ├── outreach/
│   ├── scoring/
│   ├── segmentation/
│   ├── automation/
│   └── __init__.py
│
├── config/
│   ├── settings.py          ✅ Configuration + validation
│   └── __init__.py
│
├── tests/                    ✅ NEW: Test examples
│   ├── test_scoring.py
│   └── __init__.py
│
├── ui/
│   └── streamlit_app.py
│
└── test_pipeline.py         ✅ Manual testing script
```

---

## 📊 FILES CREATED/UPDATED

### New Files (7)
1. ✅ `backend/utils/logger.py`
2. ✅ `backend/utils/exceptions.py`
3. ✅ `backend/utils/helpers.py`
4. ✅ `backend/middleware/error_handler.py`
5. ✅ `tests/test_scoring.py`
6. ✅ `pytest.ini`
7. ✅ `requirements-dev.txt`

### Updated Files (4)
1. ✅ `backend/main.py` (integrated logging & error handlers)
2. ✅ `config/settings.py` (added validation)
3. ✅ `README.md` (expanded to 1000+ lines)
4. ✅ `.gitignore` (complete configuration)

### Documentation Files (4)
1. ✅ `.env.example`
2. ✅ `ARCHITECTURE.md`
3. ✅ `DEPLOYMENT.md`
4. ✅ `UPGRADE_SUMMARY.md`
5. ✅ `GITHUB_SETUP.md`
6. ✅ `PRODUCTION_CHECKLIST.md`

---

## 💻 COMMON COMMANDS

### Git Commands
```bash
git init                                    # Initialize repo
git config user.name "Name"                 # Configure name
git config user.email "email@example.com"   # Configure email
git add .                                   # Stage all files
git status                                  # Check status
git commit -m "message"                     # Commit changes
git remote add origin URL                   # Add remote
git branch -M main                          # Rename to main
git push -u origin main                     # Push to GitHub
git log --oneline                           # View commits
git remote -v                               # View remotes
```

### Python Commands
```bash
pip install -r requirements.txt             # Install dependencies
pip install -r requirements-dev.txt         # Install dev dependencies
python test_pipeline.py                     # Run manual tests
pytest tests/ -v                            # Run automated tests
pytest tests/ --cov=backend                 # Generate coverage
uvicorn backend.main:app --reload           # Start development server
uvicorn backend.main:app --port 8000        # Start on specific port
```

### PowerShell (Windows-specific)
```bash
cd "c:\Users\rahul\Desktop\4th project"     # Navigate to project
ls                                          # List files
ls -la                                      # List all files (verbose)
cat .env.example                            # View file contents
Get-ChildItem                               # List directory contents
Remove-Item .env                            # Delete file
```

---

## 📚 DOCUMENTATION QUICK LINKS

### Internal Docs
- **README.md** — Getting started, setup, features, API docs
- **ARCHITECTURE.md** — System design, layers, patterns, data flow
- **DEPLOYMENT.md** — Docker, cloud platforms, monitoring, security
- **UPGRADE_SUMMARY.md** — What changed, before/after comparisons
- **GITHUB_SETUP.md** — Step-by-step GitHub push instructions
- **PRODUCTION_CHECKLIST.md** — Final verification checklist

### External Docs
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Pytest Documentation](https://docs.pytest.org)
- [Docker Documentation](https://docs.docker.com)
- [GitHub Help](https://docs.github.com)

---

## 🎯 FINAL CHECKLIST (Quick Version)

```
✅ BEFORE GIT:
- [ ] Code runs without errors (python test_pipeline.py)
- [ ] No .env file exists
- [ ] __pycache__ and .venv not included
- [ ] All documentation files present

✅ BEFORE GITHUB:
- [ ] Git initialized
- [ ] Files staged (git add .)
- [ ] Committed (git commit -m "...")
- [ ] Remote added (git remote add origin ...)
- [ ] Branch renamed to main
- [ ] Ready to push

✅ AFTER PUSH:
- [ ] GitHub repo created
- [ ] All files visible on GitHub
- [ ] README displayed correctly
- [ ] No secrets exposed
- [ ] Clean commit history
- [ ] Main branch active
```

---

## 🚀 STEP-BY-STEP EXECUTION (Copy & Paste)

### Copy this and run in PowerShell:

```powershell
# Navigate to project
cd "c:\Users\rahul\Desktop\4th project"

# Verify structure
Write-Host "Checking project structure..."
ls

# Verify .env not included
Write-Host "Checking for .env..."
if (Test-Path ".env") {
    Write-Host "ERROR: .env file exists! This should not be committed."
    Write-Host "Delete it with: Remove-Item .env"
} else {
    Write-Host "✓ .env not present (good!)"
}

# Initialize git
git init

# Configure git (do this once)
Write-Host "Configuring git..."
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Check status
Write-Host "Checking git status..."
git status

# Add files
Write-Host "Adding files..."
git add .

# Commit
Write-Host "Committing..."
git commit -m "feat: Initial production-ready release"

# Verify commit
Write-Host "Verifying commit..."
git log --oneline -1

Write-Host ""
Write-Host "✓ Ready for GitHub!"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Create repo on GitHub: https://github.com/new"
Write-Host "2. Copy commands from GitHub and run them:"
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main"
```

---

## 📞 WHEN YOU GET STUCK

1. **Check the docs first:**
   - `README.md` — General questions
   - `GITHUB_SETUP.md` — Git/GitHub issues
   - `PRODUCTION_CHECKLIST.md` — Verification issues

2. **Common error solutions:**
   - Authentication: Use Personal Access Token, not password
   - "origin already exists": Remove it first with `git remote rm origin`
   - ".env committed": Use `git rm --cached .env`

3. **Test it works:**
   - `python test_pipeline.py` — Manual test
   - `pytest tests/ -v` — Automated tests
   - `uvicorn backend.main:app --reload` — API test

---

## ✨ SUCCESS INDICATORS

You'll know you're done when:

✅ Git initialized and committed  
✅ Remote added to GitHub  
✅ Code pushed successfully  
✅ No errors in terminal  
✅ GitHub repo shows all files  
✅ README displays correctly  
✅ No .env or secrets visible  
✅ All folders present  
✅ Ready to share with recruiters  

---

## 🏆 YOU'RE READY!

Your project is:
- ✅ Production-ready
- ✅ Recruiter-ready
- ✅ Interview-ready
- ✅ GitHub-ready
- ✅ Deployment-ready

**Next step:** Push to GitHub using the commands above! 🚀
