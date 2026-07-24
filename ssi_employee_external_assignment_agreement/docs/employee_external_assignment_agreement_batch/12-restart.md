# Restart Employee External Assignment Agreement Batch

## Pre-Condition

- Record is in **Cancelled** or **Rejected** status.
- User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- Every agreement linked to this batch that is still in **Cancelled** or **Rejected**
  status is restarted along with the batch (cascade top-down).
