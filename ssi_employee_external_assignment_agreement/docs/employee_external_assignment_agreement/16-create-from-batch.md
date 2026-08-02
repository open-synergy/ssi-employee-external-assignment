# Create Employee External Assignment Agreement from Batch

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreements\
> **Actor:** user in group `Employee External Assignment Agreement / User`\
> **State:** `—` → `draft`\
> **Requires:** `ssi_employee_external_assignment_agreement/employee_external_assignment_agreement_batch/01-create`

## Pre-Condition

- At least one Employee External Assignment Agreement Batch record exists.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreements**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Select the **# Batch** field. Once selected, the following fields are automatically
   filled from the batch and become read-only:
   - **Type**
   - **Partner**
   - **Date**
   - **Date Start**
   - **Date End**
4. Fill in the remaining required fields:
   - **Title**: Enter the agreement title.
   - **Receivable Account**: Select the receivable account used for invoicing.
   - **Journal**: Select the accounting journal used for invoicing.
5. Click **Save**.

## Post-Condition

- A new Employee External Assignment Agreement record is created in **Draft** status,
  linked to the selected batch. The **Type**, **Partner**, **Date**, **Date Start**, and
  **Date End** fields hold the same values as the batch.
