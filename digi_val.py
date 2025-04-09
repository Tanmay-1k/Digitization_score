import streamlit as st
import pandas as pd
import tempfile
from utility import extract_text_from_pdf, compute_digitization_score, keywords, weights

st.set_page_config(page_title="📊 Bank Digitization Score Analyzer")

st.title("📊 Bank Digitization Score Analyzer")
st.markdown("Upload one or more annual report PDFs to calculate digitization scores.")

uploaded_files = st.file_uploader("📤 Upload PDF files", type="pdf", accept_multiple_files=True)

if st.button("🔍 Analyze Reports"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one PDF file.")
    else:
        results = []

        with st.spinner("Processing reports..."):
            for file in uploaded_files:
                # Save each file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(file.read())
                    tmp_path = tmp_file.name

                text = extract_text_from_pdf(tmp_path)
                if text:
                    bank_name = file.name.split("_")[0]  # simple name extractor
                    score, _ = compute_digitization_score(text, keywords, weights)
                    results.append({
                        "FY": "2024-2025",
                        "Name of Bank": bank_name,
                        "Digitization Score": score
                    })

        if results:
            df = pd.DataFrame(results)
            st.success("✅ Analysis Complete!")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", csv, "Digitization_Scores.csv")
        else:
            st.error("❌ No valid reports processed.")
