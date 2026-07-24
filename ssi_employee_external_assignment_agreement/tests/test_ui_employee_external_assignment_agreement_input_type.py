# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentAgreementInputType(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Pre-Condition: the "Agreement Input Types" menu is gated by the
        # employee_external_assignment_agreement_input_type_configurator_group
        # group. Without it, the tour fails at the FIRST step -- the menu is
        # never rendered for the "admin" login used by start_tour below.
        cls.env.ref(
            "ssi_employee_external_assignment_agreement"
            ".employee_external_assignment_agreement_input_type_configurator_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

        # Pre-Condition IK disiapkan di sini -- BUKAN lewat klik UI.
        cls.env["employee_external_assignment_agreement_input_type"].create(
            {
                "name": "TOUR EEAAIT Edit",
                "code": "/",
            }
        )
        cls.env["employee_external_assignment_agreement_input_type"].create(
            {
                "name": "TOUR EEAAIT Delete",
                "code": "/",
            }
        )
        cls.env["employee_external_assignment_agreement_input_type"].create(
            {
                "name": "TOUR EEAAIT Deactivate",
                "code": "/",
            }
        )
        cls.env["employee_external_assignment_agreement_input_type"].create(
            {
                "name": "TOUR EEAAIT Activate",
                "code": "/",
                "active": False,
            }
        )

    def test_create(self):
        """IK: docs/employee_external_assignment_agreement_input_type/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_input_type_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/employee_external_assignment_agreement_input_type/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_input_type_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/employee_external_assignment_agreement_input_type/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_input_type_delete",
            login="admin",
        )

    def test_deactivate(self):
        """IK: docs/employee_external_assignment_agreement_input_type/
        04-deactivate.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_input_type_deactivate",
            login="admin",
        )

    def test_activate(self):
        """IK: docs/employee_external_assignment_agreement_input_type/05-activate.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_input_type_activate",
            login="admin",
        )
