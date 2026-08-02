# Terminate Employee External Assignment Agreement Batch

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_batch`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreement
> Batches\
> **Actor:** user in group `Employee External Assignment Agreement Batch / User`\
> **State:** `open` → `terminate`\
> **Requires:** `05-approve`

## Pre-Condition

- Record is in **On Progress** status.
- User has _Can Terminate_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Open the record to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Terminated**.
- Every agreement linked to this batch that is still in **On Progress** status is
  terminated along with the batch (cascade top-down).
