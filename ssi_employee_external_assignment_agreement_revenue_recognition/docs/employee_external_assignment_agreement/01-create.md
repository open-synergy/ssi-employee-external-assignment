# Create Employee External Assignment Agreement

> **Module:** ssi_employee_external_assignment_agreement_revenue_recognition\
> **Extends:** ssi_employee_external_assignment_agreement — model `employee_external_assignment_agreement`,
> aksi `01-create`\
> **Inline Actions:** `action_create_pob` (Create PoB)

## Modified Flow

- Anchor: on the same create form as Flow base step 3 (fill in the required fields,
  **Type** selected), before **Save** (Flow base step 5), three additional tables gain a
  **# PoB** column and a gear button **Create PoB** on each row: the **Details** tab
  (job position lines), the **Other Fee** tab, and the **Variable Fee** tab. Clicking
  **Create PoB** on a row creates or links a single Performance Obligation for that row
  directly — no wizard opens, no confirmation dialog appears. The button requires the
  agreement's **Type** to have **PoB Product** configured (see
  `employee_external_assignment_type/01-create`); otherwise it fails with an error.
- The same button can also be clicked while the record is **On Progress** — see
  `07-create-pob.md`.
- Related view (informational, not a Flow step, not covered by a tour): the same form
  gains a **Performance Obligations** tab with a read-only **Total PoB** amount and a
  **PoB(s)** button (`action_open_pob`) that navigates to a list of Performance
  Obligations linked to this agreement via its analytic account. Pure navigation — it
  does not write any field.
