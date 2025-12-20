import json
import time
import typer
from pathlib import Path
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import profile_rows
from csv_profiler.render import render_markdown

app = typer.Typer()

@app.command()
def profile(
    input_path: Path = typer.Argument(..., help="Path to the CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Where to save results"),
    report_name: str = typer.Option("report", "--report-name", help="Name of the files")
   ):
    """
    This command reads a CSV and creates JSON and Markdown reports.
    """
    try:
        # 1. Read the data
        rows = read_csv_rows(input_path)
        
        # 2. Run the profiling logic
        report = profile_rows(rows)

        # 3. Create the output folder if it doesn't exist
        out_dir.mkdir(parents=True, exist_ok=True)

        # 4. Save the JSON report
        json_path = out_dir / f"{report_name}.json"
        json_text = json.dumps(report, indent=2, ensure_ascii=False)
        json_path.write_text(json_text, encoding="utf-8")
        typer.secho(f"Produced: {json_path}", fg=typer.colors.GREEN)

        # 5. Save the Markdown report
        md_path = out_dir / f"{report_name}.md"
        md_text = render_markdown(report)
        md_path.write_text(md_text, encoding="utf-8")
        typer.secho(f"Produced: {md_path}", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)

@app.command()
def info():
    typer.echo("CSV Profiler v1.0")

if __name__ == "__main__":
    app()