# Week 2 LinkedIn Posts

## Post 1: Designing a 4-Agent Team for Customer Support

**Title**: Designing a 4-agent team for customer support - here's my architecture

**Post**:
```
Week 2 of my Build-in-Public journey: Designing the agent architecture for AI Customer Support Automation.

After researching 92 customer service statistics, I'm building a 4-agent team:

🤖 Triage Agent: Classify tickets + confidence scoring (85% threshold)
🤖 Response Agent: RAG-based responses with KB citations
🤖 Escalation Agent: Human handoff for low-confidence tickets
🤖 Learning Agent: Learn from resolved tickets, update KB

Why 4 agents?
• 3 agents → unclear handoff boundaries
• 5 agents → over-complicated for MVP
• 4 agents → clear separation, easy to debug

Key design decisions:
• 85% confidence threshold (balances 60% deflection goal vs. CSAT ≥4.0)
• GPT-4o-mini for all agents (cost-effective, good quality)
• LangGraph for orchestration (stateful, multi-agent workflows)
• Streamlit for frontend (fastest to build)

The PM dilemma: How do you balance automation (deflection rate) with quality (CSAT)?

Week 3: Building the MVP. Follow along!

#AI #CustomerSupport #MultiAgent #ProductManagement #BuildInPublic
```

---

## Post 2: The PM Dilemma - Deflection Rate vs. CSAT

**Title**: The PM dilemma: deflection rate vs. CSAT - here's how I'm balancing them

**Post**:
```
Building an AI support automation tool taught me the hardest PM tradeoff: deflection rate vs. CSAT.

The data:
• 79% of service leaders say AI agents are essential (Salesforce 2025)
• Currently only 30% of cases resolved by AI
• 61% of customers prefer self-service for simple issues

My target:
• Deflection rate: ≥60% (2x current industry average)
• CSAT: ≥4.0/5 (maintain quality)

The tension:
• Higher deflection → more automation → risk of lower CSAT
• Lower deflection → higher CSAT → less cost savings

My solution:
1. 85% confidence threshold for auto-respond
2. Human-in-the-loop for low-confidence tickets
3. Learning agent to improve over time
4. Quality scoring before sending responses

The insight:
Deflection rate isn't everything. A 50% deflection rate with 4.5 CSAT is better than 70% deflection with 3.5 CSAT.

What's your take: Would you rather deflect more tickets or maintain higher quality?

#ProductManagement #AI #CustomerService #Tradeoffs #BuildInPublic
```

---

## Post 3: Week 2 Wrap-up - Architecture Complete

**Title**: Week 2 complete: 4-agent architecture designed, Week 3: Building MVP

**Post**:
```
Week 2 wrapped! Here's what I shipped:

✅ Designed 4-agent architecture (Triage, Response, Escalation, Learning)
✅ Defined MVP scope (must-have vs. nice-to-have)
✅ Made 5 key decisions (documented in decision journal)
✅ Created technical architecture with LangGraph + Streamlit

Key decisions:
1. 4 agents (not 3 or 5) for clear handoffs
2. 85% confidence threshold (balanced target)
3. LangGraph for orchestration (stateful workflows)
4. Streamlit for frontend (fastest to build)
5. GPT-4o-mini for all agents (cost-effective)

Industry validation:
• 79% of service leaders say AI is essential
• 30% current AI resolution → 60% target (2x opportunity)
• 90% of CX leaders report positive ROI on AI

Week 3: Building the MVP!
• Implement all 4 agents
• Build Streamlit dashboard
• Recruit 5 beta users

Follow along for the build!

#AI #CustomerSupport #BuildInPublic #ProductManagement #SaaS
```

---

## Posting Schedule

**Day 1 (Monday)**: Post 1 - Architecture design
**Day 4 (Thursday)**: Post 2 - PM dilemma (deflection vs. CSAT)
**Day 7 (Sunday)**: Post 3 - Week 2 wrap-up

**Best times to post**: 8-10 AM on Tuesday-Thursday

**Engagement tips**:
- Respond to all comments within 2 hours
- Ask questions in posts to encourage engagement
- Tag relevant people/companies (e.g., @Zendesk, @Intercom)
- Use images/diagrams to make posts more visual
