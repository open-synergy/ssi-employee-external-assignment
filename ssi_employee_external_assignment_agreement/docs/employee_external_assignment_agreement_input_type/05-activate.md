# Activate Employee External Assignment Agreement Input Type

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_input_type`\
> **Menu:** Human Resource > Configuration > Career > External Assignment > Agreement
> Input Types\
> **Actor:** user in group `Human Resource - Configurator / External Assignment Agreement Input Type`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- The record is archived (inactive).

## Flow

1. Open the **Human Resource > Configuration > Career > External Assignment > Agreement
   Input Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Open the archived record to reactivate.
4. Click the **Edit** button.
5. Toggle the **Active** field on.
6. Click **Save**.

## Post-Condition

- The record is restored and appears again in the default list view.
- The **Archived** ribbon no longer appears on the form.
- The input type can be selected again as **Input Type** on new Employee External
  Assignment Agreement Input records.
