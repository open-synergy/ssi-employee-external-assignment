# Reject Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreements\
> **Actor:** user registered as an approver on the active `approval.template`\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- Record is in **Waiting for Approval** status.
- Record is not linked to a batch (field **Batch** is empty). An agreement linked to a
  batch cannot be rejected on its own record — its workflow, including reject, only runs
  through the batch. Reject it by rejecting the batch instead (see the Agreement Batch
  **Reject** instruction), which cascades the rejection down to this agreement.
- User is registered as an active approver for the record.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreements**
   menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
