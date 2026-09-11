<div align="center">
  <a href="https://youtu.be/8QEAUtSoVgA">
    <img src="https://img.youtube.com/vi/8QEAUtSoVgA/0.jpg" alt="Google TabFM: Fast Tabular Predictions Running Locally!">
  </a>
  <h3>📺 <a href="https://youtu.be/8QEAUtSoVgA">Watch the full tutorial on YouTube</a></h3>
</div>

# 📊 TabFM + Ollama Analyzer

> **Zero-Shot Tabular Predictions & Local LLM Insights** 🧠⚡

A visually streamlined, end-to-end tool blending **TabFM** (Tabular Foundation Model) and **Ollama** (`qwen3:4b`). Input data, get predictions instantly, and receive AI-driven summaries—no dataset training required. This repository acts as an interface and wrapper for Google's TabFM, ensuring fast tabular predictions running 100% locally.

---

## 🛠️ Tech Stack
*   🧠 **Core ML:** `TabFM` (PyTorch)
*   🤖 **Local LLM:** `Ollama` (`qwen3:4b` - zero temp/fast inference)
*   🖥️ **Frontend:** `Streamlit` 
*   💾 **Data:** `pandas` & `numpy`

## 📂 Files
*   📄 **`README.md`**: Project overview and setup.
*   🐍 **`app.py`**: Streamlit UI, TabFM engine, and Ollama integration.
*   📦 **`requirements.txt`**: Minimal Python dependencies.
*   📝 **`outputs.md` / `ideal_outputs.md`**: Auto-generated, identically matched markdown logs of your predictions and AI insights.

---

## 🚀 Setup & Execution

Copy-paste these commands directly into Windows PowerShell:

**1. Install Core Dependencies**
```powershell
git clone https://github.com/google-research/tabfm.git
cd tabfm
pip install -e .[pytorch]
pip install streamlit pandas numpy requests
ollama pull qwen3:4b
```

**2. Run Application**
```powershell
streamlit run app.py
```

**3. Quick Test (Headless)**
```powershell
python -c "from tabfm import tabfm_v1_0_0_pytorch; print('TabFM loaded successfully')"
```

---

## 🎯 5 Core Use Cases
1. 🏦 **Risk Assessment:** Instantly predict credit risk based on mixed tabular data.
2. 🏡 **Real Estate Valuation:** Zero-shot regression on property features for pricing.
3. 📉 **Customer Churn:** Identify subscription cancellations from usage data.
4. 🏥 **Medical Triage:** Classify patient risk levels from health records.
5. 📦 **Inventory Forecasting:** Predict stock needs using historical inputs.

## 🔮 5 Future Upgrades
1. 📁 **Batch Upload:** CSV support for bulk processing.
2. 🎛️ **Model Selector:** UI dropdown for various Ollama models.
3. 🖨️ **PDF Export:** Download AI insights instantly.
4. 📈 **Dynamic Charts:** Plotly integration for visual metrics.
5. ⚡ **JAX Support:** Toggle PyTorch/JAX backends directly in UI.

---

**SEO Keywords:** Google TabFM, Tabular Foundation Model, Local LLM, Ollama, Qwen3, Streamlit AI interface, zero-shot tabular predictions, offline AI inference, Python tabular analysis, data science automation.
