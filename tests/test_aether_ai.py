import unittest

from ai_core_import import load_ai_module


class TestAetherAI(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_ai_module()

    def test_install_maps_to_package_manager(self) -> None:
        ai = self.mod.AetherAI()
        ai.package_manager = "apt"
        proposal = ai.propose_action("install vscode")
        self.assertIn("sudo apt install -y vscode", proposal.proposed_action)
        self.assertTrue(proposal.requires_confirmation)

    def test_remove_has_high_risk(self) -> None:
        ai = self.mod.AetherAI()
        proposal = ai.propose_action("remove docker")
        self.assertEqual("high", proposal.risk_level)
        self.assertTrue(proposal.requires_confirmation)

    def test_unknown_action_is_not_auto_execute(self) -> None:
        ai = self.mod.AetherAI()
        ai.api_key = None
        proposal = ai.propose_action("do something unexpected")
        self.assertIn("No direct command generated", proposal.proposed_action)

    def test_flatpak_install_request_maps_to_flatpak(self) -> None:
        ai = self.mod.AetherAI()
        proposal = ai.propose_action("install flatpak org.mozilla.firefox")
        self.assertEqual("flatpak install -y flathub org.mozilla.firefox", proposal.proposed_action)
        self.assertEqual("medium", proposal.risk_level)

    def test_unsafe_ai_generated_command_is_rejected(self) -> None:
        ai = self.mod.AetherAI(api_key="dummy")
        ai.gemini.generate = lambda _: "rm -rf /"
        proposal = ai.propose_action("clean everything")
        self.assertEqual("high", proposal.risk_level)
        self.assertIn("rejected by safety policy", proposal.proposed_action)


if __name__ == "__main__":
    unittest.main()
