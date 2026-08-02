# Terminate Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreements\
> **Actor:** user in group `Employee External Assignment Agreement / User`\
> **State:** `open` → `terminate`\
> **Requires:** `05-approve`

## Pre-Condition

- Record is in **On Progress** status.
- Record is not linked to a batch.
- User has _Can Terminate_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreements**
   menu.
2. Open the record to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Terminated**.
