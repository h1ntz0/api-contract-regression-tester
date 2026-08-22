from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from api_tester.core.constants import TestStatus
from api_tester.reporting.models import TestExecutionReport, TestResultItem

console = Console()


def print_banner():
    console.print(
        Panel.fit(
            "[bold cyan]API Contract & Regression Tester[/bold cyan]\n"
            "[dim]Automated OpenAPI Specification-Driven Testing[/dim]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )


def print_endpoint_discovery(endpoints: list):
    table = Table(title="Discovered API Endpoints", box=box.SIMPLE_HEAVY)
    table.add_column("Method", style="bold magenta", width=8)
    table.add_column("Path", style="cyan")
    table.add_column("Summary / Tags", style="dim")
    table.add_column("Parameters", justify="right")
    table.add_column("Responses", justify="right")

    for ep in endpoints:
        m_color = {
            "GET": "cyan",
            "POST": "green",
            "PUT": "yellow",
            "DELETE": "red",
            "PATCH": "magenta",
        }.get(ep.method, "white")

        table.add_row(
            f"[{m_color}]{ep.method}[/{m_color}]",
            ep.path,
            ep.summary or ", ".join(ep.tags) or "-",
            str(len(ep.parameters)),
            ", ".join(ep.responses.keys()) if ep.responses else "none",
        )

    console.print(table)
    console.print(f"\n[bold]Total endpoints discovered:[/bold] [cyan]{len(endpoints)}[/cyan]\n")


def print_test_plan(plan):
    table = Table(title="Generated Test Cases", box=box.ROUNDED)
    table.add_column("Test ID", style="dim", width=10)
    table.add_column("Method", style="bold", width=8)
    table.add_column("Path", style="cyan")
    table.add_column("Test Name", style="white")
    table.add_column("Suite", style="blue")
    table.add_column("Type", style="yellow")

    for tc in plan.test_cases:
        table.add_row(
            tc.id,
            tc.method,
            tc.path,
            tc.name,
            tc.suite,
            tc.test_type.value,
        )

    console.print(table)
    console.print(f"\n[bold]Total test cases in plan:[/bold] [green]{plan.total_cases}[/green]\n")


def print_execution_summary(report: TestExecutionReport, report_files: dict):
    console.print("\n" + "─" * 50)
    console.print("[bold]Test Execution Summary[/bold]")
    console.print("─" * 50)

    summary = report.summary
    console.print(f"Total Tests : [bold]{summary.total_tests}[/bold]")
    console.print(f"Passed      : [bold green]{summary.passed}[/bold green]")
    console.print(f"Failed      : [bold red]{summary.failed}[/bold red]")
    console.print(f"Errors      : [bold yellow]{summary.errors}[/bold yellow]")
    console.print(f"Skipped     : [bold dim]{summary.skipped}[/bold dim]")
    console.print(f"Pass Rate   : [bold cyan]{summary.pass_rate}%[/bold cyan]")
    console.print(f"Duration    : [dim]{summary.total_duration_sec}s[/dim]")
    console.print(f"Avg Response: [dim]{summary.avg_response_time_ms} ms[/dim]")

    if summary.failed > 0 or summary.errors > 0:
        console.print("\n[bold red]Failures Breakdown:[/bold red]")
        for item in report.results:
            if item.status in (TestStatus.FAILED, TestStatus.ERROR):
                console.print(f"  [red]✗[/red] [{item.method}] {item.path} - {item.name}")
                for v in item.violations:
                    console.print(f"      [dim]→ {v.message}[/dim]")

    console.print("\n[bold]Generated Artifacts:[/bold]")
    for fmt, path in report_files.items():
        console.print(f"  • {fmt.upper()}: [cyan]{path}[/cyan]")
    console.print()
