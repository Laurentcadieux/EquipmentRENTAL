# Data Fabric Schema Preview — EquipmentRENTAL LCversion

**Scope:** folder `EquipmentRENTAL/LCversion` (`11b28f3b-294e-4593-aba1-a5079c54e7aa`).

This is a non-mutating preview. `Field Name` is Data Fabric-safe (letters/digits only); `CSV Display Name` is the existing source header. Relationship display fields remain pending your selection.

## ACME_Departments

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `DepartmentId` | `department_id` | STRING |
| `DepartmentName` | `department_name` | STRING |
| `CostCenter` | `cost_center` | STRING |
| `BusinessUnit` | `business_unit` | STRING |
| `ManagerStaffId` | `manager_staff_id` | RELATIONSHIP → ACME_Staff |
| `DefaultLocationId` | `default_location_id` | RELATIONSHIP → ACME_Locations |
| `Status` | `status` | STRING |

## ACME_Locations

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `LocationId` | `location_id` | STRING |
| `LocationName` | `location_name` | STRING |
| `AddressLine1` | `address_line1` | STRING |
| `City` | `city` | STRING |
| `State` | `state` | STRING |
| `PostalCode` | `postal_code` | STRING |
| `SiteContactStaffId` | `site_contact_staff_id` | RELATIONSHIP → ACME_Staff |
| `Status` | `status` | STRING |

## ACME_Staff

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `StaffId` | `staff_id` | STRING |
| `FirstName` | `first_name` | STRING |
| `LastName` | `last_name` | STRING |
| `Email` | `email` | STRING |
| `Role` | `role` | STRING |
| `DepartmentId` | `department_id` | RELATIONSHIP → ACME_Departments |
| `LocationId` | `location_id` | RELATIONSHIP → ACME_Locations |
| `ApprovalLimit` | `approval_limit` | DECIMAL (2) |
| `Status` | `status` | STRING |

## Pickup_Return_Requests

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `PickupReturnRequestId` | `pickup_return_request_id` | STRING |
| `ContractId` | `contract_id` | RELATIONSHIP → Rental_Contracts |
| `VendorId` | `vendor_id` | RELATIONSHIP → Vendor_Master |
| `VendorLocationId` | `vendor_location_id` | RELATIONSHIP → Vendor_Locations |
| `RequestType` | `request_type` | STRING |
| `RequestedDate` | `requested_date` | DATE |
| `PreferredPickupDate` | `preferred_pickup_date` | DATE |
| `ScheduledPickupDate` | `scheduled_pickup_date` | DATE |
| `VendorConfirmationNumber` | `vendor_confirmation_number` | STRING |
| `RequestStatus` | `request_status` | STRING |
| `InspectionResult` | `inspection_result` | STRING |
| `DamageFlags` | `damage_flags` | STRING |
| `EquipmentReturnedDate` | `equipment_returned_date` | DATE |
| `CreatedAt` | `created_at` | DATETIME_WITH_TZ |
| `UpdatedAt` | `updated_at` | DATETIME_WITH_TZ |
| `CorrelationId` | `correlation_id` | STRING |

## Rental_Contracts

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `ContractId` | `contract_id` | STRING |
| `RentalRequestId` | `rental_request_id` | RELATIONSHIP → Rental_Requests |
| `VendorId` | `vendor_id` | RELATIONSHIP → Vendor_Master |
| `VendorLocationId` | `vendor_location_id` | RELATIONSHIP → Vendor_Locations |
| `DepartmentId` | `department_id` | RELATIONSHIP → ACME_Departments |
| `RequestedByStaffId` | `requested_by_staff_id` | RELATIONSHIP → ACME_Staff |
| `ApprovedByStaffId` | `approved_by_staff_id` | RELATIONSHIP → ACME_Staff |
| `DeliveryLocationId` | `delivery_location_id` | RELATIONSHIP → ACME_Locations |
| `BillingLocationId` | `billing_location_id` | RELATIONSHIP → ACME_Locations |
| `ContractNumber` | `contract_number` | STRING |
| `StartDate` | `start_date` | DATE |
| `EndDate` | `end_date` | DATE |
| `OriginalEndDate` | `original_end_date` | DATE |
| `TotalEstimatedPrice` | `total_estimated_price` | DECIMAL (2) |
| `ActualTotalPrice` | `actual_total_price` | DECIMAL (2) |
| `TaxAmount` | `tax_amount` | DECIMAL (2) |
| `DamageChargeAmount` | `damage_charge_amount` | DECIMAL (2) |
| `CurrencyCode` | `currency_code` | STRING |
| `BillingFrequency` | `billing_frequency` | STRING |
| `Status` | `status` | STRING |
| `UipathCaseId` | `uipath_case_id` | STRING |
| `SourceEventId` | `source_event_id` | STRING |
| `CreatedAt` | `created_at` | DATETIME_WITH_TZ |
| `UpdatedAt` | `updated_at` | DATETIME_WITH_TZ |
| `CorrelationId` | `correlation_id` | STRING |

