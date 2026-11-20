import unittest
from demos.orion.workflow import TransitionError, Workflow


class OrionTests(unittest.TestCase):
    def setUp(self):
        self.workflow = Workflow("SYN-TASK-001", "Analyze a fictional document")
        self.artifact = {"summary": "A normalized synthetic sample document", "test_claims": ["maker self-test"]}

    def test_task_requires_synthetic_id(self):
        with self.assertRaises(ValueError):
            Workflow("REAL-001", "Analyze a fictional document")

    def test_initial_state_and_history(self):
        self.assertEqual(self.workflow.state, "AWAIT_MAKER")
        self.assertEqual(self.workflow.events[0]["event"], "TASK_CREATED")

    def test_no_owner_approval_without_checker(self):
        with self.assertRaises(TransitionError):
            self.workflow.owner_decide(True, "Not allowed")

    def test_maker_result_needs_checker(self):
        self.workflow.submit_maker(self.artifact)
        self.assertEqual(self.workflow.state, "AWAIT_CHECKER")
        with self.assertRaises(TransitionError):
            self.workflow.owner_decide(True, "Not allowed")

    def test_malformed_artifact_rejected(self):
        with self.assertRaises(ValueError):
            self.workflow.submit_maker({"summary": "too short", "test_claims": []})
        self.assertEqual(self.workflow.state, "AWAIT_MAKER")

    def test_maker_cannot_resubmit(self):
        self.workflow.submit_maker(self.artifact)
        with self.assertRaises(TransitionError):
            self.workflow.submit_maker(self.artifact)

    def test_checker_pass_still_requires_owner(self):
        self.workflow.submit_maker(self.artifact)
        self.workflow.review_checker("PASS", "Synthetic contract verified by test")
        self.assertEqual(self.workflow.state, "AWAIT_OWNER")
        self.assertNotEqual(self.workflow.state, "APPROVED")

    def test_checker_fail_blocks_owner(self):
        self.workflow.submit_maker(self.artifact)
        self.workflow.review_checker("NEEDS_FIXES", "Synthetic negative-case failure confirmed")
        with self.assertRaises(TransitionError):
            self.workflow.owner_decide(True, "Not allowed")
        self.assertEqual(self.workflow.state, "REJECTED")

    def test_checker_blocked_state(self):
        self.workflow.submit_maker(self.artifact)
        self.workflow.review_checker("BLOCKED", "Required test evidence was not available")
        self.assertEqual(self.workflow.state, "REJECTED")

    def test_owner_can_approve_only_after_pass(self):
        self.workflow.submit_maker(self.artifact)
        self.workflow.review_checker("PASS", "Independent synthetic check is recorded")
        self.workflow.owner_decide(True, "Explicit owner decision")
        self.assertEqual(self.workflow.state, "APPROVED")
        self.assertFalse(self.workflow.snapshot()["side_effects_executed"])

    def test_owner_can_reject_after_pass(self):
        self.workflow.submit_maker(self.artifact)
        self.workflow.review_checker("PASS", "Independent synthetic check is recorded")
        self.workflow.owner_decide(False, "Not a current priority")
        self.assertEqual(self.workflow.state, "REJECTED")

    def test_stop_is_terminal(self):
        self.workflow.stop("Stop requested by owner")
        with self.assertRaises(TransitionError):
            self.workflow.submit_maker(self.artifact)

    def test_check_evidence_must_be_meaningful(self):
        self.workflow.submit_maker(self.artifact)
        with self.assertRaises(ValueError):
            self.workflow.review_checker("PASS", "ok")
        self.assertEqual(self.workflow.state, "AWAIT_CHECKER")

    def test_event_history_is_append_only(self):
        self.workflow.submit_maker(self.artifact)
        self.workflow.review_checker("PASS", "Independent synthetic check is recorded")
        self.workflow.owner_decide(True, "Explicit owner decision")
        self.assertEqual([e["role"] for e in self.workflow.events],
                         ["system", "maker", "checker", "owner"])


if __name__ == "__main__":
    unittest.main()
