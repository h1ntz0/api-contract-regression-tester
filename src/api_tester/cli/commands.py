import sys
import time
from typing import Optional
import typer
from rich.console import Console

from api_tester.config.loader import load_config
from api_tester.config.models import ProjectConfig
from api_tester.core.constants import ExitCode, TestStatus
from api_tester.core.exceptions import SpecificationError, ConfigurationError, ExecutionError
from api_tester.specification.loader import SpecificationLoader
from api_tester.specification.parser import OpenApiParser
from api_tester.generator.generator import TestGenerator
from api_tester.execution.runner import TestRunner
from api_tester.reporting.aggregator import ResultAggregator
from api_tester.reporting.html import ReportWriter
from api_tester.cli.output import (
    print_banner,
    print_endpoint_discovery,
    print_test_plan,
    print_execution_summary,
)

app = typer.Typer(
    help="API Contract & Regression Tester — Automated OpenAPI CLI Engine",
    no_args_is_help=True,
)
console = Console()


@app.command("validate")
def validate_command(
    spec_path: str = typer.Argument(..., help="Path or URL to OpenAPI specification (YAML/JSON)"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config YAML file"),
    insecure: bool = typer.Option(False, "--insecure", help="Allow plain HTTP for remote specs"),
):
    """Validate OpenAPI specification syntax, structure, and $ref integrity."""
    print_banner()
    try:
        cfg = load_config(config)
        loader = SpecificationLoader(
            allow_insecure_http=insecure or cfg.execution.allow_insecure_http,
            verify_tls=cfg.execution.verify_tls,
        )
        raw_spec = loader.load(spec_path)
        parser = OpenApiParser(raw_spec)
        parsed = parser.parse()

        console.print("[bold green]✓ Specification is valid![/bold green]")
        console.print(f"  • OpenAPI Version: [cyan]{parsed.openapi_version}[/cyan]")
        console.print(f"  • Title: [bold]{parsed.metadata.title}[/bold] (v{parsed.metadata.version})")
        console.print(f"  • Endpoints: [cyan]{len(parsed.endpoints)}[/cyan]")
        console.print(f"  • Servers: [dim]{', '.join(s.url for s in parsed.servers) or 'None defined'}[/dim]\n")
        raise typer.Exit(code=ExitCode.SUCCESS)

    except typer.Exit:
        raise
    except SpecificationError as e:
        console.print(f"[bold red]Specification Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.SPEC_ERROR)
    except ConfigurationError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.CONFIG_ERROR)
    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.EXECUTION_ERROR)


@app.command("discover")
def discover_command(
    spec_path: str = typer.Argument(..., help="Path or URL to OpenAPI specification"),
    method: Optional[str] = typer.Option(None, "--method", "-m", help="Filter by HTTP method (GET, POST, etc.)"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config YAML file"),
):
    """Discover all endpoints, methods, and parameters in the OpenAPI specification."""
    print_banner()
    try:
        cfg = load_config(config)
        loader = SpecificationLoader(
            allow_insecure_http=cfg.execution.allow_insecure_http,
            verify_tls=cfg.execution.verify_tls,
        )
        raw_spec = loader.load(spec_path)
        parser = OpenApiParser(raw_spec)
        parsed = parser.parse()

        endpoints = parsed.endpoints
        if method:
            endpoints = [ep for ep in endpoints if ep.method.upper() == method.upper()]

        print_endpoint_discovery(endpoints)
        raise typer.Exit(code=ExitCode.SUCCESS)

    except typer.Exit:
        raise
    except SpecificationError as e:
        console.print(f"[bold red]Specification Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.SPEC_ERROR)
    except ConfigurationError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.CONFIG_ERROR)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.EXECUTION_ERROR)


