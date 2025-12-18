import json
import time
import typer
from pathlib import Path
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import profile_rows
from csv_profiler.render import render_markdown

# Initialize Typer app
app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
):
    """
    Command to read CSV, generate profiling report, and save results.
    """
    try:
        # Start high-resolution timer
        t0 = time.perf_counter_ns()

        # Load and profile data
        rows = read_csv_rows(input_path)
        report = profile_rows(rows)

        # Stop timer and calculate elapsed time in milliseconds
        t1 = time.perf_counter_ns()
        report["timing_ms"] = (t1 - t0) / 1_000_000

        # Ensure output directory exists
        out_dir.mkdir(parents=True, exist_ok=True)

        # Write JSON report to disk
        json_path = out_dir / f"{report_name}.json"
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        typer.secho(f"Wrote {json_path}", fg=typer.colors.GREEN)

        # Write Markdown report to disk
        md_path = out_dir / f"{report_name}.md"
        md_path.write_text(render_markdown(report), encoding="utf-8")
        typer.secho(f"Wrote {md_path}", fg=typer.colors.GREEN)

        # Display preview summary if flag is set
        if preview:
            typer.echo(f"Rows: {report['n_rows']} | Cols: {report['n_cols']} | {report['timing_ms']:.2f}ms")

    except Exception as e:
        # Catch any errors, display in red, and exit with error code
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

# Main entry point for CLI execution
if __name__ == "__main__":
    app()