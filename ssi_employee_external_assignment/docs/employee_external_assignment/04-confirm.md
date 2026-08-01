# Confirm Employee External Assignment

> **Module:** ssi_employee_external_assignment\
> **Model:** `employee_external_assignment`\
> **Menu:** Human Resource > Career Management > External Assignment > Assignments\
> **Actor:** user in group `Employee External Assignment / User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft** status.
- User has _Can Confirm_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Assignments**
   menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
