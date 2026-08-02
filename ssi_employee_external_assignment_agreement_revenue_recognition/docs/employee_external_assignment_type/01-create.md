# Create Employee External Assignment Type

> **Module:** ssi_employee_external_assignment_agreement_revenue_recognition\
> **Extends:** ssi_employee_external_assignment — model `employee_external_assignment_type`,
> aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field, on a new
**Revenue Recognition** tab:

- **PoB Product**: The service product used as the `product_id` when a Performance
  Obligation (PoB) is created from an agreement detail, other fee, or variable fee line
  of this type. Domain is restricted to service-type products (`type = "service"`).
  Optional at create — not required to Save — but must be filled **before** the **Create
  PoB** button succeeds on an agreement of this type (see
  `employee_external_assignment_agreement/01-create`,
  `Inline Actions: action_create_pob`); without it, Create PoB fails with an error.
