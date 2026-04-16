# Decision Journal - Week 1 Planning

**Date**: 2026-04-15
**Project**: AI Customer Support Automation Platform
**Phase**: Week 1 - Discovery & Research

## Decisions Made

### 1. Project Selection: T2-5 Customer Support Automation
**Decision**: Build T2-5 (AI Customer Support Automation Platform) instead of other T1/T2/T3 options

**Rationale**:
- Clear business value (deflection rate, cost savings)
- Measurable success metrics (deflection rate ≥60%, CSAT ≥4.0)
- B2B positioning with clear ROI
- Extends my existing multi-agent experience
- High PM credibility (deflection rate vs. CSAT tradeoff is a classic PM dilemma)

**Alternatives Considered**:
- T1-1 Email Productivity Agent (too similar to existing MindMail)
- T1-5 Personal Finance Tracker (too similar to existing Financial Coach)
- T2-1 RAG Failure Diagnostics (good, but less business impact)
- T3-1 Health & Fitness (too long, 6-8 weeks)

**Trade-offs**:
- ✅ Pros: Clear metrics, B2B audience, measurable ROI
- ❌ Cons: Need access to support managers for interviews (may be harder to recruit)

**Confidence**: High (8.5/10)

---

### 2. Agent Architecture: 4-Agent Team
**Decision**: Build 4-agent system (Triage, Response, Escalation, Learning)

**Rationale**:
- Clear separation of concerns
- Triage handles classification
- Response handles drafting
- Escalation handles human handoff
- Learning handles improvement over time
- Simpler than 5+ agents, more capable than 2-3 agents

**Alternatives Considered**:
- 3-agent (combine Escalation with Triage) - less clear handoff
- 5-agent (separate Learning from KB updates) - over-complicated for MVP

**Trade-offs**:
- ✅ Pros: Clear roles, easy to debug, scalable
- ❌ Cons: More coordination overhead than 3-agent system

**Confidence**: High (9/10)

---

### 3. Success Metrics: Deflection Rate + CSAT
**Decision**: Primary metric = Deflection Rate (≥60%), Secondary = CSAT (≥4.0)

**Rationale**:
- Deflection rate directly measures business value (cost savings)
- CSAT ensures quality doesn't degrade
- Both are measurable and actionable
- Classic PM tradeoff (deflection vs. quality)

**Alternatives Considered**:
- Resolution time only - doesn't measure automation effectiveness
- Cost per ticket only - doesn't measure quality
- User satisfaction only - too vague

**Trade-offs**:
- ✅ Pros: Clear business value, measurable, actionable
- ❌ Cons: Requires post-resolution surveys for CSAT (may have low response rate)

**Confidence**: High (9/10)

---

### 4. Confidence Threshold: 85%
**Decision**: Auto-respond when confidence >85%, escalate to human when <85%

**Rationale**:
- 85% is a reasonable balance between automation and quality
- High enough to avoid embarrassing AI errors
- Low enough to achieve 60% deflection rate
- Can be iterated based on beta feedback

**Alternatives Considered**:
- 80% threshold - higher deflection but more risk of errors
- 90% threshold - lower risk but harder to achieve 60% deflection

**Trade-offs**:
- ✅ Pros: Clear decision boundary, easy to communicate
- ❌ Cons: May need to adjust based on beta data

**Confidence**: Medium (7/10) - will validate with beta

---

### 5. Tech Stack: Streamlit + LangChain
**Decision**: Use Streamlit for frontend, LangChain for agent orchestration

**Rationale**:
- Streamlit: Fast to build, good for demos, Python-based
- LangChain: Mature agent framework, good documentation
- Both align with my existing skills
- Easy to deploy to Streamlit Cloud

**Alternatives Considered**:
- FastAPI + HTML/JS - more control but slower to build
- Gradio - good for demos but less flexible than Streamlit
- LangGraph - more powerful but steeper learning curve

**Trade-offs**:
- ✅ Pros: Fast development, good for demos, easy deployment
- ❌ Cons: Streamlit not ideal for production, LangChain may have limitations

**Confidence**: High (8.5/10)

---

### 6. Beta Recruitment: 5 Support Teams
**Decision**: Recruit 5 support teams for beta testing

**Rationale**:
- 5 is the minimum for meaningful qualitative insights
- 5 is manageable for 2 weeks of testing
- 5 provides enough data for deflection rate statistics
- Can recruit from LinkedIn/network

**Alternatives Considered**:
- 10 teams - too many for 2 weeks of testing
- 3 teams - not enough for meaningful insights

**Trade-offs**:
- ✅ Pros: Manageable, meaningful insights, good statistics
- ❌ Cons: May be hard to recruit 5 support managers quickly

**Confidence**: Medium (7/10) - depends on network

---

### 7. LinkedIn Content Strategy: Weekly Posts
**Decision**: Publish 2 LinkedIn posts per week (total 12 posts over 6 weeks)

**Rationale**:
- 2 posts/week maintains momentum without burnout
- Weekly cadence allows time for meaningful progress
- 12 posts provides enough content for algorithm visibility
- Aligns with 6-week timeline

**Alternatives Considered**:
- Daily posts - too frequent, may lead to burnout
- Weekly posts - less visibility, slower growth
- Bi-weekly posts - too infrequent for algorithm

**Trade-offs**:
- ✅ Pros: Consistent momentum, manageable workload
- ❌ Cons: Requires discipline to maintain cadence

**Confidence**: High (9/10)

---

## Pivoted Approach: Research-Driven Instead of Interviews

**Decision**: Skip user interviews, use industry research instead

**Rationale**:
- Comprehensive industry benchmarks available (Salesforce, Zendesk, McKinsey)
- 79% of service leaders say AI is essential - clear market validation
- 30% current AI deflection vs 60% target - clear opportunity gap
- Can validate assumptions through beta testing instead

**What Changed**:
- ❌ No longer recruiting 10 user interviews
- ✅ Created comprehensive research document (interview-research.md)
- ✅ Industry benchmarks validate all key assumptions
- ✅ Will validate with beta users in Week 4 instead

## Next Decisions (Week 2)
1. Final agent architecture (detailed role definitions)
2. MVP scope (must-have vs. nice-to-have features)
3. KB implementation approach (manual vs. automated)
4. Integration approach (CSV import vs. API integrations)

---

**Last Updated**: 2026-04-15
**Next Review**: 2026-04-22 (Week 2 planning)
