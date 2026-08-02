# Create Assignment — Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement_operating_unit\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement`,
> aksi `15-create-assignment`

## Additional Fields

When this module is installed, the **Create Assignment** wizard gains one field, shown
right after the **Agreement** field:

- **Operating Unit**: The operating unit of the agreement the wizard was launched from.
  Read-only, informational only — it always mirrors the agreement's Operating Unit and
  cannot be changed here. Every assignment the wizard creates automatically inherits
  this operating unit. The **Employees** offered by the wizard are also narrowed to
  employees belonging to this same operating unit when the agreement has one set.
