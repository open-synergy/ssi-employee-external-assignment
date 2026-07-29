# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class EmployeeExternalAssignmentAgreementBatch(models.Model):
    """
    Represents an umbrella (framework) contract governing several
    Employee External Assignment Agreements with the same partner, type,
    and period. Its workflow drives the linked agreements top-down: running
    a transition on the batch cascades the same transition to every linked
    agreement still eligible for it.
    """

    _name = "employee_external_assignment_agreement_batch"
    _inherit = [
        "mixin.transaction_terminate",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_date_duration",
        "mixin.transaction_partner",
        "mixin.transaction_pricelist",
        "mixin.many2one_configurator",
    ]
    _description = "Employee External Assignment Agreement Batch"

    # mixin.multiple_approval attributes
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "open_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve",
        "action_reject",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
        "action_recompute_all_fields",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "don_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda r: r._default_date(),
        help="Date of the batch.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        comodel_name="employee_external_assignment_type",
        string="Type",
        required=True,
        help="Type of the external assignment shared by every agreement "
        "linked to this batch.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    title = fields.Char(
        string="Title",
        required=True,
        help="Title of the umbrella contract.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    ref1 = fields.Char(
        string="Reference 1",
        help="First reference for the batch.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    ref2 = fields.Char(
        string="Reference 2",
        help="Second reference for the batch.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Allowed Partners",
        help="Partners allowed to be selected in the Partner field.",
        compute_sudo=True,
        store=False,
        compute="_compute_allowed_partner_ids",
    )
    partner_location_id = fields.Many2one(
        comodel_name="res.partner",
        string="Location",
        help="Location where the job position is based.",
        domain="[('parent_id', '=', partner_id),('type','!=','contact')]",
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    agreement_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement",
        inverse_name="batch_id",
        string="Agreements",
        help="Agreements linked to and driven by this batch.",
    )
    agreement_count = fields.Integer(
        string="# Agreements",
        compute="_compute_agreement_count",
        compute_sudo=True,
        help="Number of agreements linked to this batch.",
    )

    @api.depends("agreement_ids")
    def _compute_agreement_count(self):
        for record in self:
            record.agreement_count = len(record.agreement_ids)

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

    @api.onchange("partner_id")
    def onchange_partner_location_id(self):
        self.partner_location_id = False

    @api.onchange("type_id")
    def onchange_partner_id(self):
        self.partner_id = False  # pylint: disable=W0201

    @api.model
    def _default_date(self):
        return date.today()

    def action_open_agreements(self):
        for record in self.sudo():
            result = record._open_agreements()
        return result

    def _open_agreements(self):
        self.ensure_one()
        return {
            "name": "Employee External Assignment Agreements",
            "type": "ir.actions.act_window",
            "res_model": "employee_external_assignment_agreement",
            "view_mode": "tree,form",
            "domain": [("batch_id", "=", self.id)],
        }

    def _cascade_agreement(self, method_name, allowed_states):
        self.ensure_one()
        children = self.agreement_ids.filtered(lambda a: a.state in allowed_states)
        if not children:
            return
        getattr(
            children.with_context(bypass_policy_check=True, from_batch_cascade=True),
            method_name,
        )()

    @ssi_decorator.post_confirm_action()
    def _10_cascade_confirm_agreement(self):
        self._cascade_agreement("action_confirm", ["draft"])

    @ssi_decorator.post_open_action()
    def _10_cascade_open_agreement(self):
        # Safety net: bring any straggling draft agreements to confirm first,
        # in case they were linked after the batch was already confirmed.
        self._cascade_agreement("action_confirm", ["draft"])
        self._cascade_agreement("action_open", ["confirm"])

    @ssi_decorator.post_done_action()
    def _10_cascade_done_agreement(self):
        self._cascade_agreement("action_done", ["open"])

    @ssi_decorator.post_cancel_action()
    def _10_cascade_cancel_agreement(self):
        self._cascade_agreement(
            "action_cancel", ["draft", "confirm", "open", "terminate"]
        )

    @ssi_decorator.post_terminate_action()
    def _10_cascade_terminate_agreement(self):
        self._cascade_agreement("action_terminate", ["open"])

    @ssi_decorator.post_restart_action()
    def _10_cascade_restart_agreement(self):
        self._cascade_agreement("action_restart", ["cancel", "reject"])

    @ssi_decorator.post_reject_action()
    def _10_cascade_reject_agreement(self):
        """Cascade the batch rejection to agreements still in confirm.

        Runs after the batch itself is rejected via
        ``action_reject_approval``. Only agreements in ``confirm``
        are moved to ``reject``; agreements still in ``draft`` are
        left untouched -- unlike ``_10_cascade_open_agreement``,
        reject has no safety net for stragglers linked after the
        batch was already confirmed.
        """
        self._cascade_agreement("action_reject_from_batch", ["confirm"])

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

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