@app.command("generate")
def generate_command(
    spec_path: str = typer.Argument(..., help="Path or URL to OpenAPI specification"),
    method: Optional[str] = typer.Option(None, "--method", "-m", help="Filter by HTTP method"),
    suite: Optional[str] = typer.Option("all", "--suite", "-s", help="Suite filter: smoke, regression, negative, all"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config YAML file"),
):
    """Generate and display synthetic test cases and test execution plan from OpenAPI specification."""
    print_banner()
    try:
        cfg = load_config(config)
        loader = SpecificationLoader(
            allow_insecure_http=cfg.execution.allow_insecure_http,
            verify_tls=cfg.execution.verify_tls,
        )
        raw_spec = loader.load(spec_path)
        parser = OpenApiParser(raw_spec)
        parsed = parser.parse()

        generator = TestGenerator(cfg.testing)
        plan = generator.generate(parsed, filter_method=method, filter_suite=suite)

        print_test_plan(plan)
        raise typer.Exit(code=ExitCode.SUCCESS)

    except typer.Exit:
        raise
    except SpecificationError as e:
        console.print(f"[bold red]Specification Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.SPEC_ERROR)
    except ConfigurationError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.CONFIG_ERROR)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.EXECUTION_ERROR)


@app.command("run")
def run_command(
    spec_path: str = typer.Argument(..., help="Path or URL to OpenAPI specification"),
    base_url: Optional[str] = typer.Option(None, "--base-url", "-u", help="Target API Base URL (overrides spec server)"),
    suite: Optional[str] = typer.Option("all", "--suite", "-s", help="Suite to execute: smoke, regression, negative, all"),
    method: Optional[str] = typer.Option(None, "--method", "-m", help="Filter by HTTP method"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config YAML file"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory for reports"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Number of concurrent workers"),
):
    """Execute automated contract and regression tests against target API."""
    print_banner()
    try:
        cfg = load_config(config)
        if output_dir:
            cfg.report.output_dir = output_dir
        if workers:
            cfg.execution.workers = workers

        loader = SpecificationLoader(
            allow_insecure_http=cfg.execution.allow_insecure_http,
            verify_tls=cfg.execution.verify_tls,
        )
        raw_spec = loader.load(spec_path)
        parser = OpenApiParser(raw_spec)
        parsed = parser.parse()

        # Resolve target base URL (CLI option > Config > Spec server)
        target_url = base_url or cfg.api.base_url
        if not target_url and parsed.servers:
            target_url = parsed.servers[0].url

        if not target_url:
            raise ConfigurationError("Missing base_url. Specify via --base-url, in config.yaml, or in openapi.yaml servers.")

        console.print(f"[bold]Specification:[/bold] [cyan]{spec_path}[/cyan]")
        console.print(f"[bold]Target Base URL:[/bold] [cyan]{target_url}[/cyan]")
        console.print(f"[bold]Concurrency:[/bold] [yellow]{cfg.execution.workers} worker(s)[/yellow]")
        console.print("[dim]Generating test plan...[/dim]")

        generator = TestGenerator(cfg.testing)
        plan = generator.generate(parsed, filter_method=method, filter_suite=suite)

        console.print(f"[bold green]Ready to execute {plan.total_cases} test cases.[/bold green]\n")

        start_time = time.perf_counter()
        runner = TestRunner(cfg, target_url)

        def progress_cb(item):
            status_symbol = "[bold green]✓[/bold green]" if item.status == TestStatus.PASSED else "[bold red]✗[/bold red]"
            console.print(f"{status_symbol} [{item.method}] {item.path} - [dim]{item.name}[/dim] ({item.duration_ms}ms)")

        results = runner.run_plan(plan, progress_callback=progress_cb)
        total_dur = time.perf_counter() - start_time

        # Aggregate report
        report = ResultAggregator.aggregate(
            results=results,
            project_name=cfg.name or parsed.metadata.title,
            base_url=target_url,
            spec_source=spec_path,
            total_duration_sec=total_dur,
        )

        report_files = ReportWriter.write_all(report, cfg.report)
        print_execution_summary(report, report_files)

        if report.summary.failed > 0 or report.summary.errors > 0:
            raise typer.Exit(code=ExitCode.TESTS_FAILED)

        raise typer.Exit(code=ExitCode.SUCCESS)

    except SpecificationError as e:
        console.print(f"[bold red]Specification Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.SPEC_ERROR)
    except ConfigurationError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.CONFIG_ERROR)
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {e}")
        raise typer.Exit(code=ExitCode.EXECUTION_ERROR)


def main():
    app()


if __name__ == "__main__":
    main()
