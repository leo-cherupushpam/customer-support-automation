# Week 2: Architecture & Planning

**Goal**: Design the 4-agent team and define MVP scope

**Timeline**: April 22-28, 2026

---

## Week 2 Objectives

1. **Design 4-agent architecture** (Triage, Response, Escalation, Learning)
2. **Define agent roles and handoffs**
3. **Create decision journal** (why 4 agents, why these roles)
4. **Define MVP scope** (must-have vs. nice-to-have)
5. **Publish LinkedIn posts** about architecture decisions

---

## 4-Agent Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│              Customer Support Platform                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Triage     │───▶│   Response   │───▶│  Escalation  │  │
│  │   Agent      │    │   Agent      │    │   Agent      │  │
│  │              │    │              │    │              │  │
│  │ - Classify   │    │ - Draft      │    │ - Human      │  │
│  │ - Confidence │    │   responses  │    │   handoff    │  │
│  │ - Route      │    │ - KB lookup  │    │ - Priority   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                     │                     │       │
│         └─────────────────────┼─────────────────────┘       │
│                               │                             │
│                      ┌────────▼────────┐                    │
│                      │    Learning     │                    │
│                      │    Agent        │                    │
│                      │                 │                    │
│                      │ - KB updates    │                    │
│                      │ - Pattern       │                    │
│                      │   detection     │                    │
│                      └─────────────────┘                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent 1: Triage Agent

**Purpose**: Classify incoming tickets and assign confidence score

**Input**: Customer ticket text (email/chat/ticket system)

**Output**: 
- Category (e.g., "Password Reset", "Billing Inquiry", "Feature Request")
- Confidence score (0-100%)
- Routing decision (auto-respond vs. escalate)

**Decision Logic**:
```
if confidence > 85%:
    → Route to Response Agent (auto-respond)
else:
    → Route to Escalation Agent (human handoff)
```

**Key Features**:
- Multi-label classification (ticket can belong to multiple categories)
- Confidence calibration (ensure 85% threshold is meaningful)
- Category taxonomy (10-15 tier-1 categories)

**AI Approach**:
- Use GPT-4o-mini for classification
- Few-shot prompting with example tickets
- Confidence scoring based on token probability

**Success Metrics**:
- Classification accuracy ≥90%
- Confidence calibration (85% confident = 85% accurate)
- Latency <1 second

---

## Agent 2: Response Agent

**Purpose**: Generate AI draft responses with knowledge base citations

**Input**: 
- Ticket text
- Category (from Triage Agent)
- Confidence score
- Customer context (if available)

**Output**:
- AI draft response
- KB citations (sources used)
- Response quality score

**Decision Logic**:
```
query KB by category + keywords
retrieve top-3 relevant articles
generate response with citations
score response quality
if quality < 80%:
    → Flag for human review
else:
    → Ready to send (or human approve)
```

**Key Features**:
- Knowledge base lookup (semantic search)
- Response generation with citations
- Quality scoring (hallucination detection)
- Human approval workflow

**AI Approach**:
- RAG (Retrieval Augmented Generation)
- GPT-4o-mini for response generation
- Embedding-based KB search (e.g., OpenAI embeddings)

**Success Metrics**:
- Response quality ≥4.0/5 (human review)
- Citation accuracy ≥95%
- Hallucination rate <5%

---

## Agent 3: Escalation Agent

**Purpose**: Route low-confidence tickets to human support with context

**Input**: 
- Low-confidence ticket (<85%)
- Ticket text
- Category (from Triage Agent)

**Output**:
- Human ticket with full context
- Suggested response draft
- Priority score
- Customer history summary

**Decision Logic**:
```
if confidence < 85%:
    → Generate human ticket
    → Create context summary
    → Draft suggested response
    → Assign priority (based on urgency + customer tier)
    → Route to human queue
```

**Key Features**:
- Context summary (key points, customer history)
- Suggested response draft (for human to edit)
- Priority scoring (urgency + customer tier + sentiment)
- Human-in-the-loop approval

**AI Approach**:
- Summarization (GPT-4o-mini)
- Sentiment analysis
- Priority scoring model

**Success Metrics**:
- Human satisfaction with suggested response ≥4.0/5
- Escalation handling time <2 minutes
- Context completeness ≥90%

