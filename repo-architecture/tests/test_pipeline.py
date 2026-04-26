"""Smoke tests for the deterministic pieces of repo-architecture.

Run from anywhere with: python3 -m unittest repo-architecture.tests.test_pipeline
Or from the tests/ directory:  python3 -m unittest test_pipeline

Covers:
- validate.py: VALID / INVALID / REFUSED exit codes and error messages.
- render.py:   the SAP example plan plus each fixture renders to HTML
               containing the expected layer classes, components, and prefix.
- extract.py:  smoke check on the script's argument handling (no network).

CI-friendly: only PyYAML is needed beyond the stdlib. Network is not touched.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BIN = ROOT / "bin"
FIXTURES = HERE / "fixtures"


def run(args: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args],
        capture_output=True, text=True, **kw,
    )


class ValidatePy(unittest.TestCase):
    def test_valid_plan_exits_zero(self):
        r = run([str(BIN / "validate.py"), str(FIXTURES / "valid-plan.yaml")])
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertIn("VALID", r.stdout)
        self.assertIn("layers:   user, application, data", r.stdout)

    def test_invalid_plan_reports_each_error(self):
        r = run([str(BIN / "validate.py"), str(FIXTURES / "invalid-plan.yaml")])
        self.assertEqual(r.returncode, 1)
        self.assertIn("INVALID", r.stdout)
        # Must surface the three intentional defects in invalid-plan.yaml.
        self.assertIn("invalid layout 'fancy-grid'", r.stdout)
        self.assertIn("missing evidence", r.stdout)
        self.assertIn("only 1 layer(s) populated", r.stdout)

    def test_refused_plan_passes_through_with_exit_2(self):
        r = run([str(BIN / "validate.py"), str(FIXTURES / "refused-plan.yaml")])
        self.assertEqual(r.returncode, 2)
        self.assertIn("REFUSED", r.stdout)
        self.assertIn("cookbook repo", r.stdout)
        self.assertIn("--scope", r.stdout)

    def test_validator_accepts_json(self):
        # Convert the YAML fixture to JSON on the fly.
        import yaml
        plan = yaml.safe_load((FIXTURES / "valid-plan.yaml").read_text())
        json_path = HERE / "_tmp_valid.json"
        json_path.write_text(json.dumps(plan))
        try:
            r = run([str(BIN / "validate.py"), str(json_path)])
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        finally:
            json_path.unlink()


class RenderPy(unittest.TestCase):
    OUT = HERE / "_tmp_render.html"

    def tearDown(self):
        if self.OUT.exists():
            self.OUT.unlink()

    def test_renders_fixture_to_html(self):
        r = run([
            str(BIN / "render.py"),
            str(FIXTURES / "valid-plan.yaml"),
            "--out", str(self.OUT),
            "--prefix", "tst",
        ])
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertTrue(self.OUT.exists())
        html = self.OUT.read_text()

        # Doctype and structural tags.
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("</html>", html)

        # Title and subtitle made it into the page.
        self.assertIn("Test Service", html)
        self.assertIn("Smoke-test plan", html)

        # Custom prefix was applied to all classes (no .arch- residue).
        self.assertNotIn(".arch-", html)
        self.assertIn(".tst-", html)
        self.assertIn('class="tst-wrapper"', html)

        # All three populated layers rendered with their semantic class.
        self.assertIn("tst-layer user", html)
        self.assertIn("tst-layer application", html)
        self.assertIn("tst-layer data", html)
        # Empty layers omitted (no `tst-layer ai`, etc.).
        self.assertNotIn("tst-layer ai", html)
        self.assertNotIn("tst-layer infra", html)
        self.assertNotIn("tst-layer external", html)

        # Component names made it into boxes.
        self.assertIn("Web App", html)
        self.assertIn("Postgres", html)

        # Sidebar panels rendered.
        self.assertIn("tst-sidebar-panel", html)
        self.assertIn("Monitoring", html)
        self.assertIn("Encryption", html)

    def test_renders_real_sap_plan(self):
        plan = ROOT / "examples" / "sap-o2c-automation" / "layer-plan.yaml"
        r = run([str(BIN / "render.py"), str(plan), "--out", str(self.OUT), "--prefix", "sap"])
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        html = self.OUT.read_text()
        # Everything from the plan landed in the HTML.
        self.assertIn("SAP-O2C-Automation", html)
        self.assertIn("Root Coordinator", html)
        self.assertIn("Gemini API", html)
        self.assertIn("BTP API Mgmt", html)
        # The 6 layers are all present.
        for layer in ["user", "application", "ai", "data", "infra", "external"]:
            self.assertIn(f"sap-layer {layer}", html)

    def _render_with_layout(self, layout: str) -> str:
        """Helper: load valid-plan.yaml, override layout, render, return HTML."""
        import yaml
        plan = yaml.safe_load((FIXTURES / "valid-plan.yaml").read_text())
        plan["layout"] = layout
        tmp = HERE / "_tmp_layout.yaml"
        tmp.write_text(yaml.safe_dump(plan))
        try:
            r = run([str(BIN / "render.py"), str(tmp), "--out", str(self.OUT), "--prefix", "lay"])
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            return self.OUT.read_text()
        finally:
            tmp.unlink()

    def test_single_stack_omits_sidebars_and_wrapper(self):
        html = self._render_with_layout("single-stack")
        # Has the main column with layers.
        self.assertIn('class="lay-main"', html)
        # No sidebar elements (CSS rules may still mention them — that's fine, just unused).
        self.assertNotIn('class="lay-wrapper"', html)
        self.assertNotIn('class="lay-sidebar"', html)
        self.assertNotIn('class="lay-sidebar-panel"', html)
        # Header records the layout.
        self.assertIn("layout: single-stack", html)

    def test_two_column_split_uses_one_sidebar(self):
        html = self._render_with_layout("two-column-split")
        # Wrapper present.
        self.assertIn('class="lay-wrapper"', html)
        # Exactly one populated sidebar (the fixture has both — render warns and uses left).
        self.assertEqual(html.count('class="lay-sidebar-panel"'), 1)
        self.assertIn("Monitoring", html)
        # Right sidebar content (Encryption) was dropped.
        self.assertNotIn("Encryption", html)
        self.assertIn("layout: two-column-split", html)

    def test_pipeline_renders_stages_with_arrows(self):
        html = self._render_with_layout("pipeline")
        # Pipeline-specific structure.
        self.assertIn('class="lay-pipeline"', html)
        self.assertIn('class="lay-stage"', html)
        self.assertIn('class="lay-stage-title"', html)
        self.assertIn('class="lay-arrow"', html)
        self.assertIn("→", html)
        # Three populated layers → three stages → two arrows.
        self.assertEqual(html.count('class="lay-stage"'), 3)
        self.assertEqual(html.count('class="lay-arrow"'), 2)
        # No semantic layer classes in pipeline mode.
        self.assertNotIn("lay-layer", html)
        # Pipeline uses pipeline.md, not the palette file.
        self.assertIn("pipeline (layout-native)", html)

    def test_unknown_layout_falls_back_to_three_column(self):
        import yaml
        plan = yaml.safe_load((FIXTURES / "valid-plan.yaml").read_text())
        plan["layout"] = "made-up-layout"
        tmp = HERE / "_tmp_unknown.yaml"
        tmp.write_text(yaml.safe_dump(plan))
        try:
            r = run([str(BIN / "render.py"), str(tmp), "--out", str(self.OUT), "--prefix", "lay"])
            self.assertEqual(r.returncode, 0)
            self.assertIn("not supported", r.stderr)
            html = self.OUT.read_text()
            # Three-column has the wrapper with main + two sidebars.
            self.assertIn('class="lay-wrapper"', html)
        finally:
            tmp.unlink()


class ExtractPy(unittest.TestCase):
    """Argument-handling smoke tests. No network calls."""

    def test_prints_usage_with_no_args(self):
        r = run([str(BIN / "extract.py")])
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage:", r.stderr)

    def test_help_flag_works(self):
        r = run([str(BIN / "extract.py"), "--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("scope", r.stdout)


if __name__ == "__main__":
    unittest.main()
