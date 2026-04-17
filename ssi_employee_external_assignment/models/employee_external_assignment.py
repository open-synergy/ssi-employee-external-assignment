# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class EmployeeExternalAssignment(models.Model):
    _name = "employee_external_assignment"
    _description = "Employee External Assignment"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.employee_document",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
    ]

    # mixin.multiple_approval attributes
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve",
        "action_reject",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
        "action_recompute_all_fields",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    # E.11: insert form elements into view
    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    # E.12: provide additional policy fields
    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "restart_ok",
            "reject_ok",
            "manual_number_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res

    type_id = fields.Many2one(
        comodel_name="employee_external_assignment_type",
        string="Type",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Type of the employee external assignment which will "
        "determine the allowed employees and partners.",
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda r: r._default_date(),
        help="Date of the employee external assignment.",
    )
    allowed_employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        string="Allowed Employees",
        compute="_compute_allowed_employee_ids",
        store=False,
        compute_sudo=False,
        help="Employees that are allowed to be selected based on the "
        "employee external assignment type configuration.",
    )
    allowed_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Allowed Partners",
        compute="_compute_allowed_partner_ids",
        store=False,
        compute_sudo=False,
        help="Partners that are allowed to be selected based on the "
        "employee external assignment type configuration.",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Partner of the employee external assignment. The available "
        "options are filtered based on the employee external assignment "
        "type configuration.",
    )
    partner_location_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner Location",
        domain="[('parent_id', '=', partner_id),('type','!=','contact')]",
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Location of the partner for the employee external assignment.",
    )

    def _default_date(self):
        return date.today()

    @api.onchange("partner_id")
    def onchange_partner_location_id(self):
        self.partner_location_id = False

    @api.onchange("type_id")
    def onchange_partner_id(self):
        self.partner_id = False

    @api.onchange("type_id")
    def onchange_employee_id(self):
        self.employee_id = False  # pylint: disable=attribute-defined-outside-init

    @api.depends("type_id")
    def _compute_allowed_partner_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.partner",
                    method_selection=record.type_id.partner_selection_method,
                    manual_recordset=record.type_id.partner_ids,
                    domain=record.type_id.partner_domain,
                    python_code=record.type_id.partner_python_code,
                )
            record.allowed_partner_ids = result

    @api.depends("type_id")
    def _compute_allowed_employee_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="hr.employee",
                    method_selection=record.type_id.employee_selection_method,
                    manual_recordset=record.type_id.employee_ids,
                    domain=record.type_id.employee_domain,
                    python_code=record.type_id.employee_python_code,
                )
            record.allowed_employee_ids = result
