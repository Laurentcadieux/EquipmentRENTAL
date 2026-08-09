# EquipmentRental UiPath Cloud Solution — Planning Brief

## Confirmed direction

- **Delivery model:** UiPath Automation Cloud.
- **Tenant:** `Playground`.
- **Automation naming and target-folder convention:**
  `EquipmentRENTAL/%projectname% = EquipmentRENTAL/LCversion`.
  `LCversion` is the shared release folder for this showcase; individual
  automation/project names remain the unique identifiers.
- **Solution scope:** a multi-project UiPath Solution packaged as `.uipx`.
- **Orchestration:** Maestro Case Management controls the end-to-end rental
  lifecycle.
- **Runtime:** serverless for API-first automations and the Python agent.
- **Data:** the corrected mock EquipmentRental Data Fabric model in
  `../equipment-rental-data-model.md`.
- **Showcase target:** approximately 50% API-based work, 15% RPA interactions,
  20% Python-agent-led reasoning, and 15% Agent work against mock data.
  These ratios guide the demo;
  they are not a measure of production workload.

## Required business journeys

1. Create and approve a rental request, then create an active rental contract.
2. Monitor contracts and raise 28-day, 7-day, 1-day, due-date, and overdue
   flags.
3. Process an extension, including cancellation of a pending pickup if needed.
4. Process a vendor or ACME cancellation.
5. Schedule and confirm normal or immediate pickup, inspect returned equipment,
   and close the contract.

## Integration and data constraints

- All activities must use the same `correlation_id`, `rental_request_id`, and
  `contract_id` where applicable.
- Mock vendor data includes three active vendors with exactly two locations per
  vendor.
- API and RPA paths must operate against the same mock Data Fabric records;
  they are different interaction channels, not duplicate systems of record.
- The agent may recommend a route or compose summaries, but deterministic
  validation, money calculations, status changes, and final close/cancel
  actions remain controlled workflows.

## Planning decisions still to resolve

- The hosting pattern for the RPA showcase (serverless-compatible process vs
  available unattended machine/runtime) must be checked against tenant
  capability.
- Authentication, user/group roles, Data Fabric scope, and integration-service
  connection names need tenant discovery before build.
- Vendor APIs and Mastermind are mock integrations; contract schemas and error
  behavior must be specified before implementation.
