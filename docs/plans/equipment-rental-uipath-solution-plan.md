# EquipmentRental UiPath Cloud Solution Plan

Date: August 9, 2026

## 1. Objective

Build a UiPath Cloud showcase solution for ACME EquipmentRental that demonstrates an end-to-end rental lifecycle using:

- **Maestro Case Management** as the orchestration layer
- **Automation Cloud Robots - Serverless** for background runtime
- **Data Fabric / Data Service** as the mock system of record
- A balanced showcase of **API-first automation**, **RPA interactions**, and **agent-assisted reasoning**

This plan treats the user-provided ratio as a **demo design target**:

- **50% API**
- **15% RPA**
- **20% Python Agent**
- **15% Agent**

These percentages define the **showcase composition**, not workload metering.

## 2. Why Maestro Case is the right orchestration model

UiPath documents that **Maestro Case** is suited for work that is **long-running, exception-heavy, and requires dynamic routing between stages based on evolving data and human judgment**. That fits EquipmentRental because contracts can be created, extended, cancelled, returned, flagged, reworked, and escalated over days or weeks. Source: https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/maestro-bpmn-vs-maestro-case-when-to-use-case-management

## 3. Solution scope

### In scope

1. Rental request intake and approval
2. Contract creation from approved request
3. Equipment line-item assignment from vendor catalog
4. Contract monitoring and alerting at 28, 7, 1, and 0 days
5. Overdue detection
6. Extension processing
7. Cancellation processing
8. Pickup / return scheduling
9. Return inspection and damage handling
10. Case dashboards, audit trail, and showcase reporting
11. Agent-led recommendations and summaries with deterministic workflow enforcement

### Out of scope for showcase v1

1. Real ERP/AP/PO integrations
2. Real vendor production APIs
3. Payment execution
4. Invoice reconciliation
5. Contract OCR / document extraction
6. Production-grade identity model beyond the roles needed for demo
7. Advanced mobile or external customer portal experiences

## 4. Target product composition

### Core UiPath projects

1. **Maestro Case project**
   - Owns case stages, SLAs, transitions, personas, and lifecycle rules
2. **API Workflow project(s)**
   - CRUD and business operations against Data Fabric and mock vendor APIs
3. **RPA project(s)**
   - Demonstrates UI automation against Data Fabric UI or mock vendor UI where API is intentionally absent
4. **Python Agent project**
   - Provides recommendation, summarization, and guided decision support
5. **Agent project**
   - Provides a low-code agent experience for scoped case guidance and routing
5. **Solution package (`.uipx`)**
   - Bundles the above into one deployable showcase

## 5. Capability allocation matrix

| Capability | Primary technology | Showcase share | Why it belongs there |
|---|---|---:|---|
| Create request, approve request, create contract, update status, create flags, maintain case state | API Workflows + Data Fabric APIs | 50% | Deterministic CRUD and orchestration-friendly service calls |
| Vendor catalog sync, vendor availability check, pickup request submit, return confirm | API Workflows | 50% | Best demo of serverless, governed, reusable integrations |
| Data entry fallback, legacy screen navigation, no-API vendor task, UI verification | RPA | 15% | Shows UiPath UI automation value when APIs are incomplete |
| Recommendation of extend/cancel/return route, summary generation, case briefing, escalation narrative | Python Agent | 20% | Shows judgment support without owning final business-state mutation |
| Guided case routing and scoped operator assistance | Agent | 15% | Demonstrates a low-code agent alongside the Python implementation |

### Guardrail

The agent **must not** be the system of record. Final updates to price, status, dates, flags, approvals, and closure are executed by deterministic API or RPA workflows.

## 6. Proposed end-to-end case stages

### Primary stages

1. **Intake**
   - Create `Rental_Request`
   - Validate department/staff/vendor references
   - Assign correlation keys
2. **Approval**
   - Manager or procurement approval
   - Reject, approve, or cancel before contract