---

## Agent 4: Learning Agent

**Purpose**: Learn from resolved tickets to improve KB and models

**Input**: 
- Resolved tickets (auto-responded + human-resolved)
- Human responses (for auto-responded tickets)
- Customer feedback (CSAT scores)

**Output**:
- KB updates (new Q&A pairs)
- Pattern detection (emerging issues)
- Model improvements (retraining data)

**Decision Logic**:
```
daily batch process:
    analyze resolved tickets
    identify new questions/patterns
    suggest KB updates
    flag model retraining candidates
    notify admin of changes
```

**Key Features**:
- Daily batch processing
- New question detection
- KB auto-update suggestions
- Pattern detection (trending issues)

**AI Approach**:
- Clustering (identify similar tickets)
- Anomaly detection (new patterns)
- Summarization (extract insights)

**Success Metrics**:
- KB update acceptance rate ≥70%
- Pattern detection accuracy ≥85%
- Time to detect trending issues <24 hours

---

## Agent Handoffs & Workflow

### Happy Path (Auto-Respond)
```
Customer Ticket → Triage Agent (confidence 92%) → Response Agent → 
Generate Response → Send to Customer → Learning Agent (learn from resolution)
```

### Escalation Path (Human Handoff)
```
Customer Ticket → Triage Agent (confidence 72%) → Escalation Agent → 
Create Human Ticket → Human Reviews → Human Sends Response → 
Learning Agent (learn from human response)
```

### Quality Control Path (Human Review)
```
Customer Ticket → Triage Agent (confidence 88%) → Response Agent → 
Generate Response → Quality Score 75% (<80%) → Human Review → 
Human Approves/Edits → Send to Customer → Learning Agent
```

---

## MVP Scope Definition

### Must-Have Features (Week 3-4)

**Triage Agent**:
- [ ] Ticket classification (10 predefined categories)
- [ ] Confidence scoring (0-100%)
- [ ] 85% threshold decision logic
- [ ] API endpoint for ticket ingestion

**Response Agent**:
- [ ] Knowledge base lookup (semantic search)
- [ ] Response generation with citations
- [ ] Quality scoring (basic)
- [ ] CSV import for KB articles

**Escalation Agent**:
- [ ] Human ticket creation (simple format)
- [ ] Context summary generation
- [ ] Suggested response draft
- [ ] Priority scoring (basic)

**Learning Agent**:
- [ ] Daily batch processing
- [ ] Resolved ticket analysis
- [ ] KB update suggestions
- [ ] Simple admin dashboard

**Frontend**:
- [ ] Streamlit dashboard for demo
- [ ] Ticket ingestion interface
- [ ] Agent performance metrics
- [ ] KB management interface

### Nice-to-Have Features (Post-MVP)

- [ ] Zendesk/Intercom API integrations
- [ ] Real-time CSAT survey integration
- [ ] Advanced priority scoring (customer tier + history)
- [ ] Multi-language support
- [ ] Custom category training
- [ ] Advanced analytics dashboard
- [ ] Slack notifications for escalations
- [ ] A/B testing for response templates

### Out of Scope (MVP)

- [ ] Mobile app
- [ ] Voice ticket processing
- [ ] Custom ML model training (use GPT-4o-mini)
- [ ] Enterprise SSO
- [ ] Advanced security compliance (SOC 2)
- [ ] Multi-tenant support

---

## Technical Stack

### Core Frameworks
- **Agent Orchestration**: LangChain or LangGraph (LangGraph recommended for stateful workflows)
- **LLM**: OpenAI GPT-4o-mini (cost-effective, good quality)
- **Embeddings**: OpenAI text-embedding-ada-002

### Frontend
- **Framework**: Streamlit (fastest to build, good for demos)
- **Styling**: Custom CSS for better UX

### Backend
- **Language**: Python 3.12+
- **Database**: SQLite (MVP), PostgreSQL (production)
- **API**: FastAPI (for ticket ingestion)

### Infrastructure
- **Hosting**: Streamlit Cloud (demo), AWS/GCP (production)
- **Version Control**: Git + GitHub
- **Monitoring**: LangSmith (for agent tracing)

---

## Week 2 Deliverables

