# Reset Document Number — Employee External Assignment Agreement Batch

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_batch`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreement
> Batches\
> **Actor:** user in group `Employee External Assignment Agreement Batch / Validator`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft** status.
- User has _Can Input Manual Document Number_ access right.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to the **On Progress**
  status, according to the sequence template configuration.
