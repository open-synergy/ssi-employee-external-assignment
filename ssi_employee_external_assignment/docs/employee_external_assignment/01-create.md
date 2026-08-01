# Create Employee External Assignment

> **Module:** ssi_employee_external_assignment\
> **Model:** `employee_external_assignment`\
> **Menu:** Human Resource > Career Management > External Assignment > Assignments\
> **Actor:** user in group `Employee External Assignment / User`\
> **State:** `—` → `draft`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Career Management > External Assignment > Assignments**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Type**: Select the assignment type. It determines the allowed employees and
     partners for this assignment.
   - **Employee**: Select the employee being assigned. Only employees allowed by the
     selected **Type** can be selected.
   - **Department**: Automatically filled from **Employee**. Change if needed.
   - **Manager**: Automatically filled from **Employee**. Change if needed.
   - **Job Position**: Automatically filled from **Employee**. Change if needed.
   - **Date**: Defaults to today's date. Change if needed.
   - **Start Date**: Enter the start date of the assignment.
   - **End Date**: Enter the end date of the assignment.
   - **Partner**: Select the external partner. Only partners allowed by the selected
     **Type** can be selected.
   - **Partner Location**: Optional. Select the location of the selected **Partner**.
4. Click **Save**.

## Post-Condition

- A new Employee External Assignment record is created in **Draft** status.
