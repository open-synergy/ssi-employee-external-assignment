# Create Employee External Assignment Agreement Batch

> **Module:** ssi_employee_external_assignment_agreement_operating_unit\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement_batch`,
> aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field, visible only
for users in the `operating_unit.group_multi_operating_unit` group:

- **Operating Unit**: The operating unit this batch belongs to. Optional — not required
  to Save. Defaults to the user's default operating unit.
