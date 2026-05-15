# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class CreateEmployeeExternalAgreementTerm(models.TransientModel):
    _name = "create_employee_external_agreement_term"
    _description = "Create Employee External Agreement Term"

    agreement_id = fields.Many2one(
        string="Agreement",
        comodel_name="employee_external_assignment_agreement",
        required=False,
        default=lambda self: self._context.get("active_id"),
    )
    duration_id = fields.Many2one(
        string="Duration",
        comodel_name="base.duration",
        required=True,
    )
    num_of_term = fields.Integer(
        string="Number of Terms",
        default=1,
        required=True,
    )

    def action_confirm(self):
        for record in self:
            record._confirm_cancel()

    def _confirm_cancel(self):
        self.ensure_one()
        agreement = self.agreement_id
        agreement.payment_term_ids.unlink()
        date_start = agreement.date_start
        for _ in range(self.num_of_term):
            date_end = self.duration_id.get_duration(date_start)
            # date_end = date_start + relativedelta(months=1, days=-1)
            # raise UserError("%s" % date_end)
            self.env["employee_external_assignment_agreement.payment_term"].create(
                self._prepare_payment_term_vals(date_start, date_end)
            )
            date_start = date_end + relativedelta(days=1)

    def _prepare_payment_term_vals(self, date_start, date_end):
        self.ensure_one()
        return {
            "agreement_id": self.agreement_id.id,
            "date_start": date_start,
            "date_end": date_end,
        }
