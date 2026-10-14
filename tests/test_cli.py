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

    def test_blocked_edges(self):
        for n in (1, 4, 31, 32, 33, 65, 4096):
            for repeats in ((1,) if n == 4096 else (1, 3)):
                # Closed-form oracle avoids reproducing the traversal algorithm.
                count = n * n
                cycles, remainder = divmod(count, 251)
                expected = (cycles * sum(range(251)) + sum(range(remainder))) * repeats
                p = subprocess.run([BIN, "blocked", str(n), str(repeats)],
                                   capture_output=True, text=True)
                with self.subTest(n=n, repeats=repeats):
                    self.assertEqual(p.returncode, 0, p.stderr)
                    fields = dict(item.split("=", 1) for item in p.stdout.split())
                    self.assertEqual(int(fields["checksum"]), expected)
                    self.assertEqual(fields["mode"], "blocked")
                    self.assertGreaterEqual(float(fields["elapsed_seconds"]), 0)

    def test_blocked_defaults(self):
        for args, n in ((["blocked"], 2048), (["blocked", "33"], 33)):
            p = subprocess.run([BIN, *args], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            fields = dict(item.split("=", 1) for item in p.stdout.split())
            self.assertEqual(int(fields["size"]), n)
            self.assertEqual(int(fields["repeats"]), 20)
            cycles, remainder = divmod(n * n, 251)
            self.assertEqual(int(fields["checksum"]),
                             (cycles * sum(range(251)) + sum(range(remainder))) * 20)

    def test_blocked_invalid_arguments(self):
        for tail in (["0"], ["-1"], ["4097"], ["x"], [""], ["9" * 40],
                     ["2", "0"], ["2", "-1"], ["2", "1001"],
                     ["2", "1.5"], ["2", "9" * 40], ["2", "1", "extra"]):
            with self.subTest(tail=tail):
                p = subprocess.run([BIN, "blocked", *tail], capture_output=True, text=True)
                self.assertEqual(p.returncode, 2)
                self.assertIn("Invalid arguments", p.stderr)

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
        for mode in ("row", "column", "blocked"):
            self.assertIn(mode, p.stdout)

if __name__ == "__main__":
    unittest.main()
