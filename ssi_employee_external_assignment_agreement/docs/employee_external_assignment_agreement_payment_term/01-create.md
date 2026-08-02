# Create Employee External Assignment Agreement Payment Term

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement.payment_term`\
> **Menu:** Human Resource > Career Management > External Assignment > Payment Terms\
> **Actor:** user in group `Employee External Assignment Agreement - Payment Term / User`\
> **State:** `—` → `draft`

## Pre-Condition

- An Employee External Assignment Agreement record already exists.
- If more than one Employee External Assignment Agreement is in **Draft** status
  (document number still **/**), the **Agreement** field below cannot be searched by
  typed text (its search is limited to the actual document number, which is **/** for
  every Draft record). Confirm/approve the desired Agreement first, or make sure it is
  the only Draft Agreement, before creating its Payment Term this way.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Payment Terms**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Click the **Agreement** field and select the agreement this payment term belongs to.
4. Fill in the required fields:
   - **Date Start**: Enter the start date of the payment term period.
   - **Date End**: Enter the end date of the payment term period.
5. Click **Save**.

## Post-Condition

- A new Employee External Assignment Agreement Payment Term record is created in
  **Draft** status. The document number stays **/** until the payment term reaches the
  **Done** status. Agreement-related fields (Partner, Type, Currency, Pricelist) are
  automatically filled from the selected Agreement.
