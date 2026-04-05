"""CLI interface for Cover Letter Generator."""

import logging
import sys
import os

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core import (
    generate_cover_letter,
    read_file,
    load_config,
    get_tones,
    match_skills,
    save_revision,
    list_revisions,
    TONES,
)

console = Console()
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S")


@click.group()
@click.option("--config", "config_path", default="config.yaml", help="Path to config file.")
@click.option("--verbose", is_flag=True, help="Enable verbose logging.")
@click.pass_context
def cli(ctx, config_path, verbose):
    """✉️ Cover Letter Generator - Generate personalized cover letters with AI."""
    setup_logging(verbose)
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config_path)


@cli.command()
@click.option("--resume", required=True, help="Path to resume text file.")
@click.option("--job-description", "job_desc", required=True, help="Path to job description text file.")
@click.option("--company", required=True, help="Company name.")
@click.option("--tone", type=click.Choice(list(TONES.keys()), case_sensitive=False), default="professional", help="Writing tone.")
@click.option("--name", default=None, help="Applicant name.")
@click.option("--output", "-o", default=None, help="Save output to file.")
@click.option("--show-skills", is_flag=True, help="Show skill matching analysis.")
@click.pass_context
def generate(ctx, resume, job_desc, company, tone, name, output, show_skills):
    """Generate a cover letter from resume and job description."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    from common.llm_client import check_ollama_running

    config = ctx.obj["config"]
    console.print(Panel.fit("[bold green]✉️ Cover Letter Generator[/bold green]", border_style="green"))

    if not check_ollama_running():
        console.print("[red]Error: Ollama is not running. Start it with: ollama serve[/red]")
        sys.exit(1)

    resume_text = read_file(resume, "Resume")
    jd_text = read_file(job_desc, "Job description")

    skill_match_data = match_skills(resume_text, jd_text)

    console.print(f"  [cyan]Company:[/cyan]  {company}")
    console.print(f"  [cyan]Tone:[/cyan]     {tone}")
    console.print(f"  [cyan]Resume:[/cyan]   {resume} ({len(resume_text)} chars)")
    console.print(f"  [cyan]JD:[/cyan]       {job_desc} ({len(jd_text)} chars)")
    console.print(f"  [cyan]Match:[/cyan]    {skill_match_data['match_percentage']}%")
    if name:
        console.print(f"  [cyan]Name:[/cyan]     {name}")
    console.print()

    if show_skills:
        _show_skill_table(skill_match_data)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        progress.add_task("Writing cover letter...", total=None)
        result = generate_cover_letter(resume_text, jd_text, company, tone, name, skill_match_data, config)

    console.print(Panel(Markdown(result), title="✉️ Cover Letter", border_style="green"))

    word_count = len(result.split())
    console.print(f"\n[dim]Word count: ~{word_count}[/dim]")

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(result)
        console.print(f"[green]✓ Saved to {output}[/green]")

    path = save_revision(result, company, 1, config)
    console.print(f"[green]✓ Revision saved to {path}[/green]")


def _show_skill_table(skill_match: dict):
    """Display skill matching table."""
    table = Table(title="🎯 Skill Match Analysis", border_style="green")
    table.add_column("Category", style="cyan")
    table.add_column("Matched ✅", style="green")
    table.add_column("Missing ❌", style="red")
    table.add_column("Extra 💡", style="yellow")
    for cat in ["technical", "soft", "domain"]:
        table.add_row(
            cat.title(),
            ", ".join(skill_match["matched"][cat]) or "—",
            ", ".join(skill_match["missing"][cat]) or "—",
            ", ".join(skill_match["extra"][cat]) or "—",
        )
    console.print(table)
    console.print(f"[bold]Overall Match: {skill_match['match_percentage']}%[/bold]\n")


@cli.command()
def tones():
    """List available writing tones."""
    table = Table(title="🎨 Writing Tones", border_style="green")
    table.add_column("Key", style="cyan")
    table.add_column("", style="bold")
    table.add_column("Name", style="bold")
    table.add_column("Description")
    for key, tone in get_tones().items():
        table.add_row(key, tone["icon"], tone["name"], tone["description"])
    console.print(table)


@cli.command()
@click.option("--company", default=None, help="Filter by company name.")
@click.pass_context
def revisions(ctx, company):
    """List saved revision history."""
    config = ctx.obj["config"]
    revs = list_revisions(company, config)
    if not revs:
        console.print("[yellow]No revisions found.[/yellow]")
        return
    table = Table(title="📝 Revision History", border_style="green")
    table.add_column("Filename", style="cyan")
    table.add_column("Size", justify="right")
    table.add_column("Date")
    for r in revs:
        table.add_row(r["filename"], f"{r['size']:,} B", r["modified"][:19])
    console.print(table)


@cli.command()
@click.option("--resume", required=True, help="Path to resume text file.")
@click.option("--job-description", "job_desc", required=True, help="Path to job description text file.")
def skills(resume, job_desc):
    """Analyze skill match between resume and job description."""
    resume_text = read_file(resume, "Resume")
    jd_text = read_file(job_desc, "Job description")
    skill_match = match_skills(resume_text, jd_text)
    _show_skill_table(skill_match)


def main():
    cli()

if __name__ == "__main__":
    main()
