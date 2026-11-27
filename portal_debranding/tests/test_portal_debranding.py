"""Portal debranding tests.

Validates that this module removes Odoo branding from portal pages.
"""

# Copyright 2024 level4 (https://level4.es)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests import common


class TestPortalOdooDebranding(common.TransactionCase):
    def test_brand_promotion_hidden(self):
        """web.brand_promotion should render nothing after debranding.

        The view sets t-if="False" on the .o_brand_promotion container,
        so the whole block must be skipped at render time.
        """
        html = self.env["ir.ui.view"]._render_template("web.brand_promotion", values={})
        self.assertEqual(html.strip(), "", "Brand promotion block should be removed")

    def test_portal_record_sidebar_no_powered_by(self):
        """The 'Powered by Odoo' notice in portal sidebar must be removed."""
        html = self.env["ir.ui.view"]._render_template(
            "portal.portal_record_sidebar", values={"classes": ""}
        )
        self.assertNotIn("Powered by", html)
        self.assertNotIn("utm_medium=portal", html)
        self.assertNotIn("www.odoo.com", html)

    def test_login_footer_without_odoo_link(self):
        """The login footer hides the Odoo link and its separator, and the
        footer itself when the database manager is disabled.

        Applied on the web arch only: website replaces the whole login layout.
        """
        View = self.env["ir.ui.view"]
        base = self.env.ref("web.login_layout")
        ours = self.env.ref("portal_debranding.login_debranding_hide_powered_by")
        arch = View.apply_inheritance_specs(
            etree.fromstring(base.arch), etree.fromstring(ours.arch)
        )
        manager = arch.xpath("//a[@href='/web/database/manager']")[0]
        self.assertNotIn("border-end", manager.get("class") or "")
        odoo_link = arch.xpath("//a[contains(@href, 'utm_medium=auth')]")[0]
        self.assertEqual(odoo_link.get("t-if"), "False")
        footer = manager.getparent().getparent()
        self.assertEqual(
            footer.get("t-if"), "not disable_footer and not disable_database_manager"
        )
