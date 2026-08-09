# EquipmentRental Case SDD Traceability

This matrix is the review control for the `EquipmentRentalCase` project. It
uses the original case blueprint's task IDs and names; a task is not considered
implemented merely because a generic stage exists.

| SDD ID | Stage | SDD task | UiPath task type | Current case node | Required resource |
|---|---|---|---|---|---|
| t01 | Intake & Triage | Validate job & rental data | RPA | `Validate job & rental data` | `EquipmentRentalValidationRpa` |
| t02 | Intake & Triage | Classify order status & route case | Agent | `Classify order status & route case` | `RentalCaseAgent` |
| t03 | Active Rental (Monitoring) | Monitor rental contract end date | API workflow | `Monitor rental contract end date` | `RentalMonitoringApi` |
| t04 | Active Rental (Monitoring) | Send staged expiry alerts | API workflow | `Send staged expiry alerts` | `RentalMonitoringApi` |
| t05 | Return & Close | Notify branch & confirm return intent | Action | `Notify branch & confirm return intent` | Equipment Rental Return Intent Action App |
| t06 | Return & Close | Submit pickup request & confirm scheduling | API workflow | `Submit pickup request & confirm scheduling` | `RentalCommandsApi` |
| t07 | Return & Close | Verify equipment required status in Mastermind | RPA | `Verify equipment required status in Mastermind` | `EquipmentRentalMastermindRpa` |
| t08 | Return & Close | Conduct return inspection & condition check | Action | `Conduct return inspection & condition check` | Equipment Rental Return Inspection Action App |
| t09 | Return & Close | Close rental job in Mastermind | RPA | `Close rental job in Mastermind` | `EquipmentRentalMastermindRpa` |
| t10 | Immediate Pickup | Notify United Rentals for ASAP pickup | API workflow | `Notify United Rentals for ASAP pickup` | `RentalCommandsApi` |
| t11 | Immediate Pickup | Update job status | RPA | `Update job status` | `EquipmentRentalMastermindRpa` |
| t12 | Extension Request | Cancel existing pickup request | API workflow | `Cancel existing pickup request` | `RentalCommandsApi` |
| t13 | Extension Request | Update rental extension in Mastermind | RPA | `Update rental extension in Mastermind` | `EquipmentRentalMastermindRpa` |
| t14 | Extension Request | Notify procurement & return to Active Rental | API workflow | `Notify procurement & return to Active Rental` | `RentalMonitoringApi` |

## Case Routing Implemented

- Case entry → **Intake & Triage**.
- Intake completion → **Active Rental (Monitoring)**.
- Monitoring completion → **Return & Close**.
- t05 `Immediate Pickup` → **Immediate Pickup** → returns to **Return & Close**.
- t05 `Request Extension` → **Extension Request** → resumes **Active Rental
  (Monitoring)**.
- The case may complete only when the required stages complete and
  `equipmentReturned` is true.

## Build Gaps Deliberately Visible

The case structure and all fourteen SDD task nodes are present and validated.
The resource projects and Action Apps in the final column must exist and be
bound before live debug can pass; they are not substituted by the old
`VendorPickupApi` or `RentalOrchestratorAgent` scaffolds. This keeps the
caseplan faithful to the SDD rather than presenting placeholders as runnable
automation.
