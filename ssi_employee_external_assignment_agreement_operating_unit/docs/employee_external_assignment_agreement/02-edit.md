# Edit Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement_operating_unit\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement`,
> aksi `02-edit`

## Modified Validation

- Save fails if the agreement's **Operating Unit** differs from the operating unit of
  the batch it is linked to (**# Batch** field), whenever the agreement is linked to a
  batch that itself has an Operating Unit set. This check runs on every write, not only
  when the record is first created.
