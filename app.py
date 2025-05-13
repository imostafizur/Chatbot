import streamlit as st
from debate_engine import DebateAgent, MetaAI

st.set_page_config(page_title="Multi-Agent CoT Debate Chatbot")

st.title("🧠 Multi-Agent CoT Debate Chatbot")

with st.sidebar:
    st.header("🔑 API Configuration")
    agent1_key = st.text_input("Agent 1 API Key", type="password")
    agent2_key = st.text_input("Agent 2 API Key", type="password")
    meta_ai_key = st.text_input("Meta-AI API Key", type="password")
    st.markdown("---")
    model1 = st.text_input("Agent 1 Model (e.g., openai/gpt-3.5-turbo)")
    model2 = st.text_input("Agent 2 Model")
    user_query = st.text_input("Your Question", key="query_input")
    run_btn = st.button("Start Debate")

if run_btn and all([agent1_key, agent2_key, meta_ai_key, model1, model2, user_query]):
    with st.spinner("🤔 Agents are thinking..."):

        agent1 = DebateAgent("Agent Alpha", agent1_key, model1, "a strict analyst")
        agent2 = DebateAgent("Agent Beta", agent2_key, model2, "a creative thinker")

        context = ""
        output1 = agent1.think(user_query, context)
        context += f"\nAgent Alpha: {output1}"
        output2 = agent2.think(user_query, context)
        context += f"\nAgent Beta: {output2}"

        st.subheader("🧩 Agent Arguments")
        st.markdown(f"**Agent Alpha (Model: {model1}):**\n\n{output1}")
        st.markdown("---")
        st.markdown(f"**Agent Beta (Model: {model2}):**\n\n{output2}")

        st.subheader("🧠 Meta-AI Evaluation")
        meta_ai = MetaAI(meta_ai_key)
        decision = meta_ai.synthesize(user_query, {
            "Agent Alpha": output1,
            "Agent Beta": output2
        })
        st.success("Meta-AI's Final Decision:")
        st.markdown(decision)

else:
    st.info("Please fill all fields and press 'Start Debate'.")

