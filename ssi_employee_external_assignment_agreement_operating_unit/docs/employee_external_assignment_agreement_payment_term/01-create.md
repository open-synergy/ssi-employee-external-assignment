# Create Employee External Assignment Agreement Payment Term

> **Module:** ssi_employee_external_assignment_agreement_operating_unit\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement.payment_term`,
> aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field, visible only
for users in the `operating_unit.group_multi_operating_unit` group:

- **Operating Unit**: The operating unit this payment term belongs to. Optional — not
  required to Save. Automatically filled from the selected **Agreement**'s operating
  unit once **Agreement** is set, but can still be changed manually afterwards.
