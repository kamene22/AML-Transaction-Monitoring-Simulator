# app.py
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import timedelta
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# -----------------------------
# Generate synthetic transactions
# -----------------------------
fake = Faker()

def generate_transactions(n=5000):
    data = []
    base_time = pd.Timestamp.now()

    for i in range(n):
        sender = fake.random_int(min=1000, max=9999)
        receiver = fake.random_int(min=1000, max=9999)
        amount = round(random.uniform(50, 5000), 2)
        timestamp = base_time - timedelta(minutes=random.randint(0, 50000))
        location = random.choice(["Nairobi", "Mombasa", "Kisumu", "Garissa", "Offshore"])
        data.append([i+1, sender, receiver, amount, timestamp, location])

    # Inject structuring (small repeated transactions)
    for j in range(20):
        sender = fake.random_int(min=1000, max=9999)
        for k in range(10):
            data.append([
                n+j*10+k,
                sender,
                fake.random_int(min=1000, max=9999),
                random.uniform(100, 999),
                base_time - timedelta(minutes=k),
                "Nairobi"
            ])
    return pd.DataFrame(data, columns=["transaction_id", "sender_id", "receiver_id", "amount", "timestamp", "location"])


# -----------------------------
# Rule-based AML checks
# -----------------------------
def apply_rules(df):
    df["rule_flagged"] = 0

    # Rule 1: Structuring
    df["small_txn"] = df["amount"] < 1000
    structuring = df.groupby("sender_id")["small_txn"].transform("sum") >= 5
    df.loc[structuring & df["small_txn"], "rule_flagged"] = 1

    # Rule 2: High-risk locations
    df.loc[df["location"].isin(["Offshore", "Garissa"]), "rule_flagged"] = 1

    # Rule 3: Transaction spikes
    avg_amounts = df.groupby("sender_id")["amount"].transform("mean")
    df.loc[df["amount"] > 5 * avg_amounts, "rule_flagged"] = 1

    return df


# -----------------------------
# ML anomaly detection
# -----------------------------
def apply_ml(df):
    features = pd.get_dummies(df[["amount", "location"]], drop_first=True)
    iso = IsolationForest(contamination=0.02, random_state=42)
    df["ml_flagged"] = iso.fit_predict(features)
    df["ml_flagged"] = df["ml_flagged"].map({1: 0, -1: 1})
    df["suspicious"] = df[["rule_flagged", "ml_flagged"]].max(axis=1)
    return df


# -----------------------------
# PDF Reporting
# -----------------------------
def generate_pdf_report(df):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Anti-Money Laundering (AML) Monitoring Report", styles['Title']))
    story.append(Spacer(1, 20))

    # Executive Summary
    total_txn = len(df)
    total_suspicious = df['suspicious'].sum()
    perc = round((total_suspicious/total_txn)*100, 2)
    risk_level = "High Risk" if perc > 5 else "Elevated" if perc > 2 else "Low Risk"

    summary = f"""
    <b>Executive Summary:</b><br/><br/>
    Total Transactions: {total_txn}<br/>
    Suspicious Transactions: {total_suspicious} ({perc}%)<br/>
    Overall Risk Level: {risk_level}<br/><br/>
    Key Findings:<br/>
    • Structuring detected (small repeated transfers)<br/>
    • High-risk geography transactions<br/>
    • Transaction spikes above normal behavior<br/>
    • ML anomalies identified unusual hidden patterns<br/>
    """
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 20))

    # Top suspicious transactions
    story.append(Paragraph("🔎 Top 10 Suspicious Transactions", styles['Heading2']))
    top_suspicious = df[df['suspicious']==1].sort_values("amount", ascending=False).head(10)
    for _, row in top_suspicious.iterrows():
        tx = f"TxnID: {row['transaction_id']} | Sender: {row['sender_id']} | Receiver: {row['receiver_id']} | Amount: {row['amount']} | Location: {row['location']}"
        story.append(Paragraph(tx, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer


# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.title("💰 AML Transaction Monitoring Simulator")
    st.write("Simulates M-PESA-like transactions and applies AML rules + ML anomaly detection.")

    n = st.slider("Number of transactions to simulate:", 1000, 10000, 5000, step=500)

    if st.button("Run Simulation"):
        df = generate_transactions(n)
        df = apply_rules(df)
        df = apply_ml(df)

        st.subheader("📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", len(df))
        col2.metric("Suspicious Transactions", int(df['suspicious'].sum()))
        col3.metric("Suspicious %", f"{round(df['suspicious'].mean()*100,2)}%")

        st.subheader("🚩 Suspicious Transactions Preview")
        st.dataframe(df[df["suspicious"]==1].head(20))

        st.subheader("📍 Suspicious by Location")
        susp_by_loc = df.groupby("location")["suspicious"].sum()
        st.bar_chart(susp_by_loc)

        st.subheader("📈 Suspicious Over Time")
        susp_over_time = df.set_index("timestamp").resample("D")["suspicious"].sum()
        st.line_chart(susp_over_time)

        # Download suspicious CSV
        suspicious_df = df[df["suspicious"]==1]
        csv = suspicious_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Suspicious Transactions (CSV)", csv, "suspicious_transactions.csv", "text/csv")

        # Download PDF Report
        pdf_buffer = generate_pdf_report(df)
        st.download_button("⬇️ Download AML Report (PDF)", pdf_buffer, "AML_Report.pdf", "application/pdf")

if __name__ == "__main__":
    main()
