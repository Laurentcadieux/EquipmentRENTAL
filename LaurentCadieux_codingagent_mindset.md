# Laurent Cadieux Coding-Agent Mindset

## Purpose
Build a credible UiPath showcase as a working product, not a diagram: use realistic mock data, make every automation observable in Automation Cloud, and keep each decision easy for a human reviewer to trace.

## Working principles
1. **Start with correlated data.** Use stable IDs, realistic dates, lifecycle states, vendors, people, and contracts so each scenario can be replayed end to end.
2. **Build for demonstration and operations.** A showcase must prove API, RPA, agents, human tasks, Maestro Case, Data Fabric, and Studio Web—not merely claim them.
3. **Make progress visible.** Upload the solution to Studio Web early and after meaningful milestones so stakeholders can inspect current work without local tooling.
4. **Name for human discovery.** Prefix assets, entities, folders, and test data with `EquipmentRENTAL_LCversion` and use business-readable display names.
5. **Preserve correlation.** Carry case ID, contract ID, request ID, vendor ID, and correlation ID through every workflow, event, and audit record.
6. **Design the unhappy paths first.** Extension, vendor cancellation, immediate pickup, failed validation, overdue return, and damage are primary showcase scenarios.
7. **Use the right UiPath capability.** Maestro Case owns state and SLAs; API Workflows own service operations; RPA owns UI-only steps; Agents make reasoned recommendations; Actions capture accountable human decisions.
8. **Verify instead of assuming.** Read records after loading, validate projects before upload, inspect cloud responses, and never report deployment or test success without evidence.
9. **Recover safely.** Make loaders idempotent, detect partial loads, avoid duplicate records, and resume from known state.
10. **Document decisions as we work.** Keep the SDD, data dictionary, build plan, test specification, and implementation notes aligned with the cloud solution.

## Reusable delivery sequence
1. Confirm the business lifecycle and success measures.
2. Model real-world sample data and validate referential integrity.
3. Create the cloud folder, Data Fabric entities, and named mock resources.
4. Scaffold a single UiPath Solution and upload it to Studio Web immediately.
5. Add Maestro Case first, then API, RPA, Agent, Action, and test projects.
6. Implement one vertical slice: intake → monitor → return → close.
7. Add exception paths and operational dashboards.
8. Test happy path, extension, cancellation, immediate pickup, overdue alert, and damage.
9. Package, validate, publish, deploy, and document the evidence.

## EquipmentRental-specific operating rule
Every automation must receive or derive `correlation_id`. It must be written to the rental contract/event history and included in task, agent, RPA, and API logs so a case can be followed across UiPath services.

## Codex agents and skills
Use the project-local specialist agents in `.codex/agents` as a practical delivery team. Assign bounded responsibilities—analysis, architecture, planning, design, implementation, review, and verification—then integrate their evidence before making a completion claim. Use the installed UiPath skills to select the correct product surface for each task, rather than treating all UiPath work as generic code. Keep agent outputs, design decisions, and validation results in the repository so future contributors can understand both the solution and how it was built.
