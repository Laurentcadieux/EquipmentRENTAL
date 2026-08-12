# Production-ready Equipment Rental — context snapshot

- **Task statement:** Build the Equipment Rental UiPath solution to production readiness.
- **Desired outcome:** Real Data Fabric-backed automations, Case bindings, serverless execution, and end-to-end validation.
- **Known evidence:** The deployed v1.0.0 package has only four processes. The Case requires two RPA processes, two API workflows, an agent, and two Action Apps. `RentalCommandsApi` and `RentalCaseAgent` exist only locally. Data Fabric is not yet bound. The target folder already has one Serverless runtime.
- **Constraints:** Current login targets `uipathlabs` / `Playground`; local UiPath Helm/Studio fails to start, blocking RPA project scaffolding. No Data Fabric writes or production deployment will occur until target scope is confirmed.
- **Open decision boundary:** whether current Playground is a validation environment only or the intended production tenant.
