# Reject Employee External Assignment Agreement Batch

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an active approver for the record.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
- Every linked agreement that is in **Waiting for Approval** status is cascaded to
  **Rejected** as well.
- Linked agreements still in **Draft** status (added to the batch after it was
  confirmed) are left untouched — they stay in **Draft**.