### Documentation
- [ ] Agent architecture diagram (detailed)
- [ ] Agent role definitions (this document)
- [ ] Decision journal (Week 2 decisions)
- [ ] MVP scope document (this document)
- [ ] Technical architecture doc

### Code
- [ ] Project structure setup
- [ ] Agent base classes (Triage, Response, Escalation, Learning)
- [ ] Basic Streamlit UI skeleton
- [ ] Knowledge base CSV import function

### LinkedIn Content
- [ ] Post 1: "Designing a 4-agent team for customer support"
- [ ] Post 2: "The PM dilemma: deflection rate vs. CSAT"

---

## Decision Journal (Week 2)

### Decision 1: Why 4 Agents?

**Decision**: Build 4-agent system instead of 3 or 5

**Rationale**:
- 3 agents (combine Escalation with Triage) → unclear handoff boundaries
- 5 agents (separate Learning from KB updates) → over-complicated for MVP
- 4 agents provides clear separation: classify → respond → escalate → learn

**Alternatives Considered**:
- 3-agent: Triage, Response/Escalation, Learning
- 5-agent: Triage, Response, Escalation, KB Manager, Learning

**Trade-offs**:
- ✅ Pros: Clear roles, easy to debug, scalable
- ❌ Cons: More coordination overhead than 3-agent

**Confidence**: High (9/10)

---

### Decision 2: Confidence Threshold = 85%

**Decision**: Auto-respond when confidence >85%, escalate when <85%

**Rationale**:
- 85% balances automation (60% deflection goal) with quality (CSAT ≥4.0)
- Industry insight: 75% of consumers favor AI drafting responses
- Can iterate based on beta data

**Alternatives Considered**:
- 80% threshold → higher deflection but more risk of errors
- 90% threshold → lower risk but harder to achieve 60% deflection

**Trade-offs**:
- ✅ Pros: Clear decision boundary, achievable target
- ❌ Cons: May need adjustment based on beta feedback

**Confidence**: Medium (7/10) - will validate with beta

---

### Decision 3: Use LangGraph for Orchestration

**Decision**: Use LangGraph instead of LangChain for agent orchestration

**Rationale**:
- LangGraph provides stateful, multi-agent workflows
- Better for complex handoffs between agents
- Growing adoption in production systems

**Alternatives Considered**:
- LangChain: Simpler but less flexible for multi-agent
- Custom orchestration: More control but slower to build

**Trade-offs**:
- ✅ Pros: Built-in state management, graph-based workflows
- ❌ Cons: Steeper learning curve than LangChain

**Confidence**: High (8.5/10)

---

### Decision 4: Streamlit for Frontend

**Decision**: Use Streamlit instead of FastAPI + React

**Rationale**:
- Fastest to build (MVP timeline is tight)
- Good enough for demo and beta testing
- Can migrate to custom frontend later

**Alternatives Considered**:
- FastAPI + React: More control but 2-3x development time
- Gradio: Good for demos but less flexible than Streamlit

**Trade-offs**:
- ✅ Pros: Fast development, Python-only, easy deployment
- ❌ Cons: Not ideal for production, limited customization

**Confidence**: High (9/10)

---

### Decision 5: GPT-4o-mini for All Agents

**Decision**: Use GPT-4o-mini for all agent LLM calls

**Rationale**:
- Cost-effective ($0.15/M input tokens, $0.60/M output tokens)
- Good quality for classification, generation, summarization
- Simplifies architecture (one model to manage)

**Alternatives Considered**:
- GPT-4o: Better quality but 10x more expensive
- Mix of models (small for classification, large for response): More complex

**Trade-offs**:
- ✅ Pros: Cost-effective, simple, good quality
- ❌ Cons: May have limitations on complex reasoning

**Confidence**: High (8.5/10)

---

## Next Steps (Week 3)

1. **Implement Triage Agent** (classification + confidence scoring)
2. **Implement Response Agent** (RAG + response generation)
3. **Implement Escalation Agent** (human handoff workflow)
4. **Implement Learning Agent** (batch processing + KB updates)
5. **Build Streamlit UI** (ticket ingestion + metrics dashboard)
6. **Recruit 5 beta users** (support teams)

---

**Last Updated**: 2026-04-22
**Next Review**: 2026-04-29 (Week 3 implementation review)
