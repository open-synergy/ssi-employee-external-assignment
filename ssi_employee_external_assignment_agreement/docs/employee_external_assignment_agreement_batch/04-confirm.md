# Confirm Employee External Assignment Agreement Batch

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_batch`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreement
> Batches\
> **Actor:** user in group `Employee External Assignment Agreement Batch / User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft** status.
- User has _Can Confirm_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Every agreement linked to this batch that is still in **Draft** status is confirmed
  along with the batch (cascade top-down).
