# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignment(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Pre-Condition IK disiapkan di sini -- BUKAN lewat klik UI.
        # employee_selection_method/partner_selection_method default to
        # "domain" with domain "[]", so every employee/partner is allowed.
        cls.assignment_type = cls.env["employee_external_assignment_type"].create(
            {
                "name": "TOUR EEA Type",
                "code": "/",
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "TOUR EEA Partner"})
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR EEA Cancel Reason",
                "code": "TOUR-EEA-CANCEL",
                "global_use": True,
            }
        )
        cls.terminate_reason = cls.env["base.terminate_reason"].create(
            {
                "name": "TOUR EEA Terminate Reason",
                "code": "TOUR-EEA-TERMINATE",
                "global_use": True,
            }
        )

        def _create_assignment(employee_name):
            employee = cls.env["hr.employee"].create({"name": employee_name})
            return cls.env["employee_external_assignment"].create(
                {
                    "type_id": cls.assignment_type.id,
                    "employee_id": employee.id,
                    "partner_id": cls.partner.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )

        # 01-create.md -- no pre-existing record; the create tour creates a
        # new one, but it still needs an employee to pick from the list.
        cls.env["hr.employee"].create({"name": "TOUR EEA Create Employee"})

        # 02-edit.md -- Draft record to edit.
        cls.assignment_edit = _create_assignment("TOUR EEA Edit Employee")

        # 03-delete.md -- Draft record to delete.
        cls.assignment_delete = _create_assignment("TOUR EEA Delete Employee")

        # 04-confirm.md -- Draft record to confirm.
        cls.assignment_confirm = _create_assignment("TOUR EEA Confirm Employee")

        # 05-approve.md -- Waiting for Approval record to approve.
        cls.assignment_approve = _create_assignment("TOUR EEA Approve Employee")
        cls.assignment_approve.action_confirm()

        # 06-reject.md -- Waiting for Approval record to reject.
        cls.assignment_reject = _create_assignment("TOUR EEA Reject Employee")
        cls.assignment_reject.action_confirm()

        # 10-cancel.md -- On Progress record to cancel.
        cls.assignment_cancel = _create_assignment("TOUR EEA Cancel Employee")
        cls.assignment_cancel.action_confirm()
        cls.assignment_cancel.action_approve_approval()

        # 11-terminate.md -- On Progress record to terminate.
        cls.assignment_terminate = _create_assignment("TOUR EEA Terminate Employee")
        cls.assignment_terminate.action_confirm()
        cls.assignment_terminate.action_approve_approval()

        # 12-restart.md -- Cancelled record to restart.
        cls.assignment_restart = _create_assignment("TOUR EEA Restart Employee")
        cls.assignment_restart.action_confirm()
        cls.assignment_restart.action_cancel(cls.cancel_reason)

        # 13-reset-number.md -- Draft record with a manually-set document
        # number (the "name" field is editable in Draft status).
        cls.assignment_reset_number = _create_assignment(
            "TOUR EEA Reset Number Employee"
        )
        cls.assignment_reset_number.write({"name": "TOUR-EEA-MANUAL-001"})

    def test_create(self):
        """IK: docs/employee_external_assignment/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/employee_external_assignment/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/employee_external_assignment/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_delete",
            login="admin",
        )

    def test_confirm(self):
        """IK: docs/employee_external_assignment/04-confirm.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_confirm",
            login="admin",
        )

    def test_approve(self):
        """IK: docs/employee_external_assignment/05-approve.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_approve",
            login="admin",
        )

    def test_reject(self):
        """IK: docs/employee_external_assignment/06-reject.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_reject",
            login="admin",
        )

    def test_cancel(self):
        """IK: docs/employee_external_assignment/10-cancel.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_cancel",
            login="admin",
        )

    def test_terminate(self):
        """IK: docs/employee_external_assignment/11-terminate.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_terminate",
            login="admin",
        )

    def test_restart(self):
        """IK: docs/employee_external_assignment/12-restart.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_restart",
            login="admin",
        )

    def test_reset_number(self):
        """IK: docs/employee_external_assignment/13-reset-number.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_employee_external_assignment_reset_number",
            login="admin",
        )
