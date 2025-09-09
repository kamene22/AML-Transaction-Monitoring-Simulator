
# 🕵️‍♂️ AML Transaction Monitoring Simulator  

An interactive **Anti-Money Laundering (AML) Transaction Monitoring Simulator** built with **Python, Streamlit, and Machine Learning**.  
The project demonstrates how **rule-based checks** and **anomaly detection models** can work together to flag suspicious financial activities, inspired by M-PESA-style mobile money transactions.  

---

## 🌟 Features  
- **Synthetic Transaction Generator**  
  - Creates thousands of realistic transactions with sender, receiver, amount, timestamp, and location.  
  - Injects suspicious behavior (structuring, high-risk geographies, unusual spikes).  

- **Rule-Based Detection**  
  - **Structuring**: Multiple small transactions under reporting thresholds.  
  - **Geographic Risk**: Transactions from high-risk locations flagged.  
  - **Transaction Spikes**: Amounts far above customer norms detected.  

- **Machine Learning Detection**  
  - Uses **Isolation Forest** to detect hidden anomalies beyond static rules.  

- **Streamlit Dashboard**  
  - Upload or auto-generate transactions.  
  - Interactive graphs:  
    - 🚩 Suspicious Transactions by Location  
    - 🚩 Suspicious Transactions Over Time  
  - KPI metrics and suspicious transaction table.  
  - 📄 Export a detailed PDF report of flagged activities.  

---

## 📂 Project Structure  
```bash
AML-Transaction-Monitoring-Simulator/
│
├── aml_app.py                # Streamlit app entry point
├── aml_utils.py              # Helper functions (rules, ML, reporting)
├── requirements.txt          # Python dependencies
├── suspicious_transactions.csv # Sample output (auto-generated)
├── AML_Report.pdf            # Sample PDF report (auto-generated)
└── README.md                 # This file
````

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/kamene22/AML-Transaction-Monitoring-Simulator.git
cd AML-Transaction-Monitoring-Simulator
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run aml_app.py
```

👉 Your browser will open at `http://localhost:8501`.

---

## 📊 Sample Dashboard Screenshots

### Suspicious Transactions by Location

*(Example: Offshore regions showing high flags)*

### Suspicious Transactions Over Time

*(Spikes detected on certain days)*

---

## 📄 Example PDF Report

The app generates a downloadable **AML Report (PDF)** including:

* Executive Summary
* Detection methods explained
* Suspicious transaction statistics
* Visual charts
* Top 10 flagged transactions

---

## 🧠 Tech Stack

* **Python 3.9+**
* **Pandas / NumPy** – Data simulation & manipulation
* **Scikit-learn** – Isolation Forest anomaly detection
* **Matplotlib** – Visualization
* **Streamlit** – Interactive web app
* **ReportLab** – Automated PDF reporting
* **Faker** – Synthetic data generation

---

## 🎯 Use Cases

* Learn how AML monitoring works in practice.
* Prototype for fintech AML/CTF (Anti-Terrorist Financing) controls.
* Portfolio project showcasing **data science + compliance + dashboards**.

---

## 🙌 Contribution

Contributions are welcome!
If you’d like to add features (e.g., sanctions screening API, geospatial risk maps, or live transaction ingestion), feel free to open a PR.

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**[Monicah Mwanzia](https://github.com/kamene22)**

* 💼 Data Science & AI Enthusiast
* 🔍 Passionate about Fraud Detection, AML/CTF, and Responsible AI

---

⭐ If you like this project, consider giving it a **star** on GitHub!


