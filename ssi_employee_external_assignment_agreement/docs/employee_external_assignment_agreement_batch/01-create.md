# Create Employee External Assignment Agreement Batch

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_batch`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreement
> Batches\
> **Actor:** user in group `Employee External Assignment Agreement Batch / User`\
> **State:** `—` → `draft`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreement
   Batches** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Type**: Select the employee external assignment type shared by every agreement
     linked to this batch. Determines the allowed partners.
   - **Partner**: Select the partner for this batch. Options are filtered based on the
     selected **Type**.
   - **Title**: Enter the batch (umbrella contract) title.
   - **Date**: Defaults to today. Change if needed.
   - **Date Start**: Enter the start date of the batch period.
   - **Date End**: Enter the end date of the batch period.
   - **Currency**: Select the currency used for this batch.
   - **Pricelist**: Select the pricelist. Options are filtered based on the selected
     **Currency**.
4. Click **Save**.

## Post-Condition

- A new Employee External Assignment Agreement Batch record is created in **Draft**
  status. The document number stays **/** until the batch reaches the **On Progress**
  status.
