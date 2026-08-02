# Restart Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreements\
> **Actor:** user in group `Employee External Assignment Agreement / Validator`\
> **State:** `cancel`/`reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- Record is in **Cancelled** or **Rejected** status (restart is not available from
  **Terminated** — a terminated agreement cannot be restarted).
- Record is not linked to a batch.
- User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreements**
   menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
