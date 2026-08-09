# Test Specification — EquipmentRental UiPath Cloud Showcase

## End-to-end scenarios

| ID | Scenario | Required proof |
|---|---|---|
| E2E-01 | API-first rental | Request, approval, contract, item, and case share correlation IDs |
| E2E-02 | 28-day monitoring | Exactly one `FourWeekExpiry` flag is created for the contract/window/date |
| E2E-03 | Extension | End date, lifecycle event, flags, and case route update coherently |
| E2E-04 | Pre-pickup cancellation | Contract closes without a return workflow |
| E2E-05 | Immediate pickup | Pickup request and RPA/API fallback remain correlated |
| E2E-06 | Return with damage | Inspection routes to review and closes only after approval |
| E2E-07 | Overdue escalation | Daily escalation occurs at 1, 7, and 14 overdue days |
| E2E-08 | Python Agent | Summary/recommendation is visible but does not mutate final state |
| E2E-09 | Agent | Scoped guidance/routing is recorded in the case history |
| E2E-10 | RPA fallback | Vendor 3 portal path updates the same Data Fabric entities as API paths |

## Cross-cutting assertions

- No duplicate processing for a repeated `source_event_id`.
- No duplicate monitoring flag for `(contract_id, alert_window, target_date)`.
- Vendor location and equipment catalog references match the contract vendor.
- Case history, lifecycle events, and workflow logs contain the same
  `correlation_id`.
- Agent tool calls are limited to approved deterministic workflows.
