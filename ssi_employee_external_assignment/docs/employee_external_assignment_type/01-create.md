# Create Employee External Assignment Type

> **Module:** ssi_employee_external_assignment\
> **Model:** `employee_external_assignment_type`\
> **Menu:** Human Resource > Configuration > Career > External Asssignment Types\
> **Actor:** user in group `Human Resource - Configurator / Employee External Assignment Type`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Configuration > Career > External Asssignment Types**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter the type name.
   - **Code**: Enter a unique code for this type, or fill with **/** to generate it
     later using the **Generate Code** button.
4. Go to the **Partner** tab and set:
   - **Partner Selection Method**: Select how allowed partners are determined:
     **Manual**, **Domain** (default), or **Python Code**.
   - **Partners**: Only visible when Partner Selection Method = **Manual**. Select the
     partners allowed on an employee external assignment of this type.
   - **Partner Domain**: Only visible when Partner Selection Method = **Domain**. Enter
     the domain expression evaluated against Partner. Default: `[]`.
   - **Partner Python Code**: Only visible when Partner Selection Method = **Python
     Code**. Enter the Python code that sets the `result` variable to a recordset of
     Partner. Default: `result = []`.
5. Go to the **Employee** tab and set:
   - **Selecton Method**: Select how allowed employees are determined: **Manual**,
     **Domain** (default), or **Python Code**.
   - **Employees**: Only visible when Selecton Method = **Manual**. Select the employees
     allowed on an employee external assignment of this type.
   - **Domain**: Only visible when Selecton Method = **Domain**. Enter the domain
     expression evaluated against Employee. Default: `[]`.
   - **Python Code**: Only visible when Selecton Method = **Python Code**. Enter the
     Python code that sets the `result` variable to a recordset of Employee. Default:
     `result = []`.
6. Click **Save**.

## Post-Condition

- A new Employee External Assignment Type record is created and available for selection
  as **Type** on an Employee External Assignment record.
