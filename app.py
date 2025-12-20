import streamlit as st
import csv
import json
from io import StringIO
from pathlib import Path
from csv_profiler.profile import profile_rows
from csv_profiler.render import render_markdown

# 1. Page Configuration
st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload a CSV → profile it → export JSON + Markdown")

st.sidebar.header("Inputs")

# 2. Initialize Variables and Session State
rows = None
report = st.session_state.get("report")

# 3. Handle File Upload
uploaded = st.file_uploader("Upload a CSV", type=["csv"])
show_preview = st.sidebar.checkbox("Show preview", value=True)

if uploaded is not None:
    # Decode bytes to text
    text = uploaded.getvalue().decode("utf-8-sig")
    # Parse text into a list of dictionaries
    rows = list(csv.DictReader(StringIO(text)))
    
    # 4. Data Safeguards (Error Handling)
    if len(rows) == 0:
        st.error("CSV has no data. Upload a CSV with at least 1 row.")
        st.stop()
        
    if len(rows[0]) == 0:
        st.warning("CSV has no headers (no columns detected).")

    # 5. Data Preview
    if show_preview:
        st.subheader("Preview")
        st.write(rows[:5])
else:
    st.info("Upload a CSV to begin.")

# 6. Report Generation Logic
if rows is not None and len(rows) > 0:
    if st.button("Generate report"):
        # Run the profiling package logic
        report = profile_rows(rows)
        # Store result in session state to prevent losing it on rerun
        st.session_state["report"] = report

# Refresh the report variable from session state
report = st.session_state.get("report")

# 7. Display Results
if report is not None:
    # Summary metrics (n_rows and n_cols)
    cols = st.columns(2)
    cols[0].metric("Rows", report.get("n_rows", 0))
    cols[1].metric("Columns", report.get("n_cols", 0))

    # Display the column profile table
    st.subheader("Columns")
    st.write(report["columns"])

    # Markdown preview inside an expander
    with st.expander("Markdown preview", expanded=False):
        st.markdown(render_markdown(report))

    # 8. Export Section (Download and Save)
    st.sidebar.markdown("---")
    report_name = st.sidebar.text_input("Report name", value="report")
    
    json_file = report_name + ".json"
    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    
    md_file = report_name + ".md"
    md_text = render_markdown(report)

    # Download Buttons
    c1, c2 = st.columns(2)
    c1.download_button("Download JSON", data=json_text, file_name=json_file)
    c2.download_button("Download Markdown", data=md_text, file_name=md_file)

    # Save to outputs
    if st.button("Save to outputs/"):
        out_dir = Path("outputs")
        out_dir.mkdir(parents=True, exist_ok=True)
        
        (out_dir / json_file).write_text(json_text, encoding="utf-8")
        (out_dir / md_file).write_text(md_text, encoding="utf-8")
        
        st.success(f"Saved outputs/{json_file} and outputs/{md_file}")