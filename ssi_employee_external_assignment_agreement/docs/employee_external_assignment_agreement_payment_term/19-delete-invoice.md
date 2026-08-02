# Delete Invoice — Employee External Assignment Agreement Payment Term

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement.payment_term`\
> **Menu:** Human Resource > Career Management > External Assignment > Payment Terms\
> **Actor:** user in group `Employee External Assignment Agreement - Payment Term / User`\
> **Requires:** `18-create-invoice`

## Pre-Condition

- An Invoice is already linked to the record (the button is only available while the
  **Invoice** field is not empty).

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Payment Terms**
   menu.
2. Open the record.
3. Go to the **Invoice** tab.
4. Click the **Delete Invoice** button.

## Post-Condition

- The linked invoice is permanently deleted and the **Invoice** field is cleared. The
  **Create Invoice** button becomes available again in its place.