3. **Fulfillment**
   - Create `Rental_Contract`
   - Attach `Rental_Equipment_Items`
   - Activate contract
4. **Active Monitoring**
   - Scheduled checks create flags and tasks
   - Agent prepares recommended action summary
5. **Disposition**
   - Branch to extension, cancellation, standard return, or immediate pickup
6. **Closure**
   - Final inspection, damage decision, financial finalization, close case

### Secondary stages

1. **Extension Review**
2. **Cancellation Review**
3. **Return / Pickup Coordination**
4. **Damage Review**
5. **Overdue Escalation**
6. **Exception Recovery**

## 7. Case tasks by execution mode

UiPath documents that Maestro Case tasks can include **Human action, RPA Workflow, API Workflow, Execute Connector, AI Agent, Child Case, Wait for Timer, and Wait for Connector Event**. Source: https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/maestro-bpmn-vs-maestro-case-when-to-use-case-management

| Stage | Task | Mode | Notes |
|---|---|---|---|
| Intake | Validate request payload | API Workflow | Check required fields and relationships |
| Approval | Manager approval | Human task | Approve / reject / request changes |
| Fulfillment | Create contract and items | API Workflow | Writes Data Fabric records |
| Fulfillment | Fetch vendor availability | API Workflow | Mock vendor API call |
| Fulfillment | Legacy vendor entry fallback | RPA | Used when vendor API path is absent |
| Active Monitoring | Daily monitor scheduler | Wait for timer + API Workflow | Creates flags based on dates |
| Active Monitoring | Generate case summary | Agent | Summarizes expiring / overdue context |
| Extension Review | Recommend extension path | Agent | Recommendation only |
| Extension Review | Apply approved extension | API Workflow | Updates contract and event history |
| Cancellation Review | Cancel vendor booking | API Workflow or RPA | Channel depends on mock vendor capability |
| Return / Pickup | Request pickup | API Workflow | Creates pickup request |
| Return / Pickup | Confirm pickup in legacy UI | RPA | Showcase fallback path |
| Damage Review | Summarize inspection risk | Agent | Suggests severity and next action |
| Closure | Final close | API Workflow | Deterministic final status transition |

## 8. Data and correlation architecture

### Required correlation keys

Every case, task, workflow, event, and log entry must carry:

- `correlation_id`
- `rental_request_id`
- `contract_id` when contract exists
- `uipath_case_id` once case is instantiated
- `source_event_id` for idempotent vendor/event processing

### Relationship model

UiPath documents that Data Fabric relationships are **one-to-many (1:M)**. The current schema already aligns to that pattern for departments, staff, contracts, items, events, and flags. Source: https://docs.uipath.com/data-service/automation-cloud/latest/user-guide/relationship

### Design rule

API and RPA paths must update the **same Data Fabric records**, not separate mock stores.

## 9. Runtime and deployment model

### Runtime

Use **Automation Cloud Robots - Serverless** for background automations. UiPath documents that serverless robots run background automation without requiring customers to provision or manage infrastructure, and that unattended execution requires **background, cross-platform** processes. Sources:

- https://docs.uipath.com/orchestrator/automation-cloud/latest/user-guide/automation-cloud-robots-serverless
- https://docs.uipath.com/orchestrator/automation-cloud/latest/user-guide/executing-unattended-automations-with-serverless-robots

### Important runtime constraint

The RPA showcase must be designed as a **background cross-platform** process if it is expected to run on serverless. If a chosen demo needs classic foreground UI interaction, the tenant will need a non-serverless unattended runtime path. This remains a build-time gating decision.

### Packaging

Bundle the case project, API workflow project(s), agent project, and RPA project(s) into one UiPath Solution (`.uipx`).

## 10. API strategy

UiPath documents that Data Fabric Open API uses OAuth 2.0 and external-app scopes, with access tokens typically valid for one hour. Source: https://docs.uipath.com/data-service/automation-cloud/latest/user-guide/api-access

