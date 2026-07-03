# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.ssi_decorator import ssi_decorator


class EmployeeExternalAssignmentAgreementPaymentTerm(models.Model):
    _name = "employee_external_assignment_agreement.payment_term"
    _inherit = [
        "employee_external_assignment_agreement.payment_term",
    ]

    @ssi_decorator.post_done_action()
    def _10_create_pob_acceptance(self):
        """Create a PoB acceptance for each agreement detail when payment term is done."""
        self.ensure_one()
        agreement = self.agreement_id
        PoA = self.env["performance_obligation_acceptance"]
        for detail in agreement.detail_ids:
            pob = detail.pob_id
            if not pob:
                continue
            compensation_rules = detail.compensation_term_ids.mapped("rule_id")
            if not compensation_rules:
                continue
            payslip_lines = self.payslip_detail_ids.filtered(
                lambda l, rules=compensation_rules: l.rule_id in rules
            )
            if not payslip_lines:
                continue
            PoA.create(self._prepare_pob_acceptance_data(pob, payslip_lines))

    def _prepare_pob_acceptance_data(self, pob, payslip_lines):
        self.ensure_one()
        return {
            "performance_obligation_id": pob.id,
            "partner_id": self.agreement_id.partner_id.id,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "date": self.date_end,
            "payslip_line_ids": [(6, 0, payslip_lines.ids)],
        }
