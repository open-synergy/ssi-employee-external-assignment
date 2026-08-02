# Approve Employee External Assignment Agreement Batch

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_batch`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreement
> Batches\
> **Actor:** user registered as an approver on the active `approval.template`\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an active approver for the record.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- This model has a single approval level, so approving immediately completes the
  approval process: status changes directly to **On Progress** (no separate "Open" IK
  step — the `confirm -> open` transition runs automatically right after approval).
- As part of that automatic transition, every agreement linked to this batch is driven
  top-down: any agreement still in **Draft** status is confirmed first (safety net),
  then every agreement in **Waiting for Approval** status is opened directly — bypassing
  its own separate approval step.
