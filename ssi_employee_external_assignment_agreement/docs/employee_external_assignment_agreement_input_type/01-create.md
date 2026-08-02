# Create Employee External Assignment Agreement Input Type

> **Module:** ssi_employee_external_assignment_agreement\
> **Model:** `employee_external_assignment_agreement_input_type`\
> **Menu:** Human Resource > Configuration > Career > External Assignment > Agreement
> Input Types\
> **Actor:** user in group `Human Resource - Configurator / External Assignment Agreement Input Type`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Career > External Assignment > Agreement
   Input Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter the input type name.
   - **Code**: Enter a unique code for this input type, or fill with **/** to generate
     it later using the **Generate Code** button.
4. Go to the **Default Amount** tab and set:
   - **Default Amount**: Enter the default amount to be set when this input type is
     selected on an Employee External Assignment Agreement Input record. Optional,
     defaults to `0.00`.
5. Click **Save**.

## Post-Condition

- A new Employee External Assignment Agreement Input Type record is created and
  available for selection as **Input Type** on an Employee External Assignment Agreement
  Input record.
