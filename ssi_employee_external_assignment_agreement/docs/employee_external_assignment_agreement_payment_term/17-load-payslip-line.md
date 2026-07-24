# Load Payslip Lines — Employee External Assignment Agreement Payment Term

## Pre-Condition

- Record is in **Draft** status (the button is only available while in Draft).
- At least one Payslip is already linked to the record (see
  [16-reload-payslip.md](16-reload-payslip.html)).
- The Agreement has at least one Job Position detail with a Compensation Term.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Payment Terms**
   menu.
2. Open the record.
3. Go to the **Payslip Lines** tab.
4. Click the **Payslip Lines** button (refresh icon).

## Post-Condition

- For every Compensation Term on the Agreement's Job Position details, the matching
  Payslip Lines (same Salary Rule) from the record's own linked Payslips are loaded into
  the **Payslip Lines** field.
- The **Payment Term Rules** list is regenerated from the Agreement's Salary Rules,
  replacing any previously generated rows.
