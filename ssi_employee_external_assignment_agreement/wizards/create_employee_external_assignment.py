# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CreateEmployeeExternalAssignment(models.TransientModel):
    """Wizard that creates one External Assignment per selected employee.

    Launched from an Employee External Assignment Agreement in Open
    state. The employee choices are restricted to the job positions
    listed on the agreement and to the employee configurator of the
    agreement type, excluding employees who already have an active
    assignment on that same agreement.
    """

    _name = "create_employee_external_assignment"
    _description = "Create Employee External Assignment"

    agreement_id = fields.Many2one(
        string="Agreement",
        comodel_name="employee_external_assignment_agreement",
        required=True,
        ondelete="cascade",
        default=lambda self: self._context.get("active_id"),
        help="Agreement this wizard was launched from. New assignments "
        "are linked to this agreement.",
    )
    allowed_employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        string="Allowed Employees",
        relation="create_employee_external_assignment_allowed_rel",
        column1="wizard_id",
        column2="employee_id",
        compute="_compute_allowed_employee_ids",
        store=False,
        compute_sudo=True,
        help="Employees eligible for a new assignment: their job position "
        "is one of the agreement's job positions, they pass the employee "
        "configuration of the agreement type, and they do not already "
        "have an active assignment on this agreement.",
    )
    employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        string="Employees",
        relation="create_employee_external_assignment_employee_rel",
        column1="wizard_id",
        column2="employee_id",
        required=True,
        help="Employees to create a new external assignment for.",
    )

    @api.depends("agreement_id", "agreement_id.type_id")
    def _compute_allowed_employee_ids(self):
        """Restrict employee choices to eligible employees.

        An employee is allowed when the job position is one of the
        agreement's job positions and the employee passes the employee
        configurator of the agreement type (selection method, manual
        list, domain, or Python code). Python code is evaluated with
        ``document`` set to the agreement. An agreement without a type
        adds no type restriction.

        Employees who already have an active assignment (state not in
        ``cancel``, ``terminate``, or ``reject``) on the same agreement
        are excluded, so they cannot be assigned twice.
        """
        for record in self:
            allowed = self.env["hr.employee"]
            if record.agreement_id:
                candidate_employees = self.env["hr.employee"].search(
                    [
                        (
                            "job_id",
                            "in",
                            record.agreement_id.all_job_position_ids.ids,
                        )
                    ]
                )
                existing_assignments = self.env["employee_external_assignment"].search(
                    [
                        ("agreement_id", "=", record.agreement_id.id),
                        ("state", "not in", ["cancel", "terminate", "reject"]),
                    ]
                )
                allowed = candidate_employees - existing_assignments.mapped(
                    "employee_id"
                )
                type_employees = record._get_type_employees()
                if type_employees is not None:
                    allowed &= type_employees
            record.allowed_employee_ids = allowed

    def _get_type_employees(self):
        """Get the employees allowed by the agreement type configurator.

        :return: ``hr.employee`` recordset allowed by the type, or
            ``None`` when the agreement has no type (no restriction)
        """
        self.ensure_one()
        agreement = self.agreement_id
        assignment_type = agreement.type_id
        if not assignment_type:
            return None
        result = agreement._m2o_configurator_get_filter(
            object_name="hr.employee",
            method_selection=assignment_type.employee_selection_method,
            manual_recordset=assignment_type.employee_ids,
            domain=assignment_type.employee_domain,
            python_code=assignment_type.employee_python_code,
        )
        return result or self.env["hr.employee"]

    def action_create_assignment(self):
        """Create the selected employees' assignments and open the list.

        :return: an ``ir.actions.act_window`` dict limited to the
            assignments just created
        """
        for record in self.sudo():
            result = record._create_assignment()
        return result

    def _create_assignment(self):
        """Create one ``employee_external_assignment`` per employee row.

        Refuses to run unless the linked agreement is in Open state.

        :return: an ``ir.actions.act_window`` dict limited to the
            assignments created by this run
        """
        self.ensure_one()
        if self.agreement_id.state != "open":
            error_message = """
Context: Create Employee External Assignment
Database ID: %s
Problem: Agreement %s is not in Open state
Solution: Move the agreement to Open state before creating assignments
""" % (
                self.agreement_id.id,
                self.agreement_id.name,
            )
            raise UserError(_(error_message))

        Assignment = self.env["employee_external_assignment"]  # noqa: N806
        created = Assignment
        for employee in self.employee_ids:
            created |= Assignment.create(self._prepare_assignment_vals(employee))
        return self._open_created_assignment(created)

    def _prepare_assignment_vals(self, employee):
        """Build the ``employee_external_assignment`` values for an employee.

        Extension point: override in a glue module (e.g. Operating Unit)
        to add fields without touching the creation flow.

        :param employee: the ``hr.employee`` record to create the
            assignment for
        :return: dict of ``employee_external_assignment`` values
        """
        self.ensure_one()
        agreement = self.agreement_id
        return {
            "agreement_id": agreement.id,
            "type_id": agreement.type_id.id,
            "partner_id": agreement.partner_id.id,
            "partner_location_id": agreement.partner_location_id.id,
            "date": agreement.date,
            "date_start": agreement.date_start,
            "date_end": agreement.date_end,
            "employee_id": employee.id,
            "job_id": employee.job_id.id,
            "department_id": employee.department_id.id,
            "manager_id": employee.parent_id.id,
        }

    def _open_created_assignment(self, assignments):
        """Build the window action listing the newly created assignments.

        :param assignments: the ``employee_external_assignment``
            recordset created by this run
        :return: an ``ir.actions.act_window`` dict limited to
            ``assignments``
        """
        self.ensure_one()
        action = self.env.ref(
            "ssi_employee_external_assignment.employee_external_assignment_action"
        ).read()[0]
        action["domain"] = [("id", "in", assignments.ids)]
        return action
