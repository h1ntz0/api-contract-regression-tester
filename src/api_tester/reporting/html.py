import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

from api_tester.config.models import ReportConfig
from api_tester.core.constants import TestStatus
from api_tester.reporting.models import TestExecutionReport


class ReportWriter:
    """Generates CLI outputs, JSON results, JUnit XML files, and interactive HTML dashboards."""

    @classmethod
    def write_all(cls, report: TestExecutionReport, report_config: ReportConfig) -> Dict[str, str]:
        out_dir = Path(report_config.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        created_files = {}

        # 1. Write JSON Report
        if report_config.generate_json:
            json_path = out_dir / "results.json"
            json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
            created_files["json"] = str(json_path)

        # 2. Write JUnit XML
        if report_config.generate_junit:
            junit_path = out_dir / "junit.xml"
            xml_str = cls._generate_junit_xml(report)
            junit_path.write_text(xml_str, encoding="utf-8")
            created_files["junit"] = str(junit_path)

        # 3. Write HTML Report
        if report_config.generate_html:
            html_path = out_dir / "index.html"
            html_content = cls._render_html_report(report)
            html_path.write_text(html_content, encoding="utf-8")
            created_files["html"] = str(html_path)

        return created_files

    @classmethod
    def _render_html_report(cls, report: TestExecutionReport) -> str:
        # Search template in templates/ directory
        template_dir = Path(__file__).resolve().parent.parent.parent.parent / "templates"
        if not template_dir.exists():
            template_dir = Path("./templates")

        env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=True)
        try:
            template = env.get_template("report.html")
            return template.render(report=report)
        except Exception:
            # Fallback simple HTML if template file missing
            return f"<html><body><h1>{report.project_name}</h1><p>Passed: {report.summary.passed}/{report.summary.total_tests}</p></body></html>"

    @classmethod
    def _generate_junit_xml(cls, report: TestExecutionReport) -> str:
        testsuite = ET.Element(
            "testsuite",
            name=report.project_name,
            tests=str(report.summary.total_tests),
            failures=str(report.summary.failed),
            errors=str(report.summary.errors),
            skipped=str(report.summary.skipped),
            time=str(report.summary.total_duration_sec),
            timestamp=report.timestamp,
        )

        for item in report.results:
            tc = ET.SubElement(
                testsuite,
                "testcase",
                classname=f"api.{item.endpoint_id}",
                name=item.name,
                time=str(round(item.duration_ms / 1000.0, 3)),
            )

            if item.status == TestStatus.FAILED:
                fail_msg = item.failure_reason or "Assertion / contract failure"
                fail_elem = ET.SubElement(tc, "failure", message=fail_msg, type="ContractViolation")
                details = "\n".join(f"- {v.message}" for v in item.violations)
                fail_elem.text = details or fail_msg

            elif item.status == TestStatus.ERROR:
                err_elem = ET.SubElement(tc, "error", message=item.failure_reason or "Execution error", type="ExecutionError")
                err_elem.text = item.failure_reason or "Error"

            elif item.status == TestStatus.SKIPPED:
                ET.SubElement(tc, "skipped")

        return ET.tostring(testsuite, encoding="unicode", xml_declaration=True)
