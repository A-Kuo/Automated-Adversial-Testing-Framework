"""
RTaaS CLI entry point.

Usage:
    rtaas evaluate --target-url URL [--target-model MODEL] [--profile PROFILE]
    rtaas list-profiles
    rtaas list-attacks --profile PROFILE
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    app = typer.Typer(name="rtaas", help="Red-Team-as-a-Service CLI")
    console = Console()
    _HAS_TYPER = True
except ImportError:
    _HAS_TYPER = False


def _no_typer() -> None:
    print("Install 'typer' and 'rich' for CLI support: pip install rtaas")
    sys.exit(1)


if _HAS_TYPER:
    @app.command()
    def evaluate(
        target_url: str = typer.Option(..., "--target-url", help="OpenAI-compatible endpoint URL"),
        target_auth: str | None = typer.Option(None, "--target-auth", help="Authorization header value"),
        target_model: str = typer.Option("unknown", "--target-model", help="Model name for report"),
        profile: str = typer.Option("general_basic", "--profile", help="Attack profile to run"),
        max_attacks: int = typer.Option(50, "--max-attacks", help="Maximum number of attacks"),
        compliance: str = typer.Option(
            "eu_ai_act,nist_ai_rmf", "--compliance", help="Comma-separated compliance frameworks"
        ),
        output: Path = typer.Option(Path("report.json"), "--output", help="Output JSON path"),
        mock: bool = typer.Option(False, "--mock", help="Use mock target (no API calls)"),
    ) -> None:
        """Run a red-team evaluation against a target LLM."""
        from rtaas.attack_engine.library import AttackProfile
        from rtaas.evaluator import Evaluator

        if mock:
            target_url = "http://mock.local/v1/chat/completions"
            console.print("[yellow]Running in mock mode — no real API calls will be made.[/yellow]")

        try:
            prof = AttackProfile(profile)
        except ValueError:
            valid = [p.value for p in AttackProfile]
            console.print(f"[red]Unknown profile '{profile}'. Valid: {valid}[/red]")
            raise typer.Exit(1)

        frameworks = [f.strip() for f in compliance.split(",") if f.strip()]

        console.print("\n[bold]RTaaS Evaluation[/bold]")
        console.print(f"Target:  {target_url}")
        console.print(f"Profile: {prof.value}  |  Max attacks: {max_attacks}")
        console.print(f"Frameworks: {frameworks}\n")

        evaluator = Evaluator(target_url=target_url, target_auth=target_auth)
        report = evaluator.run(
            profile=prof,
            compliance_frameworks=frameworks,
            max_attacks=max_attacks,
            target_model=target_model,
            verbose=True,
        )

        report.export_json(str(output))
        console.print(f"\n[green]Report saved to {output}[/green]")

    @app.command()
    def list_profiles() -> None:
        """List available attack profiles."""
        from rtaas.attack_engine.library import AttackProfile

        table = Table(title="Available Attack Profiles")
        table.add_column("Profile", style="cyan")
        for prof in AttackProfile:
            table.add_row(prof.value)
        console.print(table)

    @app.command()
    def list_attacks(
        profile: str = typer.Option("general_basic", "--profile"),
    ) -> None:
        """List attacks in a given profile."""
        from rtaas.attack_engine.library import AttackLibrary, AttackProfile

        try:
            prof = AttackProfile(profile)
        except ValueError:
            console.print(f"[red]Unknown profile: {profile}[/red]")
            raise typer.Exit(1)

        library = AttackLibrary()
        attacks = library.load(prof)

        table = Table(title=f"Attacks in profile: {profile}")
        table.add_column("ID", style="cyan", width=12)
        table.add_column("Domain", width=12)
        table.add_column("Harm Category", width=22)
        table.add_column("Severity", width=10)
        table.add_column("Prompt (truncated)")

        for atk in attacks:
            table.add_row(
                atk.attack_id,
                atk.domain,
                atk.harm_category,
                atk.severity_if_failed,
                atk.prompt[:60] + "..." if len(atk.prompt) > 60 else atk.prompt,
            )
        console.print(table)

else:
    def app() -> None:  # type: ignore[misc]
        _no_typer()
