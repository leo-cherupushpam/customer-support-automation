# Customer Support Automation - MVP Demo

import streamlit as st
from src.agents import TriageAgent, ResponseAgent, EscalationAgent

st.set_page_config(page_title="AI Support Automation", layout="wide")

st.title("🤖 AI Customer Support Automation")
st.markdown("### Multi-Agent System for Ticket Triage and Response")

# Initialize agents
triage_agent = TriageAgent()
response_agent = ResponseAgent()
escalation_agent = EscalationAgent()

st.sidebar.header("Input Ticket")
ticket_text = st.sidebar.text_area("Enter customer ticket:", height=150)

if st.sidebar.button("Process Ticket"):
    if not ticket_text.strip():
        st.error("Please enter a ticket message")
    else:
        # Step 1: Triage
        with st.spinner("🔍 Triage Agent classifying ticket..."):
            classification = triage_agent.classify_ticket(ticket_text)
        
        st.subheader("1. Triage Agent Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", classification.category)
        col2.metric("Confidence", f"{classification.confidence:.0%}")
        col3.metric("Auto-Respond", "Yes" if classification.should_auto_respond() else "No")
        
        # Step 2: Response or Escalation
        if classification.should_auto_respond():
            with st.spinner("📝 Response Agent generating response..."):
                response = response_agent.generate_response(ticket_text, classification.category)
                quality = response_agent.evaluate_quality(response)
            
            st.subheader("2. Response Agent Results")
            st.markdown("### Generated Response")
            st.info(response)
            
            col1, col2 = st.columns(2)
            col1.metric("Quality Score", f"{quality:.2f}")
            col2.metric("Needs Human Review", "No" if quality >= 0.7 else "Yes")
            
        else:
            with st.spinner("⚠️ Escalation Agent preparing human handoff..."):
                escalation = escalation_agent.create_escalation(
                    ticket_text, 
                    classification.category, 
                    classification.confidence
                )
            
            st.subheader("2. Escalation Agent Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Context Summary")
                st.info(escalation.context_summary)
            
            with col2:
                st.markdown("### Suggested Response")
                st.warning(escalation.suggested_response)
            
            st.markdown("### Priority Assignment")
            st.error(f"🔴 {escalation.priority.upper()}")

st.divider()

st.markdown("""
### How It Works

1. **Triage Agent**: Classifies incoming tickets and assigns confidence scores
   - Confidence > 85% → Auto-respond
   - Confidence < 85% → Escalate to human

2. **Response Agent**: Generates draft responses with KB citations
   - Uses template-based responses (MVP)
   - Quality scoring to determine if human review needed

3. **Escalation Agent**: Prepares human handoff for low-confidence tickets
   - Context summary
   - Suggested response draft
   - Priority assignment

### MVP Features
- ✅ Ticket classification (5 categories)
- ✅ Confidence scoring
- ✅ Template-based responses
- ✅ Human escalation workflow
- ✅ Priority assignment
- ⏳ Knowledge base (coming soon)
- ⏳ Learning agent (coming soon)
""")
