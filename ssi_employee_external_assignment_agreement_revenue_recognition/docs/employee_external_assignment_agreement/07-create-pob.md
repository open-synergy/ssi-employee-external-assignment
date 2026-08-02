# Create PoB - Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement_revenue_recognition\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement`\
> **Model:** `employee_external_assignment_agreement`\
> **Menu:** Human Resource > Career Management > External Assignment > Agreements\
> **Actor:** user in group `Employee External Assignment Agreement / User`\
> **Requires:** `ssi_employee_external_assignment_agreement/employee_external_assignment_agreement/05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Record:** At least one line exists in the **Details**, **Other Fee**, or **Variable
  Fee** table.
- **Config:** **PoB Product** is set on the agreement's **Type** (see
  `employee_external_assignment_type/01-create`, this module's delta).
- **Access:** User is in group `Employee External Assignment Agreement / User`.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Agreements**
   menu.
2. Open the record to act on (status **On Progress**).
3. On the **Details** (or **Other Fee** / **Variable Fee**) tab, click the gear button
   **Create PoB** on the row.

## Post-Condition

- The **# PoB** column on that row is filled: a new Performance Obligation is created
  (or an existing one is linked) for that row.
- The Performance Obligation can be viewed via the **PoB(s)** smart button (see
  `01-create.md`, `## Modified Flow`).
- The agreement's status is unchanged — this action does not transition **state**.
