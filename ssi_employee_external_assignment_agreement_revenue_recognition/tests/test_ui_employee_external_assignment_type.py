# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentType(HttpSavepointCase):
    """Tour tests for the ``employee_external_assignment_type`` PoB delta."""

    def test_create(self):
        """Run the create delta tour for ``employee_external_assignment_type``.

        IK: docs/employee_external_assignment_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_revenue_recognition_"
            "employee_external_assignment_type_create",
            login="admin",
        )
