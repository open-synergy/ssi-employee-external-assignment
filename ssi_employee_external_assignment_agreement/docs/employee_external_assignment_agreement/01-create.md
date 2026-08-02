# Create Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreements\
> **Actor:** user in group `Employee External Assignment Agreement / User`\
> **State:** `—` → `draft`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreements**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Type**: Select the employee external assignment type. Determines the allowed
     partners, job positions, salary rules, and other/variable fee products available
     for this agreement.
   - **Partner**: Select the partner for this agreement. Options are filtered based on
     the selected **Type**.
   - **Title**: Enter the agreement title.
   - **Date Start**: Enter the start date of the agreement period.
   - **Date End**: Enter the end date of the agreement period.
   - **Currency**: Select the currency used for this agreement.
   - **Pricelist**: Select the pricelist. Options are filtered based on the selected
     **Currency**.
4. Go to the **Accounting Configuration** tab and fill in:
   - **Receivable Account**: Select the receivable account used for invoicing.
   - **Journal**: Select the accounting journal used for invoicing.
   - **Usage**: Automatically filled from **Type**. Change if needed.
5. Click **Save**.

## Post-Condition

- A new Employee External Assignment Agreement record is created in **Draft** status.
  The document number stays **/** until the agreement reaches the **Open** status.
