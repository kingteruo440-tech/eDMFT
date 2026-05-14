import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GAUMESH = REPO_ROOT / "src" / "python" / "gaumesh.py"


class GauMeshScriptTests(unittest.TestCase):
    def run_gaumesh(self, *args):
        return subprocess.run(
            [sys.executable, str(GAUMESH), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_script_runs_without_scipy_dependency(self):
        result = self.run_gaumesh(
            "x0=[0]",
            "dx0=[0.4]",
            "fwhm=[1.0]",
            "xmin=-4",
            "xmax=4",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# NPoints=", result.stdout)
        mesh_points = [line for line in result.stdout.splitlines() if not line.startswith("#")]
        self.assertGreater(len(mesh_points), 0)

    def test_zero_lower_bound_is_treated_as_defined(self):
        result = self.run_gaumesh(
            "x0=[0, 1]",
            "dx0=[0.4]",
            "fwhm=[1.0, 1.0]",
            "xmin=0",
            "xmax=4",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("different lengths", result.stderr)
        self.assertNotIn("xmin,xmax have not been defined", result.stderr)


if __name__ == "__main__":
    unittest.main()
