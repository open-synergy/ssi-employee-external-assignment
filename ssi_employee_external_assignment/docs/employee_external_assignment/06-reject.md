# Reject Employee External Assignment

> **Module:** ssi_employee_external_assignment\
> **Model:** `employee_external_assignment`\
> **Menu:** Human Resource > Career Management > External Assignment > Assignments\
> **Actor:** user registered as an approver on the active `approval.template`\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template.
- User has _Can Reject_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Assignments**
   menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
