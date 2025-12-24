import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

st.set_page_config(page_title="AI Finance Coach", layout="wide")

st.title("💰 AI Personal Finance Coach")
st.write("Smart insights on your finances using AI")

uploaded = st.file_uploader("Upload your transactions CSV", type=["csv"])

if not uploaded:
    st.info("Upload your CSV to see dashboard & chat with the AI coach 😊")

if uploaded:
    df = pd.read_csv(uploaded)

    # ---------- DATA PREP ----------
    df['date'] = pd.to_datetime(df['date'])

    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expenses = abs(df[df['amount'] < 0]['amount'].sum())
    net_savings = total_income - total_expenses
    savings_rate = (net_savings / total_income) * 100 if total_income > 0 else 0

    # ---------- KPI ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.0f}")
    col2.metric("Total Expenses", f"₹{total_expenses:,.0f}")
    col3.metric("Savings Rate", f"{savings_rate:.2f}%")

    # ---------- CATEGORY PIE ----------
    cat = df[df['amount'] < 0].groupby('category')['amount'].sum().abs()
    st.plotly_chart(px.pie(values=cat.values, names=cat.index,
                           title="Spending by Category"))

    # ---------- MONTHLY TREND ----------
    monthly_trend = (
        df[df['amount'] < 0]
        .resample('M', on='date')['amount']
        .sum()
        .abs()
        .reset_index()
    )

    monthly_trend['Year'] = monthly_trend['date'].dt.year
    monthly_trend['Month'] = monthly_trend['date'].dt.strftime('%b')
    monthly_trend.rename(columns={'amount': 'Spend'}, inplace=True)

    st.plotly_chart(px.line(
        monthly_trend,
        x="Month",
        y="Spend",
        color="Year",
        markers=True,
        title="Monthly Spending Trend"
    ))

    # ---------- INSIGHTS & ALERTS ----------
    st.subheader("🔔 Insights & Alerts")
    alerts = []

    # 1️⃣ Spike Detection
    avg_monthly = monthly_trend['Spend'].mean()
    last_month = monthly_trend['Spend'].iloc[-1]
    rise_percent = ((last_month - avg_monthly) / avg_monthly) * 100 if avg_monthly > 0 else 0

    if rise_percent > 30:
        alerts.append(f"⚠️ Spike Alert: Last month's spending is {rise_percent:.1f}% higher than usual.")

    # 2️⃣ Recurring Payments
    recurring = (
        df[df['amount'] < 0]
        .groupby(['category', 'amount'])
        .size()
        .reset_index(name='count')
    )

    recurring_payments = recurring[recurring['count'] >= 3]

    if not recurring_payments.empty:
        alerts.append("🔁 Recurring Payments detected:")
        for _, row in recurring_payments.iterrows():
            alerts.append(f"   • {row['category']} repeated {int(row['count'])} times (₹{abs(int(row['amount']))})")

    # 3️⃣ Fee / Charges Detection
    if 'description' in df.columns:
        fee_df = df[
            (df['amount'] < 0) &
            (df['description'].str.contains('fee|charge|penalty|late', case=False, na=False))
        ]
    else:
        fee_df = df[
            (df['amount'] < 0) &
            (df['category'].str.contains('fee|charge|penalty|late', case=False, na=False))
        ]

    if not fee_df.empty:
        alerts.append("💸 Possible Unnecessary Fees detected:")
        for _, r in fee_df.tail(5).iterrows():
            alerts.append(f"   • {r['date'].strftime('%Y-%m-%d')} — {r['category']} (₹{abs(int(r['amount']))})")

    # Savings Warning
    if savings_rate < 0:
        alerts.append("🔴 Cash Flow Warning: You are spending more than you earn.")

    # Show Alerts
    if alerts:
        for a in alerts:
            st.warning(a)
    else:
        st.success("🎉 Everything looks good! No major financial risks detected.")

    # ---------- WHAT IF ----------
    st.divider()
    st.subheader("🎯 What If You Control Your Wants?")

    if 'type' in df.columns:
        wants_df = df[df['type'] == 'Want']
        reduction = st.slider("Reduce 'Want' spending by %:", 0, 100, 20)

        months = df['date'].dt.to_period('M').nunique()
        months = max(months, 1)

        monthly_avg_wants = wants_df['amount'].abs().sum() / months
        potential = monthly_avg_wants * (reduction / 100)

        c1, c2 = st.columns(2)
        c1.metric("Monthly Savings", f"₹{potential:,.0f}")
        c2.metric("Yearly Impact", f"₹{potential*12:,.0f}")
    else:
        st.error("CSV must have a 'type' column (Want/Need).")

    # ---------- AI CHAT COACH ----------
    st.divider()
    st.subheader("🤖 Chat with Your AI Finance Coach")

    try:
        api_key = st.sidebar.text_input("Gemini API Key", type="password")

        if api_key:
            genai.configure(api_key=api_key)
        else:
            st.warning("Please enter your Gemini API Key in the sidebar to use the Chat Coach.")

        context = f"""
Income: {total_income}
Expenses: {total_expenses}
Savings Rate: {savings_rate:.2f}%
Top Categories: {cat.sort_values(ascending=False).head(5).to_dict()}
Avg Monthly Spend: {avg_monthly:.2f}
Last Month Spend: {last_month:.2f}
"""

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hi! 👋 I’m your AI Finance Coach. Ask me anything about your spending, savings, or financial health."}
            ]

        for msg in st.session_state.chat_history:
            if msg["role"] == "assistant":
                st.info(msg["content"])
            elif msg["role"] == "user":
                st.success("🧑 You: " + msg["content"])

        user_input = st.text_input("Type your question or follow‑up here:")

        if st.button("Ask Coach") and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            model = genai.GenerativeModel("models/gemini-flash-latest")

            prompt = f"""
You are a friendly personal finance coach.
Use the user's financial data to give clear, actionable, simple advice.

User Financial Summary:
{context}

Conversation:
{st.session_state.chat_history}

User Question:
{user_input}
"""

            with st.spinner("Thinking..."):
                response = model.generate_content(prompt)

            st.session_state.chat_history.append(
                {"role": "assistant", "content": response.text}
            )

            st.rerun()

    except Exception as e:
        st.error(f"AI Error: {e}")
