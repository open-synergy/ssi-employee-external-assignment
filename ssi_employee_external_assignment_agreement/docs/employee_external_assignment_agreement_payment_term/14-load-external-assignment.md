# Load External Assignments — Employee External Assignment Agreement Payment Term

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement.payment_term`\
> **Menu:** Human Resource > Career Management > External Assignment > Payment Terms\
> **Actor:** user in group `Employee External Assignment Agreement - Payment Term / User`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft** status (the button is only available while in Draft).

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Payment Terms**
   menu.
2. Open the record.
3. Go to the **Included Assignments** tab.
4. Click the **External Assignments** button (refresh icon).

## Post-Condition

- Employee External Assignment records whose **Date Start**/**Date End** fall within the
  Agreement's own **Date Start**/**Date End**, and whose **Partner** matches the
  Agreement's **Partner**, are loaded into the **External Assignments** field, replacing
  any previously loaded assignments.
