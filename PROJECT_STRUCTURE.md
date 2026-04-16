# Customer Support Automation - Project Structure

```
customer-support-automation/
├── README.md                          # Project overview
├── PRD.md                             # Product requirements document
├── decisions/
│   ├── 2026-04-15-week1-planning.md  # Week 1 decisions
│   └── week-2-architecture.md         # Week 2 architecture decisions
├── interviews/
│   ├── interview-guide.md             # Interview questions
│   ├── scheduling-template.md         # Booking tracker
│   ├── day-2-execution.md             # Day 2 guide
│   ├── interview-notes/               # Interview notes (if conducted)
│   └── linkedin-posts-week2.md        # Week 2 LinkedIn posts
├── knowledge/
│   ├── index.md                       # Knowledge base index
│   └── interview-research.md          # Industry benchmarks
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── triage_agent.py            # Triage Agent (classification)
│   │   ├── response_agent.py          # Response Agent (RAG)
│   │   ├── escalation_agent.py        # Escalation Agent (handoff)
│   │   └── learning_agent.py          # Learning Agent (KB updates)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuration settings
│   │   ├── llm_client.py              # LLM client (OpenAI)
│   │   └── embeddings.py              # Embedding client
│   └── knowledge_base/
│       ├── __init__.py
│       ├── kb_manager.py              # KB management
│       └── sample_kb.csv              # Sample knowledge base
├── app.py                             # Streamlit main app
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
└── tests/
    ├── __init__.py
    ├── test_triage_agent.py
    ├── test_response_agent.py
    └── test_escalation_agent.py
```

## Key Files

### Core Application
- `app.py` - Main Streamlit application (ticket ingestion, metrics dashboard)
- `src/agents/` - Agent implementations (4 agents)
- `src/utils/` - Utility functions (LLM client, config)
- `src/knowledge_base/` - KB management and sample data

### Documentation
- `README.md` - Project overview and quick start
- `PRD.md` - Detailed product requirements
- `decisions/` - Decision journal (all product/tech decisions)
- `knowledge/` - Research and benchmarks

### Testing
- `tests/` - Unit tests for all agents

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key

# Run the app
streamlit run app.py
```

## Agent Implementations

### Triage Agent (`src/agents/triage_agent.py`)
- Classifies tickets into categories
- Assigns confidence score (0-100%)
- Routes to Response or Escalation Agent

### Response Agent (`src/agents/response_agent.py`)
- RAG-based response generation
- Knowledge base lookup
- Citation tracking

### Escalation Agent (`src/agents/escalation_agent.py`)
- Human handoff for low-confidence tickets
- Context summary generation
- Priority scoring

### Learning Agent (`src/agents/learning_agent.py`)
- Daily batch processing
- KB update suggestions
- Pattern detection

## Next Steps

Week 3: Implement all 4 agents and build Streamlit UI
