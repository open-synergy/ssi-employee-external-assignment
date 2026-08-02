# Create Invoice — Employee External Assignment Agreement Payment Term

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement.payment_term`\
> **Menu:** Human Resource > Career Management > External Assignment > Payment Terms\
> **Actor:** user in group `Employee External Assignment Agreement - Payment Term / User`\
> **Requires:** `01-create`

## Pre-Condition

- No Invoice is linked to the record yet (the button is only available while the
  **Invoice** field is empty).

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Payment Terms**
   menu.
2. Open the record.
3. Go to the **Invoice** tab.
4. Click the **Create Invoice** button.

## Post-Condition

- A new customer invoice is created from the Agreement and linked to the record: the
  **Invoice** field now shows the created invoice, invoice lines are generated from the
  **Payment Term Rules** and from the Agreement's other/variable fees, and the **Delete
  Invoice** button becomes available in its place.
