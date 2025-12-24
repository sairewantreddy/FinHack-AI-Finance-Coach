# FinHack-AI-Finance-Coach
An AI-powered personal finance dashboard that helps users understand spending,
track savings, detect risky behavior, and receive actionable AI guidance.

Built for students, young professionals, and anyone who wants smarter control
over their finances.

---

## 🚀 What It Does

### 📊 Interactive Finance Dashboard
✔️ Upload your transaction CSV  
✔️ Automatically analyzes your income & expenses  
✔️ Visualizes spending patterns clearly

### 🥧 Spending Insights
- Spending by category (Pie Chart)
- Monthly spending trend (Line Chart)
- Detects unusual spending behavior

### ⚠️ Smart Alerts
- Overspending detection
- Expense spikes & risky financial behavior
- Savings performance

### 🎯 “What If” Simulator
Plan smarter by simulating:
- Reduced wants/luxury spending
- See monthly + yearly savings impact

### 🤖 AI Finance Chat Coach
Chat with an intelligent finance assistant:
- Understand your habits
- Get personalized suggestions
- Ask follow‑up questions
- Maintains chat memory

---

## 🛠️ Tech Stack
- **Python**
- **Streamlit** – UI & App
- **Pandas** – Data Processing
- **Plotly** – Charts
- **Google Gemini AI** – Finance Coach Assistant

---

## 🧪 How to Use
1️⃣ Upload your transactions CSV  
2️⃣ Explore dashboard insights  
3️⃣ Run simulations  
4️⃣ Chat with your AI Coach
The app is best run locally or via Streamlit Cloud.
Colab is provided as an optional demo setup.

A **sample dataset** is included for demo ease.

---

## 📸 Screenshots
All feature screenshots are available in the /screenshots folder.

How the Demo runs:

▶️ Run on Google Colab
You can run the AI Finance Coach directly in Google Colab.

1️⃣ Install Required Libraries
Run:

!pip install -U streamlit plotly pandas google-generativeai
2️⃣ Create the Streamlit App
Run the cell below and paste the full app.py code inside it:

%%writefile app.py
# (Paste the full Streamlit app code here)
3️⃣ Download Cloudflare Tunnel
This is used to create a public URL for the Streamlit app.

!wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
!chmod +x cloudflared-linux-amd64
4️⃣ Start Streamlit
!pkill streamlit
!nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
5️⃣ Generate Public URL
Run:

!./cloudflared-linux-amd64 tunnel --url http://127.0.0.1:8501
✔️ A public https link will be generated
✔️ Open it in your browser
🎉 The app is live!

🔑 API Key
Enter your Gemini API Key in the Streamlit sidebar to enable AI chat.

📌 Notes
Colab resets if closed, so steps must be re‑run each session

Works best on desktop browser

CSV must contain:

date

amount

category

type (Want / Need)
