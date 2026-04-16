# Customer Support Automation - Enhanced Demo

import streamlit as st
from src.agents import TriageAgent, ResponseAgent, EscalationAgent
from utils.analytics import AnalyticsTracker
from utils.export import export_to_csv
import tempfile
import os

st.set_page_config(page_title="AI Support Automation", layout="wide", initial_sidebar_state="expanded")

st.title("🤖 AI Customer Support Automation")
st.markdown("### Multi-Agent System with Advanced Features")

# Initialize agents and analytics
triage_agent = TriageAgent()
response_agent = ResponseAgent()
escalation_agent = EscalationAgent()
analytics = AnalyticsTracker("analytics.json")

# Session state for ticket history
if 'ticket_history' not in st.session_state:
    st.session_state.ticket_history = []

# Sidebar
st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("---")
st.sidebar.markdown("### Process Ticket")

ticket_text = st.sidebar.text_area("Enter customer ticket:", height=150, key="ticket_input")

col1, col2 = st.sidebar.columns(2)
with col1:
    process_button = st.sidebar.button("🚀 Process Ticket", type="primary")
with col2:
    export_button = st.sidebar.button("📥 Export CSV")

# Handle export
if export_button:
    if st.session_state.ticket_history:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
            export_to_csv(st.session_state.ticket_history, tmp_file.name)
            
            with open(tmp_file.name, 'rb') as f:
                st.download_button(
                    label="📥 Download CSV",
                    data=f,
                    file_name="support_tickets.csv",
                    mime="text/csv"
                )
            os.unlink(tmp_file.name)
    else:
        st.warning("No tickets to export. Process some tickets first!")

# Process ticket
if process_button:
    if not ticket_text.strip():
        st.error("Please enter a ticket message")
    else:
        with st.spinner("🔍 Processing ticket..."):
            # Step 1: Triage
            classification = triage_agent.classify_ticket(ticket_text)
            
            # Step 2: Response or Escalation
            if classification.should_auto_respond():
                response = response_agent.generate_response(ticket_text, classification.category)
                quality = response_agent.evaluate_quality(response)
                
                # Save to analytics
                analytics.track_ticket_processed(
                    ticket_id=str(len(st.session_state.ticket_history) + 1),
                    category=classification.category,
                    auto_responded=True,
                    confidence=classification.confidence,
                    tokens_used=200,  # Estimate
                    response_time=0.5  # Estimate
                )
                
                # Add to history
                st.session_state.ticket_history.append({
                    "ticket_id": str(len(st.session_state.ticket_history) + 1),
                    "ticket_text": ticket_text,
                    "category": classification.category,
                    "response": response,
                    "auto_responded": True,
                    "confidence": classification.confidence,
                    "priority": "low"
                })
                
                # Display results
                st.subheader("✅ Auto-Responded")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Category", classification.category)
                col2.metric("Confidence", f"{classification.confidence:.0%}")
                col3.metric("Quality Score", f"{quality:.2f}")
                
                st.markdown("### Generated Response")
                st.info(response)
                
                st.success(f"✅ Auto-responded (Quality: {quality:.2f})")
                
            else:
                escalation = escalation_agent.create_escalation(
                    ticket_text, 
                    classification.category, 
                    classification.confidence
                )
                
                # Save to analytics
                analytics.track_ticket_processed(
                    ticket_id=str(len(st.session_state.ticket_history) + 1),
                    category=classification.category,
                    auto_responded=False,
                    confidence=classification.confidence,
                    tokens_used=150,  # Estimate
                    response_time=0.5  # Estimate
                )
                
                # Add to history
                st.session_state.ticket_history.append({
                    "ticket_id": str(len(st.session_state.ticket_history) + 1),
                    "ticket_text": ticket_text,
                    "category": classification.category,
                    "response": escalation.suggested_response,
                    "auto_responded": False,
                    "confidence": classification.confidence,
                    "priority": escalation.priority
                })
                
                # Display results
                st.subheader("⚠️ Escalated to Human")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Context Summary")
                    st.info(escalation.context_summary)
                
                with col2:
                    st.markdown("### Suggested Response")
                    st.warning(escalation.suggested_response)
                
                st.markdown(f"### Priority: {escalation.priority.upper()}")
                if escalation.priority == "urgent":
                    st.error("🔴 URGENT - Immediate attention required")
                elif escalation.priority == "high":
                    st.error("🔴 HIGH - Priority handling")
                elif escalation.priority == "medium":
                    st.warning("🟡 MEDIUM - Standard handling")
                else:
                    st.success("🟢 LOW - Queue for later")

st.divider()

# Analytics Dashboard
st.subheader("📊 Analytics Dashboard")
stats = analytics.get_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", stats["total_tickets"])
col2.metric("Deflection Rate", f"{stats['deflection_rate']:.1%}")
col3.metric("Avg Response Time", f"{stats['average_response_time']:.2f}s")
col4.metric("Est. Cost", f"${stats['estimated_cost']:.4f}")

st.markdown("---")
st.subheader("Category Distribution")
if stats["category_distribution"]:
    for category, count in stats["category_distribution"].items():
        st.write(f"• {category}: {count}")
else:
    st.info("No data yet. Process some tickets to see analytics.")

st.divider()

# Ticket History
st.subheader("📋 Recent Tickets")
if st.session_state.ticket_history:
    for ticket in st.session_state.ticket_history[-5:]:  # Show last 5
        with st.expander(f"Ticket #{ticket['ticket_id']} - {ticket['category']}"):
            st.write(f"**Text:** {ticket['ticket_text']}")
            st.write(f"**Response:** {ticket['response']}")
            st.write(f"**Auto-Responded:** {'✅ Yes' if ticket['auto_responded'] else '❌ No'}")
            st.write(f"**Confidence:** {ticket['confidence']:.0%}")
            if not ticket['auto_responded']:
                st.write(f"**Priority:** {ticket['priority'].upper()}")
else:
    st.info("No tickets processed yet. Enter a ticket and click 'Process Ticket' to get started!")

st.divider()

st.markdown("""
### How It Works

1. **Triage Agent**: Classifies incoming tickets and assigns confidence scores
   - Confidence > 85% → Auto-respond
   - Confidence < 85% → Escalate to human

2. **Response Agent**: Generates draft responses with quality scoring
   - Template-based responses (MVP)
   - Quality scoring to determine if human review needed

3. **Escalation Agent**: Prepares human handoff for low-confidence tickets
   - Context summary
   - Suggested response draft
   - Priority assignment based on urgency and sentiment

### Features
- ✅ Ticket classification (5 categories)
- ✅ Confidence scoring
- ✅ Template-based responses
- ✅ Human escalation workflow
- ✅ Priority assignment
- ✅ Analytics tracking
- ✅ CSV export
- ⏳ Streaming responses (coming soon)
- ⏳ RAG knowledge base (Week 2)
""")
