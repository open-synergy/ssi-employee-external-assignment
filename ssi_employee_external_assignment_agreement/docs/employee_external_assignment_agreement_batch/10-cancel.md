# Cancel Employee External Assignment Agreement Batch

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_batch`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreement
> Batches\
> **Actor:** user in group `Employee External Assignment Agreement Batch / Validator`\
> **State:** `draft`/`open`/`done`/`terminate` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft**, **On Progress**, **Done**, or **Terminated** status (cancel is
  not available while **Waiting for Approval**).
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Cancelled**.
- Every agreement linked to this batch that is still in **Draft**, **Waiting for
  Approval**, **On Progress**, or **Terminated** status is cancelled along with the
  batch (cascade top-down).
