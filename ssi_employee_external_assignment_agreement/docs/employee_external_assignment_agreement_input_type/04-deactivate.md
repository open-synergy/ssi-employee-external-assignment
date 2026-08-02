# Deactivate Employee External Assignment Agreement Input Type

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_input_type`\
> **Menu:** Human Resource > Configuration > Career > External Assignment > Agreement
> Input Types\
> **Actor:** user in group `Human Resource - Configurator / External Assignment Agreement Input Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Career > External Assignment > Agreement
   Input Types** menu.
2. Open the record to deactivate.
3. Click the **Edit** button.
4. Toggle the **Active** field off.
5. Click **Save**.

## Post-Condition

- The record is archived; an **Archived** ribbon appears on the form.
- The record no longer appears in the default list view.
- Deactivated input types cannot be selected as **Input Type** on new Employee External
  Assignment Agreement Input records.
