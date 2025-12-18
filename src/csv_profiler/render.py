from __future__ import annotations
from datetime import datetime
import json
from pathlib import Path

# Save the report as a formatted JSON file
def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    # Create directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write JSON string to file
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")


# Save the report as a detailed Markdown file
def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    rows = report["summary"]["rows"]
    columns_count = report["summary"]["columns"]
    cols = report["columns"]
    
    lines = []
    
    # Header Section
    lines.append("# CSV Profile: data/sample.csv\n")
    lines.append("\n")
    
    # Summary Section
    lines.append("## Summary\n")
    lines.append(f"- Rows: {rows:,}\n")
    lines.append(f"- Columns: {columns_count:,}\n")
    lines.append("\n")
    
    # Columns Overview Table
    lines.append("## Columns\n\n")
    lines.append("| Column | Type | Missing | Unique |\n")
    lines.append("|--------|------|---------|--------|\n")
    
    for name, col in cols.items():
        missing_percent = (col["missing"] / rows * 100) if rows > 0 else 0
        lines.append(f"| {name} | {col['type']} | {missing_percent:.1f}% | {col['unique']} |\n")
    
    lines.append("\n")
    lines.append("## Column Details\n\n")
    
    # Individual Column Details
    for name, col in cols.items():
        lines.append(f"### {name}\n")
        lines.append(f"- **Type:** {col.get('type', 'unknown')}\n")
        lines.append(f"- **Missing:** {col.get('missing', 0)}\n")
        lines.append(f"- **Unique:** {col.get('unique', 0)}\n")
        
        # Numeric Stats
        if col["type"] == "number":
            lines.append(f"- **Min:** {col.get('min', 'N/A'):.2f}\n")
            lines.append(f"- **Max:** {col.get('max', 'N/A'):.2f}\n")
            lines.append(f"- **Mean:** {col.get('mean', 'N/A'):.2f}\n")
        
        # Text Stats
        if col["type"] == "text":
            top = col.get("top", [])
            if top:
                lines.append("- **Top values:**\n")
                for value, count in top:
                    lines.append(f"  - {value}: {count}\n")
        
        lines.append("\n")
    
    # Save the combined lines to the file
    path.write_text("".join(lines), encoding="utf-8")


# Generate a Markdown string for previewing in UI
def render_markdown(report: dict) -> str:
    lines: list[str] = []
    # Report Header
    lines.append(f"# CSV Profiling Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    
    # Summary Section
    lines.append("## Summary\n")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**\n")
    
    # Column Summary Table
    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")
    
    # Add rows to the table using list comprehension
    lines.extend([
        f"| {c['name']} | {c['type']} | {c['missing']} | {c['missing_pct']:.1f}% | {c['unique']} |"
        for c in report["columns"]
    ])
    
    # Footer Notes
    lines.append("\n## Notes\n")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")
    
    return "\n".join(lines)