## Rental_Equipment_Items

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `RentalItemId` | `rental_item_id` | STRING |
| `ContractId` | `contract_id` | RELATIONSHIP → Rental_Contracts |
| `VendorEquipmentId` | `vendor_equipment_id` | RELATIONSHIP → Vendor_Equipment_Catalog |
| `EquipmentCategory` | `equipment_category` | STRING |
| `EquipmentName` | `equipment_name` | STRING |
| `Model` | `model` | STRING |
| `SerialNumber` | `serial_number` | STRING |
| `Quantity` | `quantity` | DECIMAL (0) |
| `DailyRate` | `daily_rate` | DECIMAL (2) |
| `WeeklyRate` | `weekly_rate` | DECIMAL (2) |
| `MonthlyRate` | `monthly_rate` | DECIMAL (2) |
| `DeliveryFee` | `delivery_fee` | DECIMAL (2) |
| `PickupFee` | `pickup_fee` | DECIMAL (2) |
| `CurrencyCode` | `currency_code` | STRING |
| `ConditionAtDelivery` | `condition_at_delivery` | STRING |
| `ConditionAtReturn` | `condition_at_return` | STRING |
| `CreatedAt` | `created_at` | DATETIME_WITH_TZ |
| `UpdatedAt` | `updated_at` | DATETIME_WITH_TZ |
| `CorrelationId` | `correlation_id` | STRING |

## Rental_Lifecycle_Events

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `EventId` | `event_id` | STRING |
| `ContractId` | `contract_id` | RELATIONSHIP → Rental_Contracts |
| `EventType` | `event_type` | STRING |
| `EventTimestamp` | `event_timestamp` | DATETIME_WITH_TZ |
| `PerformedByStaffId` | `performed_by_staff_id` | RELATIONSHIP → ACME_Staff |
| `OldEndDate` | `old_end_date` | DATE |
| `NewEndDate` | `new_end_date` | DATE |
| `ReasonCode` | `reason_code` | STRING |
| `Notes` | `notes` | STRING |
| `SourceSystem` | `source_system` | STRING |
| `SourceEventId` | `source_event_id` | STRING |
| `CreatedAt` | `created_at` | DATETIME_WITH_TZ |
| `UpdatedAt` | `updated_at` | DATETIME_WITH_TZ |
| `CorrelationId` | `correlation_id` | STRING |

## Rental_Monitoring_Flags

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `FlagId` | `flag_id` | STRING |
| `ContractId` | `contract_id` | RELATIONSHIP → Rental_Contracts |
| `FlagType` | `flag_type` | STRING |
| `FlagDate` | `flag_date` | DATE |
| `TargetDate` | `target_date` | DATE |
| `DaysBeforeEnd` | `days_before_end` | DECIMAL (0) |
| `Severity` | `severity` | STRING |
| `Status` | `status` | STRING |
| `AssignedToStaffId` | `assigned_to_staff_id` | RELATIONSHIP → ACME_Staff |
| `ResolutionNotes` | `resolution_notes` | STRING |
| `AlertWindow` | `alert_window` | DECIMAL (0) |
| `AlertSentAt` | `alert_sent_at` | DATETIME_WITH_TZ |
| `CreatedAt` | `created_at` | DATETIME_WITH_TZ |
| `UpdatedAt` | `updated_at` | DATETIME_WITH_TZ |
| `CorrelationId` | `correlation_id` | STRING |

## Rental_Requests

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `RentalRequestId` | `rental_request_id` | STRING |
| `RequestNumber` | `request_number` | STRING |
| `RequestedByStaffId` | `requested_by_staff_id` | RELATIONSHIP → ACME_Staff |
| `DepartmentId` | `department_id` | RELATIONSHIP → ACME_Departments |
| `DeliveryLocationId` | `delivery_location_id` | RELATIONSHIP → ACME_Locations |
| `RequestDate` | `request_date` | DATE |
| `NeededStartDate` | `needed_start_date` | DATE |
| `NeededEndDate` | `needed_end_date` | DATE |
| `BusinessReason` | `business_reason` | STRING |
| `EstimatedCost` | `estimated_cost` | STRING |
| `CurrencyCode` | `currency_code` | STRING |
| `RequestStatus` | `request_status` | STRING |
| `ApprovedByStaffId` | `approved_by_staff_id` | RELATIONSHIP → ACME_Staff |
| `ApprovalDate` | `approval_date` | DATE |
| `CreatedAt` | `created_at` | DATETIME_WITH_TZ |
| `UpdatedAt` | `updated_at` | DATETIME_WITH_TZ |
| `CorrelationId` | `correlation_id` | STRING |

