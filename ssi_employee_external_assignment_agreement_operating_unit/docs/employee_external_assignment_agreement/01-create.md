# Create Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement_operating_unit\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement`,
> aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field, visible only
for users in the `operating_unit.group_multi_operating_unit` group:

- **Operating Unit**: The operating unit this agreement belongs to. Optional — not
  required to Save. If the **# Batch** field is filled, this field is automatically set
  to the batch's operating unit and becomes read-only. If **# Batch** is left empty
  (standalone agreement), this field can be filled freely and defaults to the user's
  default operating unit.

## Modified Validation

- Save (create or write) fails if the agreement's **Operating Unit** differs from the
  operating unit of the batch it is linked to (**# Batch** field), whenever the
  agreement is linked to a batch that itself has an Operating Unit set. This check runs
  every time the record is created or written, not only at the moment **# Batch** is
  first selected.
