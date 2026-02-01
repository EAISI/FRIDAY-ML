# FRIDAY-ML Consolidation Plan

**Date**: 2026-02-01
**Status**: Awaiting Approval
**Impact**: Medium - Documentation updates, no code changes

## Executive Summary

The project has significant inconsistencies between documentation and actual structure, plus ~90% duplication between `.claude/CLAUDE.md` and `.vibe`. This plan consolidates configuration, fixes path references, and reorganizes reference materials.

## Critical Issues Found

### 1. Path Inconsistencies (HIGH PRIORITY)

**Problem**: Documentation references non-existent directories and files

**Current State**:
```
Actual structure:          Referenced in docs:
├── notebooks/            ├── deep-learning/     ❌ (doesn't exist)
│   ├── mnist.py         │   ├── mnist.py
│   └── ames-housing.py  │   ├── mnist/
└── data/                │   └── mnist.png
                          └── autogluon/         ❌ (doesn't exist)
                              └── ames-housing.ipynb ❌ (doesn't exist)
```

**Affected Files**:
- `.claude/CLAUDE.md` (lines 34, 56-60, 73)
- `.vibe` (lines 153, 195-196, 201)
- `justfile` (line 5)
- `README.md` (references deep-learning/mnist.py)

**Impact**: AI agents will fail to find notebooks, justfile commands won't work

---

### 2. Configuration Duplication (HIGH PRIORITY)

**Problem**: `.claude/CLAUDE.md` and `.vibe` contain ~90% identical content

**Duplication Analysis**:
| Section | .claude/CLAUDE.md | .vibe | Duplication |
|---------|------------------|-------|-------------|
| Project Overview | Lines 5-9 | Lines 6-10 | 100% |
| Tech Stack | Lines 12-19 | Lines 141-147 | 95% |
| Development Commands | Lines 21-42 | Lines 149-154 | 90% |
| Guidelines | Lines 85-93 | Lines 157-189 | 80% |
| Architecture | Lines 50-83 | Lines 192-207 | 75% |

**Total Duplicated Content**: ~180 lines / 200 total lines = **90% duplication**

**Impact**: Maintenance burden, inconsistencies between files, confusion about source of truth

---

### 3. Misorganized Reference Materials (MEDIUM PRIORITY)

**Problem**: 19 Polars reference notebooks (8,514 lines) are in `.claude/rules/` but they're not "rules"

**Current Location**: `.claude/rules/polars/` (ch01.py through ch18.py, appendix1.py)
**Purpose**: Educational reference documentation for Polars library
**Issue**: `rules/` should contain guidelines/standards, not reference material

**Impact**: Organizational confusion, `.claude/rules/` mixes rules with examples

---

### 4. Insufficient .gitignore (MEDIUM PRIORITY)

**Current .gitignore** (only 2 lines):
```gitignore
.venv/
/logs
```

**Missing Critical Entries**:
- `.env` ⚠️ **SECURITY RISK** - Secrets could be committed
- `__pycache__/` - Python bytecode cache
- `*.pyc` - Compiled Python files
- `.DS_Store` - macOS metadata
- `*.egg-info/` - Python package metadata
- `.pytest_cache/` - Test cache
- `.ruff_cache/` - Linter cache

**Impact**: Security risk, repository pollution with build artifacts

---

### 5. Version Inconsistencies (LOW PRIORITY)

**Problem**: Different Python version requirements across files

- `pyproject.toml`: Requires Python 3.11+
- `.claude/skills/friday/SKILL.md`: Says 3.12+
- `.claude/CLAUDE.md`: Correctly says 3.11+

**Impact**: Confusion about actual requirements, potential runtime errors

---

## Proposed Solutions

### Phase 1: Fix Critical Path Issues (15 min)

**1.1 Update .claude/CLAUDE.md**
- [ ] Line 34: `deep-learning/mnist.py` → `notebooks/mnist.py`
- [ ] Line 41: `just mnist` → `just mnist` (keep, will fix justfile)
- [ ] Lines 54-63: Replace directory layout with actual structure
- [ ] Line 73: `deep-learning/mnist.py` → `notebooks/mnist.py`

**1.2 Update .vibe**
- [ ] Line 153: `deep-learning/mnist.py` → `notebooks/mnist.py`
- [ ] Lines 195-196: Update project_structure.directories (remove autogluon, deep_learning)
- [ ] Line 201: `deep-learning/mnist.py` → `notebooks/mnist.py`
- [ ] Line 202: Keep `notebooks/ames-housing.py` (already correct)

**1.3 Update justfile**
- [ ] Line 5: `mnist.py` → `notebooks/mnist.py`
- [ ] Add: `ames-housing: uv run marimo edit notebooks/ames-housing.py`

**1.4 Update README.md**
- [ ] Search for `deep-learning/mnist.py` and replace with `notebooks/mnist.py`

