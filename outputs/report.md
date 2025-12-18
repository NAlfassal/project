from __future__ import annotations
from pathlib import Path

def write_markdown(report: dict, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    n_rows = report.get("n_rows", 0)
    columns = report.get("columns", [])
    missing_data = report.get("missing_values_per_column", {})

    lines = [
        "# Data Profile Report",
        "",
        f"- **Total Rows:** {n_rows}",
        f"- **Total Columns:** {len(columns)}",
        "",
        "## Missing Values",
        "",
        "| Column Name | Missing Count |",
        "| :--- | :--- |"
    ]

    for col in columns:
        count = missing_data.get(col, 0)
        lines.append(f"| {col} | {count} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
