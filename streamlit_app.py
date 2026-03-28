import html
import json
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

from ai_pipeline import FileCleansingPipeline, ProcessedArtifact, save_uploaded_file


st.set_page_config(page_title="AI File Cleansing and Analysis", layout="wide")


@st.cache_resource
def get_pipeline() -> FileCleansingPipeline:
    return FileCleansingPipeline(root_dir=str(Path(__file__).resolve().parent))


def render_results_table(results: List[ProcessedArtifact]) -> str:
    rows = []
    for item in results:
        findings_html = "".join(f"<li>{html.escape(point)}</li>" for point in item.key_findings)
        rows.append(
            "<tr>"
            f"<td>{html.escape(item.file_name)}</td>"
            f"<td>{html.escape(item.file_type)}</td>"
            f"<td>{html.escape(item.file_description)}</td>"
            f"<td><ul>{findings_html}</ul></td>"
            "</tr>"
        )

    return (
        "<table style='width:100%; border-collapse: collapse;'>"
        "<thead><tr>"
        "<th style='border-bottom:1px solid #ccc; text-align:left; padding:8px;'>File Name</th>"
        "<th style='border-bottom:1px solid #ccc; text-align:left; padding:8px;'>File Type</th>"
        "<th style='border-bottom:1px solid #ccc; text-align:left; padding:8px;'>Description</th>"
        "<th style='border-bottom:1px solid #ccc; text-align:left; padding:8px;'>Key Findings</th>"
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )


def show_masked_preview(result: ProcessedArtifact) -> None:
    masked_path = Path(result.masked_file_path)
    suffix = masked_path.suffix.lower()

    st.write(f"Masked file: {masked_path.name}")

    if suffix in {".png", ".jpg", ".jpeg"}:
        st.image(str(masked_path), caption="Masked image preview", use_container_width=True)
    elif suffix == ".txt":
        st.text_area("Masked text preview", masked_path.read_text(encoding="utf-8", errors="ignore"), height=220)
    elif suffix == ".xlsx":
        try:
            sheets = pd.read_excel(masked_path, sheet_name=None)
            first_sheet = next(iter(sheets.values()))
            st.dataframe(first_sheet, use_container_width=True)
        except Exception as exc:
            st.warning(f"Could not preview Excel file: {exc}")
    elif suffix == ".pdf":
        st.info("PDF preview is available as a download.")
    else:
        st.info("Preview is not available for this file type.")

    st.download_button(
        label="Download masked file",
        data=masked_path.read_bytes(),
        file_name=masked_path.name,
        mime="application/octet-stream",
        key=f"download_{result.file_name}_{result.file_type}",
    )


def build_structured_report_payload(results: List[ProcessedArtifact]) -> List[dict]:
    payload: List[dict] = []
    for result in results:
        payload.append(
            {
                "file_name": result.file_name,
                "file_type": result.file_type,
                "file_description": result.file_description,
                "key_findings": result.key_findings,
            }
        )
    return payload


def main() -> None:
    st.title("AI-Powered File Cleansing and Analysis")
    st.write(
        "Upload PDF, image, PPTX, XLSX, or TXT files. "
        "The app extracts text, detects and masks PII, saves intermediate outputs, and builds report-style insights."
    )

    pipeline = get_pipeline()

    uploads = st.file_uploader(
        "Upload one or more files",
        type=["pdf", "png", "jpg", "jpeg", "pptx", "xlsx", "txt"],
        accept_multiple_files=True,
    )

    if "results" not in st.session_state:
        st.session_state.results = []

    if st.button("Process Files", type="primary"):
        if not uploads:
            st.warning("Please upload at least one supported file.")
        else:
            processed_results: List[ProcessedArtifact] = []
            with st.spinner("Running extraction, PII detection, masking, and analysis..."):
                for uploaded_file in uploads:
                    saved_file = save_uploaded_file(uploaded_file, pipeline.upload_dir)
                    if saved_file is None:
                        st.warning(f"Skipped unsupported file: {uploaded_file.name}")
                        continue
                    processed_results.append(pipeline.process_file(saved_file))
            st.session_state.results = processed_results
            st.success(f"Processed {len(processed_results)} file(s).")

    if st.session_state.results:
        results: List[ProcessedArtifact] = st.session_state.results
        structured_report = build_structured_report_payload(results)

        st.subheader("Structured Report")
        st.markdown(render_results_table(results), unsafe_allow_html=True)
        st.download_button(
            label="Download full structured report (JSON)",
            data=json.dumps(structured_report, indent=2),
            file_name="structured_report.json",
            mime="application/json",
            key="download_structured_report_json",
        )

        st.subheader("Per-File Details")
        for result in results:
            with st.expander(f"{result.file_name} ({result.file_type})", expanded=False):
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("**Masked File Preview**")
                    show_masked_preview(result)

                with col2:
                    st.markdown("**Detected PII Entities (Structured)**")
                    entities_df = pd.DataFrame(result.entities)
                    if entities_df.empty:
                        st.write("No PII entities detected.")
                    else:
                        st.dataframe(entities_df, use_container_width=True)

                    st.markdown("**Output JSON**")
                    payload = {
                        "file_name": result.file_name,
                        "file_type": result.file_type,
                        "file_description": result.file_description,
                        "key_findings": result.key_findings,
                    }
                    st.code(json.dumps(payload, indent=2), language="json")
                    st.download_button(
                        label="Download this file's report (JSON)",
                        data=json.dumps(payload, indent=2),
                        file_name=f"{Path(result.file_name).stem}_report.json",
                        mime="application/json",
                        key=f"download_report_{result.file_name}",
                    )

                st.markdown("**Intermediate: Extracted Raw Text**")
                st.text_area(
                    f"raw_{result.file_name}",
                    result.raw_text,
                    height=180,
                    label_visibility="collapsed",
                )

                st.markdown("**Intermediate: Cleaned Text (PII Masked)**")
                st.text_area(
                    f"clean_{result.file_name}",
                    result.cleaned_text,
                    height=180,
                    label_visibility="collapsed",
                )


if __name__ == "__main__":
    main()
