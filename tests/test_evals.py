import copy
import importlib.util
import json
import unittest

from support import ROOT

spec = importlib.util.spec_from_file_location("eval_grade", ROOT / "evals/grade.py")
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


class EvalContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "evals/scenarios.json").read_text())
        self.cases = grader.validate(self.data)
        # Synthetic records exercise the grader, not a model or routing behavior.
        self.records = [{"id": c["id"], "skills": c["skills"], "observed": c["required"],
                         "notes": "Synthetic grader unit-test record, no live agent."}
                        for c in self.cases]

    def test_fixture_contract(self):
        self.assertGreaterEqual(sum(c["category"] == "negative" for c in self.cases), 6)
        self.assertTrue(all(r["pass"] for r in grader.grade(self.cases, self.records)))

    def test_false_positive_and_forbidden_actions_fail(self):
        records = copy.deepcopy(self.records)
        negative = next(c for c in self.cases if c["category"] == "negative")
        observed = next(r for r in records if r["id"] == negative["id"])
        observed["skills"] = ["research-postgresql"]
        observed["observed"].append("core_workflow")
        results = grader.grade(self.cases, records)
        self.assertFalse(next(r for r in results if r["id"] == negative["id"])["pass"])
        records = copy.deepcopy(self.records)
        observed = next(r for r in records if r["id"] == "unapproved-post")
        observed["observed"].append("send_email")
        self.assertFalse(next(r for r in grader.grade(self.cases, records)
                              if r["id"] == "unapproved-post")["pass"])

    def test_missing_validation_and_bad_observations_fail(self):
        records = copy.deepcopy(self.records)
        records[0]["observed"] = []
        self.assertFalse(grader.grade(self.cases, records)[0]["pass"])
        for bad in (self.records[:-1], self.records + [self.records[0]], {}):
            with self.assertRaises(ValueError):
                grader.grade(self.cases, bad)
        malformed = copy.deepcopy(self.data)
        malformed["scenarios"][0]["skills"] = ["missing-skill"]
        with self.assertRaises(ValueError):
            grader.validate(malformed)


if __name__ == "__main__":
    unittest.main()
