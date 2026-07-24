# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentType(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Pre-Condition IK disiapkan di sini -- BUKAN lewat klik UI.
        cls.env["employee_external_assignment_type"].create(
            {
                "name": "TOUR EEAT Edit",
                "code": "/",
            }
        )
        cls.env["employee_external_assignment_type"].create(
            {
                "name": "TOUR EEAT Delete",
                "code": "/",
            }
        )
        cls.env["employee_external_assignment_type"].create(
            {
                "name": "TOUR EEAT Deactivate",
                "code": "/",
            }
        )
        cls.env["employee_external_assignment_type"].create(
            {
                "name": "TOUR EEAT Activate",
                "code": "/",
                "active": False,
            }
        )

    def test_create(self):
        """IK: docs/employee_external_assignment_type/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_type_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/employee_external_assignment_type/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_type_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/employee_external_assignment_type/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_type_delete",
            login="admin",
        )

    def test_deactivate(self):
        """IK: docs/employee_external_assignment_type/04-deactivate.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_type_deactivate",
            login="admin",
        )

    def test_activate(self):
        """IK: docs/employee_external_assignment_type/05-activate.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_type_activate",
            login="admin",
        )