**Expected Outcome**: All documentation matches actual project structure

---

### Phase 2: Consolidate Configuration Files (20 min)

**Approach**: Keep both files but clarify their roles and eliminate duplication

**2.1 Restructure .claude/CLAUDE.md**
Make it a concise **AI agent reference card** (target: 80 lines):
- Project overview (5 lines)
- Tech stack (5 lines)
- Quick commands (10 lines)
- Key patterns only (30 lines)
- Reference to detailed rules in `.claude/rules/`

**2.2 Restructure .vibe**
Keep as **Vibe-specific configuration** with:
- YAML metadata and settings (keep as-is)
- Workflow templates (unique to Vibe)
- Reference to `.claude/CLAUDE.md` for main guidance
- FRIDAY skill integration (unique to Vibe)

**2.3 Create .claude/rules/GUIDELINES.md**
New comprehensive file for detailed guidance (consolidates duplicated content):
- Architecture patterns
- Development principles
- Common patterns
- Educational approach
- All the detailed guidelines currently duplicated

**File Structure After Consolidation**:
```
.claude/
├── CLAUDE.md                    # 80 lines - Quick reference for AI agents
├── rules/
│   ├── GUIDELINES.md            # 150 lines - Detailed AI agent guidelines (NEW)
│   ├── code-style.md            # Existing - Python code quality
│   ├── marimo.md                # Existing - Marimo patterns
│   └── security.md              # Existing - Security rules
.vibe                             # Vibe-specific config, references CLAUDE.md
```

**Expected Outcome**:
- Single source of truth for shared content
- Clear separation of concerns
- Reduced duplication from 90% to <10%

---

### Phase 3: Reorganize Reference Materials (10 min)

**3.1 Create references/ directory**
```bash
mkdir -p references/polars
```

**3.2 Move Polars notebooks**
```bash
mv .claude/rules/polars/*.py references/polars/
```

**3.3 Update references in documentation**
- `.claude/rules/code-style.md`: Update all polars/ links to `references/polars/`
- Create `references/README.md` explaining the reference materials

**3.4 Update .vibe file patterns**
- Add `references/**` to include patterns

**New Structure**:
```
FRIDAY-ML/
├── .claude/
│   └── rules/          # Only actual rules/guidelines
├── references/          # Educational reference materials (NEW)
│   └── polars/         # 19 Polars example notebooks
└── notebooks/          # Working notebooks
```

**Expected Outcome**: Clear separation between rules and reference documentation

---

### Phase 4: Improve .gitignore (5 min)

**4.1 Add Standard Python Ignores**
```gitignore
# Virtual Environment
.venv/
venv/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project Specific
/logs/
*.log

# Security - CRITICAL
.env
.env.local
*.pem
*.key

# Caches
.pytest_cache/
.ruff_cache/
.mypy_cache/

# Notebooks
.ipynb_checkpoints/
```

**Expected Outcome**: Proper protection against committing secrets and build artifacts

---

### Phase 5: Fix Version Inconsistencies (2 min)

**5.1 Update .claude/skills/friday/SKILL.md**
- Change Python requirement from 3.12+ to 3.11+
- Align with pyproject.toml

**Expected Outcome**: Consistent Python version requirements across all files

---

## Implementation Order

**Recommended sequence** (total time: ~50 minutes):

1. **Phase 1** (15 min) - Fix paths - IMMEDIATE IMPACT
2. **Phase 4** (5 min) - Update .gitignore - SECURITY
3. **Phase 5** (2 min) - Fix version inconsistencies - QUICK WIN
4. **Phase 3** (10 min) - Reorganize references - ORGANIZATIONAL
5. **Phase 2** (20 min) - Consolidate configs - MAINTENANCE

## Rollback Plan

All changes are documentation/configuration only:
- Keep original files as `.bak` during updates
- Git commit after each phase
- Can revert individual commits if needed

## Risks

**Low Risk**: No code changes, only documentation and configuration
**Testing**: Verify justfile commands work after Phase 1
**Validation**: Run `uv run marimo check` on moved notebooks after Phase 3

## Success Criteria

- [ ] All file paths in documentation match actual structure
- [ ] `just mnist` and `just tensorboard` commands work
- [ ] .gitignore includes `.env` and standard Python ignores
- [ ] Configuration duplication reduced from 90% to <10%
- [ ] Polars reference materials separated from rules
- [ ] Python version consistent across all files
- [ ] All marimo notebooks still load correctly

## Decision Required

**Please approve or modify this plan before proceeding with implementation.**

Options:
1. **Approve all phases** - Full consolidation (~50 min)
2. **Approve Phase 1 + 4 only** - Critical fixes only (~20 min)
3. **Modify plan** - Suggest changes
4. **Reject** - Keep current state
