# Create Employee External Assignment

> **Module:** ssi_employee_external_assignment_operating_unit\
> **Extends:** ssi_employee_external_assignment — model `employee_external_assignment`, aksi
> `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field, visible only
for users in the `operating_unit.group_multi_operating_unit` group:

- **Operating Unit**: The operating unit associated with this assignment. Optional — not
  required to Save. Once filled, the choices for the **Employee** field on the same form
  are automatically narrowed to employees belonging to the same operating unit.
