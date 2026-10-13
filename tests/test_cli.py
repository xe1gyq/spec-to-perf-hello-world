"""Acceptance checks: independent oracle, mode equivalence, input boundaries."""
import subprocess
import unittest

BIN = "./build/matrix-scan"

class AcceptanceTests(unittest.TestCase):
    def test_checksum(self):
        for n in (1, 2, 17, 251):
            for repeats in (1, 3):
                expected = sum(i % 251 for i in range(n * n)) * repeats
                for mode in ("row", "column"):
                    with self.subTest(n=n, repeats=repeats, mode=mode):
                        p = subprocess.run([BIN, mode, str(n), str(repeats)],
                                           capture_output=True, text=True, check=True)
                        fields = dict(item.split("=", 1) for item in p.stdout.split())
                        self.assertEqual(int(fields["checksum"]), expected)
                        self.assertGreaterEqual(float(fields["elapsed_seconds"]), 0)

    def test_invalid_arguments(self):
        for args in ([], ["other"], ["row", "0"], ["row", "-1"],
                     ["row", "4097"], ["row", "2", "0"], ["row", "2", "1001"],
                     ["row", "1.5"], ["row", "2x"], ["row", ""],
                     ["row", "9" * 40], ["row", "2", "1", "extra"]):
            with self.subTest(args=args):
                p = subprocess.run([BIN, *args], capture_output=True, text=True)
                self.assertEqual(p.returncode, 2)
                self.assertIn("Invalid arguments", p.stderr)

    def test_help(self):
        p = subprocess.run([BIN, "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("Usage:", p.stdout)

if __name__ == "__main__":
    unittest.main()
