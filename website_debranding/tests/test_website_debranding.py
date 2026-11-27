# Copyright 2026 IT Brasil
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteDebranding(TransactionCase):
    def _render(self):
        return str(
            self.env["ir.ui.view"]._render_template(
                "web.brand_promotion_message",
                values={"_message": "Create a free website", "_utm_medium": "portal"},
            )
        )

    def test_promotion_removed_when_active(self):
        # The post_init_hook disables the view under --test-enable.
        self.env.ref("website_debranding.layout_footer_copyright").active = True
        html = self._render()
        self.assertNotIn("Powered by", html)
        self.assertNotIn("free website", html)

    def test_promotion_shown_when_disabled(self):
        self.env.ref("website_debranding.layout_footer_copyright").active = False
        self.assertIn("Powered by", self._render())
