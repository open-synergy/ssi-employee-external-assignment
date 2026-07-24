# Approve Employee External Assignment Agreement Payment Term

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an active approver for the record.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Payment Terms**
   menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- This model has a single approval level, so approving immediately completes the
  approval process: status changes directly to **Done** (no separate "Finish" IK step --
  the `confirm -> done` transition runs automatically right after approval).
