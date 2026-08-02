# Cancel Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreements\
> **Actor:** user in group `Employee External Assignment Agreement / Validator`\
> **State:** `draft`/`open`/`done`/`terminate` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft**, **On Progress**, **Done**, or **Terminated** status (cancel is
  not available while **Waiting for Approval**).
- Record is not linked to a batch.
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreements**
   menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Cancelled**.
