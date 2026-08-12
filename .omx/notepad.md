# Working Memory

## 2026-08-12 — EquipmentRENTAL Data Fabric migration and functional automation integration

- User approved creation/copy of the 13 native Data Fabric schemas and 22,758 source records from `EquipmentRENTAL/LCversion` (`11b28f3b-294e-4593-aba1-a5079c54e7aa`) to the target solution folder `EquipmentRENTAL/EquipmentRENTAL_LCversion` (`5e6c96e4-ee96-4055-a02b-d62993318509`), retaining the source.
- All 13 target schemas exist. Target IDs:
  - ACME_Locations `0d1ce66a-8896-f111-9b33-000d3a64f664`
  - ACME_Departments `221ce66a-8896-f111-9b33-000d3a64f664`
  - ACME_Staff `abd22971-8896-f111-9b33-000d3a64f664`
  - Vendor_Master `bfd22971-8896-f111-9b33-000d3a64f664`
  - Vendor_Locations `752a6377-8896-f111-9b33-000d3a64f664`
  - Vendor_Equipment_Catalog `bac26185-8896-f111-9b33-000d3a64f664`
  - Rental_Requests `794b6d8d-8896-f111-9b33-000d3a64f664`
  - Rental_Contracts `914b6d8d-8896-f111-9b33-000d3a64f664`
  - Rental_Equipment_Items `24e6589a-8896-f111-9b33-000d3a64f664`
  - Rental_Lifecycle_Events `ac9a95a0-8896-f111-9b33-000d3a64f664`
  - Rental_Monitoring_Flags `d09a95a0-8896-f111-9b33-000d3a64f664`
  - Pickup_Return_Requests `9458c8a6-8896-f111-9b33-000d3a64f664`
  - Vendor_Equipment_Availability `d76035c7-8896-f111-9b33-000d3a64f664`
- Target `ACME_Locations` data was verified: 4 records copied. Need resume `UIPATH_DATA_FABRIC_FOLDER_KEY=5e6c96e4-ee96-4055-a02b-d62993318509 UIPATH_CLI_DISABLE_VERSION_SYNC=1 python3 -u scripts/seed_data_fabric.py` and verify all record counts through `uip df records list` (entity list returns null RecordCount in this tenant).
- `scripts/seed_data_fabric.py` changed: folder key now uses `UIPATH_DATA_FABRIC_FOLDER_KEY`; it has temporary command diagnostics to remove/refine before commit.
- `automation/EquipmentRENTAL_LCversion/EquipmentRentalCase/caseplan.json`: all 12 `folderPath` values changed from `EquipmentRENTAL/LCversion` to `EquipmentRENTAL/EquipmentRENTAL_LCversion`.
- User clarified they need functional Data Fabric reads/writes, not just bindings. Remaining: implement Data Fabric CRUD in RentalCommandsApi, RentalMonitoringApi, VendorPickupApi; configure RentalCaseAgent + RentalOrchestratorAgent with target data context/tools; validate API workflow JSON; sync resources; deploy missing RentalCommandsApi and RentalCaseAgent; validate case bindings/pack/deploy.
- Existing target deployed processes: RentalMonitoringApi, VendorPickupApi, RentalOrchestratorAgent, EquipmentRentalCase. Missing in target: RentalCommandsApi and RentalCaseAgent.
- Source solution project files have empty bindings_v2.json; current APIs are pure JS responses and require supported Data Fabric activity/connector design. `uip api-workflow registry resolve` syntax is positional (`resolve <keyword>`); prior `--query` call failed.