## Vendor_Equipment_Availability

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `AvailabilityId` | `availability_id` | STRING |
| `VendorEquipmentId` | `vendor_equipment_id` | RELATIONSHIP → Vendor_Equipment_Catalog |
| `AvailabilityDate` | `availability_date` | DATE |
| `TotalQuantity` | `total_quantity` | DECIMAL (0) |
| `ReservedQuantity` | `reserved_quantity` | DECIMAL (0) |
| `AvailableQuantity` | `available_quantity` | DECIMAL (0) |
| `OutOfServiceQuantity` | `out_of_service_quantity` | DECIMAL (0) |
| `AvailabilityStatus` | `availability_status` | STRING |
| `SourceSystem` | `source_system` | STRING |
| `CorrelationId` | `correlation_id` | STRING |
| `CreatedAt` | `created_at` | DATETIME_WITH_TZ |

## Vendor_Equipment_Catalog

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `VendorEquipmentId` | `vendor_equipment_id` | STRING |
| `VendorId` | `vendor_id` | RELATIONSHIP → Vendor_Master |
| `VendorLocationId` | `vendor_location_id` | RELATIONSHIP → Vendor_Locations |
| `EquipmentCategory` | `equipment_category` | STRING |
| `EquipmentName` | `equipment_name` | STRING |
| `Model` | `model` | STRING |
| `DailyRate` | `daily_rate` | DECIMAL (2) |
| `WeeklyRate` | `weekly_rate` | DECIMAL (2) |
| `MonthlyRate` | `monthly_rate` | DECIMAL (2) |
| `AvailableQuantity` | `available_quantity` | DECIMAL (0) |
| `TotalQuantity` | `total_quantity` | DECIMAL (0) |
| `AvailabilityStatus` | `availability_status` | STRING |
| `ReplacementValue` | `replacement_value` | DECIMAL (2) |
| `CurrencyCode` | `currency_code` | STRING |
| `LastAvailabilitySyncAt` | `last_availability_sync_at` | DATETIME_WITH_TZ |

## Vendor_Locations

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `VendorLocationId` | `vendor_location_id` | STRING |
| `VendorId` | `vendor_id` | RELATIONSHIP → Vendor_Master |
| `LocationName` | `location_name` | STRING |
| `AddressLine1` | `address_line1` | STRING |
| `City` | `city` | STRING |
| `State` | `state` | STRING |
| `PostalCode` | `postal_code` | STRING |
| `ContactName` | `contact_name` | STRING |
| `ContactEmail` | `contact_email` | STRING |
| `ContactPhone` | `contact_phone` | STRING |
| `Status` | `status` | STRING |

## Vendor_Master

| Field Name | CSV Display Name | Inferred Type |
|---|---|---|
| `VendorId` | `vendor_id` | STRING |
| `VendorName` | `vendor_name` | STRING |
| `VendorType` | `vendor_type` | STRING |
| `SupportEmail` | `support_email` | STRING |
| `SupportPhone` | `support_phone` | STRING |
| `ApiSystemName` | `api_system_name` | STRING |
| `Status` | `status` | STRING |

## Relationship display-field decisions required

| Target entity | Candidate display field choices |
|---|---|
| `ACME_Staff` | `StaffId` or `Email` |
| `ACME_Departments` | `DepartmentId` or `DepartmentName` |
| `ACME_Locations` | `LocationId` or `LocationName` |
| `Vendor_Master` | `VendorId` or `VendorName` |
| `Vendor_Locations` | `VendorLocationId` or `LocationName` |
| `Vendor_Equipment_Catalog` | `VendorEquipmentId` or `EquipmentName` |
| `Rental_Requests` | `RentalRequestId` or `RequestNumber` |
| `Rental_Contracts` | `ContractId` or `ContractNumber` |

## Import method

Because the schema includes `RELATIONSHIP` fields, CSV bulk import cannot be used for those values. Records will be created in dependency order with JSON inserts after parent UUIDs are resolved. The availability entity can be imported only after its catalog relationship UUIDs are translated.
