# PRD — EquipmentRental UiPath Cloud Showcase

## Goal

Deliver a UiPath Cloud solution that demonstrates the complete ACME equipment
rental lifecycle with Maestro Case orchestration, shared Data Fabric data,
serverless API work, focused RPA, and two complementary agent experiences.

## Users

Requester, Manager Approver, Procurement Specialist, Case Worker, Operations
Supervisor, and Platform Admin.

## End-to-end journeys

1. Request → validate → approve → activate a rental contract.
2. Monitor active contracts and create flags at 28, 7, 1, and 0 days, plus
   overdue flags.
3. Extend, cancel, return, or immediately pick up equipment.
4. Inspect returned equipment, resolve damage, and close the case.

## Showcase allocation

| Channel | Target share | Purpose |
|---|---:|---|
| API Workflow | 50% | Deterministic Data Fabric and mock-vendor actions |
| RPA | 15% | Legacy mock-vendor portal fallback and visible UI evidence |
| Python Agent | 20% | Case summary, recommendation, explanation, and draft communication |
| Agent | 15% | Scoped low-code case guidance and routing support |

## Non-negotiables

- Maestro Case is the only lifecycle-orchestration owner.
- Data Fabric is the single mock system of record.
- Every cross-layer action carries `correlation_id`, `rental_request_id`, and
  `contract_id` when available.
- Agents are advisory; deterministic workflows own final business-state changes.
- Deploy to `Playground` using the naming standard
  `EquipmentRENTAL/%projectname% = EquipmentRENTAL/LCversion`.

## Showcase defaults

These defaults remove planning blockers and may be overridden in a future
business-policy pass.

| Policy | Default |
|---|---|
| Approval | Manager up to USD 10,000; Procurement above USD 10,000 |
| Extension | Up to 30 days without Procurement; maximum 90 additional days |
| Cancellation | Draft/pre-pickup cancellation closes the contract; post-pickup cancellation follows return/pickup flow |
| Damage | Case Worker records inspection; Operations Supervisor approves any damage charge |
| Overdue | Flag on due date; escalate daily at 1, 7, and 14 overdue days |
| Vendor behavior | Vendor 1 API-first; Vendor 2 delayed confirmation; Vendor 3 mock portal/RPA fallback |

## Success criteria

- All listed journeys complete with a single auditable correlation chain.
- At least one scenario exercises each channel allocation.
- A packaged solution deploys to the Playground target hierarchy.
- The operator can see automation, human decisions, agent recommendations, and
  case history in the same case experience.
