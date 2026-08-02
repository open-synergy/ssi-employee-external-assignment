# Approve Employee External Assignment Agreement Payment Term

> **Module:** ssi_employee_external_assignment_agreement_revenue_recognition\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement.payment_term`,
> aksi `05-approve`

## Post-Condition

- When the payment term reaches **Done** status, a Performance Obligation Acceptance is
  automatically created for each agreement detail line that has a PoB and a payslip line
  matching its compensation rule.