### API-first operations

1. Create/read/update Data Fabric entities
2. Raise monitoring flags
3. Write lifecycle events
4. Call mock vendor endpoints
5. Trigger pickup and return confirmations
6. Return normalized JSON payloads to Maestro and agents

### API workflow candidates

1. `CreateRentalRequestApi`
2. `ApproveRentalRequestApi`
3. `CreateRentalContractApi`
4. `CreateMonitoringFlagsApi`
5. `GetExpiringContractsApi`
6. `ExtendRentalContractApi`
7. `CancelRentalContractApi`
8. `CreatePickupReturnRequestApi`
9. `CompleteReturnInspectionApi`
10. `CloseRentalCaseApi`
11. `MockVendorAvailabilityApi`
12. `MockVendorPickupApi`

## 11. RPA strategy

RPA should be used selectively to prove UiPath value where UI automation is still needed.

### Recommended RPA showcase slices

1. Enter a pickup request in a mock vendor web portal with no API
2. Validate Data Fabric UI record state after an API operation
3. Perform exception fallback when a vendor API intentionally returns an error
4. Demonstrate human-readable evidence capture (screenshots / logs)

### Constraint

Do not overuse RPA for CRUD that is already better served by API workflows. That weakens the showcase architecture.

## 12. Agent strategy

UiPath documents that agents can use **API workflows as tools**, and that API workflows can provide secure, deterministic, serverless integrations for agents. Source: https://docs.uipath.com/agents/automation-cloud/latest/user-guide/api-workflows

### Agent responsibilities

1. Summarize a rental case for case workers
2. Recommend next-best action for expiring contracts
3. Explain why a contract was flagged
4. Draft manager-facing extension or cancellation summaries
5. Triage overdue or damage-risk cases into suggested queues

### Agent guardrails

1. No direct final mutation of contract status
2. No final approval authority
3. No financial calculation as source of truth
4. All external actions must go through approved tools
5. Tool use limited to approved API workflows / RPA handoffs

## 13. Human-in-the-loop design

Use HITL for:

1. Approval of request when above threshold
2. Approval of extension beyond policy window
3. Damage-charge confirmation
4. Exception-handling review when vendor data conflicts with ACME data

## 14. Personas and access

As of **June 25, 2026**, UiPath notes that **Case Management solution roles are process-scoped** and managed through the solution deployment lifecycle rather than tenant-level Manage Access. Source: https://docs.uipath.com/automation-cloud/automation-cloud/latest/release-notes/june-2026

### Showcase personas

1. Requester
2. Manager Approver
3. Procurement Specialist
4. Case Worker
5. Operations Supervisor
6. Platform Admin

## 15. Build sequence

### Phase 1 — Foundation

1. Confirm tenant capabilities and licenses
2. Confirm Data Fabric service enabled
3. Confirm Maestro Case availability
4. Confirm serverless and robot units
5. Confirm target folder and solution structure
6. Create choice sets, entities, and relationships in Data Fabric
7. Seed correlated mock data

### Phase 2 — Core deterministic services

1. Build API workflows for Data Fabric CRUD and business actions
2. Define mock vendor APIs and error behaviors
3. Create normalized contracts for workflow inputs/outputs
4. Add idempotency and correlation handling

### Phase 3 — Case orchestration

1. Design `sdd.md`
2. Build `caseplan.json`
3. Implement stages, tasks, SLAs, escalations, and re-entry
4. Connect API workflows, human tasks, RPA workflows, and agent tools

### Phase 4 — RPA and agent showcase

1. Build minimal but credible RPA fallback journeys
2. Build agent with approved tools and prompts
3. Add monitoring summary and recommendation tasks

### Phase 5 — Solution packaging and demo hardening

1. Bundle all projects in `.uipx`
2. Validate solution deployment
3. Run test scenarios
4. Build demo dashboards and operator runbook

## 16. OMX sub-agent and skill plan

