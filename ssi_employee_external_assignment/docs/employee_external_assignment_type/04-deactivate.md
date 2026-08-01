# Deactivate Employee External Assignment Type

> **Module:** ssi_employee_external_assignment\
> **Model:** `employee_external_assignment_type`\
> **Menu:** Human Resource > Configuration > Career > External Asssignment Types\
> **Actor:** user in group `Human Resource - Configurator / Employee External Assignment Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Career > External Asssignment Types**
   menu.
2. Open the record to deactivate.
3. Click the **Edit** button.
4. Toggle the **Active** field off.
5. Click **Save**.

## Post-Condition

- The record is archived; an **Archived** ribbon appears on the form.
- The record no longer appears in the default list view.
- Deactivated types cannot be selected as **Type** on new Employee External Assignment
  records.
