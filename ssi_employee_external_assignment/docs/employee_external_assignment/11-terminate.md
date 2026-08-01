# Terminate Employee External Assignment

> **Module:** ssi_employee_external_assignment\
> **Model:** `employee_external_assignment`\
> **Menu:** Human Resource > Career Management > External Assignment > Assignments\
> **Actor:** user in group `Employee External Assignment / User`\
> **State:** `open` → `terminate`\
> **Requires:** `05-approve`

## Pre-Condition

- Record is in **On Progress** status.
- User has _Can Terminate_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Assignments**
   menu.
2. Open the record to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Terminated**.