Because the user asked to plan with the available sub-agents and skills, use this staffing model for execution.

### OMX role map

| Lane | Recommended OMX role | Purpose |
|---|---|---|
| Requirements hardening | `analyst` | Resolve remaining business rules and acceptance criteria |
| Architecture | `architect` | Validate product split across Case / API / RPA / Agent |
| Work planning | `planner` | Sequence implementation tasks and dependencies |
| Case build | `executor` with `uipath-maestro-case` | Build `sdd.md`, `tasks.md`, `caseplan.json` |
| API workflow build | `executor` with `uipath-api-workflow` | Create Data Fabric and mock-vendor API workflows |
| RPA build | `executor` with `uipath-rpa` | Build UI automation fallback processes |
| Agent build | `executor` with `uipath-agents` | Build recommendation / summary agent |
| Platform setup | `executor` with `uipath-platform` | Tenant, folder, Data Fabric, connection, and deployment work |
| Packaging | `executor` with `uipath-solution` | Package and deploy `.uipx` |
| Verification | `verifier` or `critic` | Validate claims, coverage, and demo readiness |

### Primary UiPath skills by phase

| Phase | Primary skills |
|---|---|
| Planning / SDD | `uipath-planner`, `uipath-maestro-case` |
| Platform discovery | `uipath-platform`, `uipath-admin` |
| Case build | `uipath-maestro-case` |
| API build | `uipath-api-workflow` |
| RPA build | `uipath-rpa` |
| Agent build | `uipath-agents` |
| Packaging | `uipath-solution` |
| Review / QA | `uipath-review`, `uipath-test`, `uipath-insights` |
| HITL design | `uipath-human-in-the-loop`, `uipath-tasks` |

## 17. Critical acceptance criteria

1. A new rental request can be created and approved end to end.
2. An approved request can create an active rental contract with at least one equipment item.
3. All related records share valid correlation keys.
4. A scheduled monitor creates 28-day, 7-day, 1-day, due-date, and overdue flags correctly.
5. An extension updates contract end date, logs lifecycle history, and resolves/replaces affected flags.
6. A cancellation updates the contract, logs the event, and halts further return processing unless re-opened.
7. A return flow creates pickup records, updates inspection result, and closes the contract.
8. An agent can summarize a case and recommend an action using only approved tools.
9. RPA can complete at least one no-API vendor path against the same correlated case.
10. Maestro Case dashboards and history make the full case auditable.
11. The packaged solution deploys and runs in the target UiPath tenant.

## 18. Key business-rule gaps to resolve before build

1. **Approval policy** — exact thresholds for manager vs procurement approval
2. **Extension policy** — maximum extension length and escalation rules
3. **Cancellation policy** — financial effect before and after delivery
4. **Damage policy** — how damage charges are assessed and approved
5. **Overdue policy** — escalation tiers and SLA ownership
6. **Vendor simulation contract** — exact request/response schemas and failure codes
7. **RPA target choice** — Data Fabric UI vs mock vendor portal vs both
8. **Demo KPIs** — what success measures the showcase must display live

## 19. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Serverless RPA cannot support desired UI demo | Medium | Keep RPA slice background-compatible or switch that slice to VM/unattended runtime |
| Overuse of agent creates weak governance story | High | Restrict agent to recommendation and summarization |
| Duplicate state paths between API and RPA | High | Force both channels to update the same Data Fabric entities |
| Mock vendor design too shallow | Medium | Define explicit API contracts, latency, and error scenarios |
| Missing process-scoped role planning | Medium | Define personas in case solution design, not as tenant-only roles |
| Data Fabric API quota/licensing too low for demo loops | Medium | Size demo data and polling frequency carefully |

## 20. Recommended next artifact set

1. `sdd.md` for the full solution
2. `tasks/tasks.md` execution backlog
3. API contract document for mock vendor services
4. Demo data seeding spec
5. Test scenario pack for happy path + exception paths
