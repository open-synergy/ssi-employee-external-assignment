# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class EmployeeExternalAssignmentAgreement(models.Model):
    _name = "employee_external_assignment_agreement"
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
    _description = "Employee External Assignment Agreement"

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
        help="Date of the agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        comodel_name="employee_external_assignment_type",
        string="Type",
        required=True,
        help="Type of the external assignment.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    title = fields.Char(
        string="Title",
        required=True,
        help="Title of the external assignment agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    ref1 = fields.Char(
        string="Reference 1",
        help="First reference for the external assignment agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    ref2 = fields.Char(
        string="Reference 2",
        help="Second reference for the external assignment agreement.",
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
    management_fee_percent = fields.Float(
        string="Management Fee (%)",
        help="Management fee percentage for this agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    detail_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement.detail",
        inverse_name="agreement_id",
        string="Details",
        help="Details of the external assignment agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_salary_rule_ids = fields.Many2many(
        comodel_name="hr.salary_rule",
        string="Allowed Salary Rules",
        help="Salary rules that are allowed to be selected based on the "
        "employee external assignment type configuration.",
        compute="_compute_allowed_salary_rule_ids",
        store=False,
        compute_sudo=True,
    )
    all_salary_rule_ids = fields.Many2many(
        comodel_name="hr.salary_rule",
        string="All Salary Rules",
        help="All salary rules associated with this agreement.",
        compute_sudo=True,
        store=True,
        relation="rel_external_assignment_agreement_2_salary_rule",
        column1="agreement_id",
        column2="salary_rule_id",
        compute="_compute_all_salary_rule_ids",
    )
    allowed_job_ids = fields.Many2many(
        comodel_name="hr.job",
        string="Allowed Job Positions",
        help="Job positions that are allowed to be selected based on the "
        "employee external assignment type configuration.",
        compute="_compute_allowed_job_ids",
        store=False,
        compute_sudo=True,
    )
    all_job_position_ids = fields.Many2many(
        comodel_name="hr.job",
        string="All Job Positions",
        help="All job positions associated with this agreement.",
        compute_sudo=True,
        store=True,
        relation="rel_external_assignment_agreement_2_job_position",
        column1="agreement_id",
        column2="job_position_id",
        compute="_compute_all_job_position_ids",
    )
    payment_term_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement.payment_term",
        inverse_name="agreement_id",
        string="Payment Terms",
        help="Payment terms associated with this agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_other_fee_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Allowed Other Fee Categories",
        help="Other fee categories that are allowed to be selected based on the "
        "employee external assignment type configuration.",
        compute="_compute_allowed_other_fee_category_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_other_fee_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Other Fees",
        help="Other fees that are allowed to be selected based on the "
        "employee external assignment type configuration.",
        compute="_compute_allowed_other_fee_ids",
        store=False,
        compute_sudo=True,
    )
    other_fee_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement.other_fee",
        inverse_name="agreement_id",
        string="Other Fees",
        help="Other fees associated with this agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    variable_fee_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement.variable_fee",
        inverse_name="agreement_id",
        string="Variable Fees",
        help="Variable fees associated with this agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    input_line_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement_input",
        inverse_name="agreement_id",
        string="Input Types",
        help="Input values associated with this agreement.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    assignment_ids = fields.One2many(
        comodel_name="employee_external_assignment",
        inverse_name="agreement_id",
        string="External Assignments",
        help="External assignments associated with this agreement.",
        readonly=True,
    )
    # Financial Accounting configuration
    receivable_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Receivable Account",
        help="Account used for receivables in this agreement.",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        help="Journal used for accounting entries in this agreement.",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    usage_id = fields.Many2one(
        comodel_name="product.usage_type",
        string="Usage",
        help="Usage that determines which account is used when generating "
        "invoices from this agreement's payment terms. Defaulted from "
        "the assignment type, but can be overridden.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    # Cost Accounting Configuration
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=False,
    )
    analytic_group_id = fields.Many2one(
        string="Analytic Group",
        comodel_name="account.analytic.group",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_receivable_account_ids = fields.Many2many(
        comodel_name="account.account",
        string="Allowed Receivable Accounts",
        help="Receivable accounts that are allowed to be selected based on "
        "the employee external assignment type configuration.",
        compute="_compute_allowed_receivable_account_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_journal_ids = fields.Many2many(
        comodel_name="account.journal",
        string="Allowed Journals",
        help="Journals that are allowed to be selected based on the "
        "employee external assignment type configuration.",
        compute="_compute_allowed_journal_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_usage_ids = fields.Many2many(
        comodel_name="product.usage_type",
        string="Allowed Usages",
        help="Usages that are allowed to be selected based on the "
        "employee external assignment type configuration.",
        compute="_compute_allowed_usage_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_analytic_group_ids = fields.Many2many(
        comodel_name="account.analytic.group",
        string="Allowed Analytic Groups",
        help="Analytic groups that are allowed to be selected based on the "
        "employee external assignment type configuration.",
        compute="_compute_allowed_analytic_group_ids",
        store=False,
        compute_sudo=True,
    )
    batch_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement_batch",
        string="# Batch",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Umbrella contract (batch) governing this agreement. When set, "
        "the partner, type, and period are snapshotted from the batch and "
        "the workflow is driven by the batch rather than run independently.",
    )

    @api.depends(
        "detail_ids",
        "detail_ids.compensation_term_ids",
        "detail_ids.compensation_term_ids.rule_id",
    )
    def _compute_all_salary_rule_ids(self):
        for record in self:
            all_salary_rule_ids = self.env["hr.salary_rule"]
            for detail in record.detail_ids:
                all_salary_rule_ids |= detail.compensation_term_ids.mapped("rule_id")
            record.all_salary_rule_ids = all_salary_rule_ids

    @api.depends(
        "detail_ids",
        "detail_ids.job_id",
    )
    def _compute_all_job_position_ids(self):
        for record in self:
            all_job_position_ids = self.env["hr.job"]
            for detail in record.detail_ids:
                all_job_position_ids |= detail.job_id
            record.all_job_position_ids = all_job_position_ids

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
    def _compute_allowed_job_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="hr.job",
                    method_selection=record.type_id.job_selection_method,
                    manual_recordset=record.type_id.job_ids,
                    domain=record.type_id.job_domain,
                    python_code=record.type_id.job_python_code,
                )
            record.allowed_job_ids = result

    @api.depends("type_id")
    def _compute_allowed_salary_rule_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="hr.salary_rule",
                    method_selection=record.type_id.salary_rule_selection_method,
                    manual_recordset=record.type_id.salary_rule_ids,
                    domain=record.type_id.salary_rule_domain,
                    python_code=record.type_id.salary_rule_python_code,
                )
            record.allowed_salary_rule_ids = result

    @api.depends("type_id")
    def _compute_allowed_other_fee_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.category",
                    method_selection=record.type_id.other_fee_category_selection_method,
                    manual_recordset=record.type_id.other_fee_category_ids,
                    domain=record.type_id.other_fee_category_domain,
                    python_code=record.type_id.other_fee_category_python_code,
                )
            record.allowed_other_fee_category_ids = result

    @api.depends("type_id")
    def _compute_allowed_other_fee_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.type_id.other_fee_selection_method,
                    manual_recordset=record.type_id.other_fee_ids,
                    domain=record.type_id.other_fee_domain,
                    python_code=record.type_id.other_fee_python_code,
                )
            record.allowed_other_fee_ids = result

    @api.depends("type_id")
    def _compute_allowed_receivable_account_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.account",
                    method_selection=record.type_id.receivable_account_selection_method,
                    manual_recordset=record.type_id.receivable_account_ids,
                    domain=record.type_id.receivable_account_domain,
                    python_code=record.type_id.receivable_account_python_code,
                )
            record.allowed_receivable_account_ids = result

    @api.depends("type_id")
    def _compute_allowed_journal_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.journal",
                    method_selection=record.type_id.journal_selection_method,
                    manual_recordset=record.type_id.journal_ids,
                    domain=record.type_id.journal_domain,
                    python_code=record.type_id.journal_python_code,
                )
            record.allowed_journal_ids = result

    @api.depends("type_id")
    def _compute_allowed_usage_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.usage_type",
                    method_selection=record.type_id.usage_selection_method,
                    manual_recordset=record.type_id.usage_ids,
                    domain=record.type_id.usage_domain,
                    python_code=record.type_id.usage_python_code,
                )
            record.allowed_usage_ids = result

    @api.depends("type_id")
    def _compute_allowed_analytic_group_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.analytic.group",
                    method_selection=record.type_id.analytic_group_selection_method,
                    manual_recordset=record.type_id.analytic_group_ids,
                    domain=record.type_id.analytic_group_domain,
                    python_code=record.type_id.analytic_group_python_code,
                )
            record.allowed_analytic_group_ids = result

    @api.onchange("partner_id", "batch_id")
    def onchange_partner_location_id(self):
        self.partner_location_id = False
        if self.batch_id:
            self.partner_location_id = self.batch_id.partner_location_id

    @api.onchange("type_id", "batch_id")
    def onchange_partner_id(self):
        self.partner_id = False  # pylint: disable=W0201
        if self.batch_id:
            self.partner_id = self.batch_id.partner_id  # pylint: disable=W0201

    @api.onchange("partner_id", "batch_id")
    def onchange_contact_partner_id(self):
        self.contact_partner_id = False
        if self.batch_id:
            self.contact_partner_id = self.batch_id.contact_partner_id

    @api.onchange("currency_id", "batch_id")
    def onchange_pricelist_id(self):
        self.pricelist_id = False
        if self.batch_id:
            self.pricelist_id = self.batch_id.pricelist_id

    @api.onchange("type_id")
    def onchange_usage_id(self):
        self.usage_id = self.type_id.usage_id

    @api.onchange("batch_id")
    def onchange_type_id(self):
        if self.batch_id:
            self.type_id = self.batch_id.type_id  # pylint: disable=W0201

    @api.onchange("batch_id")
    def onchange_date(self):
        if self.batch_id:
            self.date = self.batch_id.date  # pylint: disable=W0201

    @api.onchange("batch_id")
    def onchange_date_start(self):
        if self.batch_id:
            self.date_start = self.batch_id.date_start  # pylint: disable=W0201

    @api.onchange("batch_id")
    def onchange_date_end(self):
        if self.batch_id:
            self.date_end = self.batch_id.date_end  # pylint: disable=W0201

    @api.onchange("batch_id")
    def onchange_currency_id(self):
        if self.batch_id:
            self.currency_id = self.batch_id.currency_id  # pylint: disable=W0201

    @api.model
    def _default_date(self):
        return date.today()

    @api.constrains("batch_id", "type_id", "partner_id", "date_start", "date_end")
    def _check_batch_agreement_alignment(self):
        for document in self.sudo():
            if not document._check_batch_agreement_alignment_condition():
                error_message = """
Context: Link agreement to batch
Database ID: %s
Problem: Type, partner, or period does not match the linked batch %s
Solution: Align the agreement's type, partner, and period with the batch, \
or unlink the batch
""" % (
                    document.id,
                    document.batch_id.name,
                )
                raise ValidationError(_(error_message))

    def _check_batch_agreement_alignment_condition(self):
        self.ensure_one()
        if not self.batch_id:
            return True
        batch = self.batch_id
        if self.type_id != batch.type_id:
            return False
        if self.partner_id != batch.partner_id:
            return False
        if self.date_start and batch.date_start and self.date_start < batch.date_start:
            return False
        if self.date_end and batch.date_end and self.date_end > batch.date_end:
            return False
        return True

    def _check_not_batch_driven(self):
        self.ensure_one()
        if not self.batch_id:
            return
        if self.env.context.get("from_batch_cascade"):
            return
        batch = self.batch_id.sudo()
        error_message = """
Context: Run workflow transition on agreement
Database ID: %s
Problem: This agreement is governed by batch %s and its workflow cannot run \
independently
Solution: Run the workflow transition from the batch record instead
""" % (
            self.id,
            batch.name,
        )
        raise UserError(_(error_message))

    def action_confirm(self):
        for record in self:
            record._check_not_batch_driven()
        return super().action_confirm()

    def action_approve_approval(self):
        for record in self:
            record._check_not_batch_driven()
        return super().action_approve_approval()

    def action_reject_approval(self):
        for record in self:
            record._check_not_batch_driven()
        return super().action_reject_approval()

    def action_open(self):
        for record in self:
            record._check_not_batch_driven()
        return super().action_open()

    def action_done(self):
        for record in self:
            record._check_not_batch_driven()
        return super().action_done()

    def action_cancel(self, cancel_reason=False):
        for record in self:
            record._check_not_batch_driven()
        return super().action_cancel(cancel_reason)

    def action_terminate(self, terminate_reason=False):
        for record in self:
            record._check_not_batch_driven()
        return super().action_terminate(terminate_reason)

    def action_restart(self):
        for record in self:
            record._check_not_batch_driven()
        return super().action_restart()

    def action_reject_from_batch(self):
        """Reject this agreement as a side effect of its batch reject.

        Exposed as a plain method (no button) -- called only by the
        batch's ``_10_cascade_reject_agreement`` hook when the batch
        itself is rejected via ``action_reject_approval``.
        """
        for record in self.sudo():
            record._reject_from_batch()

    def _reject_from_batch(self):
        """Force this agreement into ``reject`` state from its batch.

        Does not delegate to
        ``mixin.multiple_approval._action_approval()`` because that
        method only records a rejection when ``self.env.user`` is
        listed in the ``approver_user_ids`` of the agreement's own
        active approval -- the batch's approver is not guaranteed to
        also approve every linked agreement, so delegating would
        silently leave the agreement in ``confirm`` while the batch
        moves to ``reject``. Instead, every active approval is
        written ``rejected`` directly (same audit trail as a manual
        reject: ``date`` and ``user_id`` set), then ``state`` is set
        to ``reject``. The pre/post reject runners still fire so glue
        module hooks keep working on this cascade path.

        :raises UserError: if this agreement has no ``batch_id`` --
            this method is exclusive to the batch cascade path.
        """
        self.ensure_one()
        if not self.batch_id:
            error_message = """
Context: Reject agreement from batch cascade
Database ID: %s
Problem: This agreement has no linked batch
Solution: Call action_reject_approval on this agreement directly, \
or link it to a batch first
""" % (
                self.id,
            )
            raise UserError(_(error_message))
        self._run_pre_reject_check()
        self._run_pre_reject_action()
        self.active_approval_ids.write(
            {
                "status": "rejected",
                "date": fields.Datetime.now(),
                "user_id": self.env.user.id,
            }
        )
        self.write({"state": "reject"})
        self._run_post_reject_check()
        self._run_post_reject_action()
        self._notify_reject_action()

    def action_open_payment_terms(self):
        for record in self.sudo():
            result = record._open_payment_term()
        return result

    def _open_payment_term(self):
        self.ensure_one()
        action = self.env.ref(
            "ssi_employee_external_assignment_agreement."
            "employee_external_assignment_agreement_payment_term_action"
        ).read()[0]
        action["domain"] = [("agreement_id", "=", self.id)]
        action["context"] = {
            "default_agreement_id": self.id,
        }
        return action

    @api.model
    def cron_finish_agreement(self):
        today = date.today()
        domain = [
            ("state", "=", "open"),
            ("date_end", "<", today),
            ("batch_id", "=", False),
        ]
        agreements = self.search(domain)
        agreements.with_context(bypass_policy_check=True).action_done()

    @ssi_decorator.post_open_action()
    def _10_create_analytic_account(self):
        self.ensure_one()
        if self.analytic_account_id:
            self._update_analytic_account()
        else:
            AA = self.env["account.analytic.account"]  # pylint: disable=C0103
            aa = AA.create(self._prepare_analytic_account())
            self.write(
                {
                    "analytic_account_id": aa.id,
                }
            )

    def _update_analytic_account(self):
        self.ensure_one()
        self.analytic_account_id.write(self._prepare_update_analytic_account())

    def _prepare_update_analytic_account(self):
        self.ensure_one()
        group_id = self.analytic_group_id and self.analytic_group_id.id or False
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,  # pylint: disable=E1101
            "group_id": group_id,
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

    def _prepare_analytic_account(self):
        self.ensure_one()
        group_id = self.analytic_group_id and self.analytic_group_id.id or False
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,  # pylint: disable=E1101
            "group_id": group_id,
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

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
