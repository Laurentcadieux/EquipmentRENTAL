# EquipmentRental Mock Data Model

This model is the canonical source for synthetic data used to test the
EquipmentRental UiPath Cloud solution.  Every workflow, mock API event, queue
item, and UiPath Case must carry `correlation_id`, `rental_request_id`, and
`contract_id` when they exist.

## Modeling rules

- Store all entities in the same Data Fabric/Data Service scope so the
  relationships are available to the automations that use them.
- Treat every `*_id` as a required, unique text identifier unless marked
  optional. Use UiPath Relationship fields rather than unrelated free-text
  values when implementing these as Data Fabric entities.
- Use Choice Sets for every status, role, event type, flag type, severity,
  condition, and billing-frequency value listed below.
- Use ISO 4217 `currency_code` values and two-decimal monetary fields.
- `source_event_id` and the alert uniqueness rule make mock vendor events and
  monitoring runs idempotent.

## Shared audit fields

Add the following fields to all transaction entities (`Rental_Requests`,
`Rental_Contracts`, `Rental_Equipment_Items`, `Rental_Lifecycle_Events`,
`Rental_Monitoring_Flags`, and `Pickup_Return_Requests`):

| Column | Type | Notes |
|---|---|---|
| `created_at` | datetime | UTC creation timestamp |
| `updated_at` | datetime | UTC last-update timestamp |
| `correlation_id` | string | End-to-end test/run correlation, e.g. `ER-2026-000001` |

## ACME master data

### `ACME_Departments`

`department_id` (PK), `department_name`, `cost_center`, `business_unit`,
`manager_staff_id` (FK → `ACME_Staff.staff_id`, optional until staff are
seeded), `default_location_id` (FK → `ACME_Locations.location_id`), `status`.

### `ACME_Staff`

`staff_id` (PK), `first_name`, `last_name`, `email` (unique), `role`,
`department_id` (FK → `ACME_Departments.department_id`), `location_id`
(FK → `ACME_Locations.location_id`), `approval_limit`, `status`.

Allowed `role`: `Requester`, `Manager`, `Procurement`, `Case Worker`.

### `ACME_Locations`

`location_id` (PK), `location_name`, `address_line1`, `city`, `state`,
`postal_code`, `site_contact_staff_id` (FK → `ACME_Staff.staff_id`, optional
until staff are seeded), `status`.

## Vendor master data

### `Vendor_Master`

`vendor_id` (PK), `vendor_name` (unique), `vendor_type`, `support_email`,
`support_phone`, `api_system_name`, `status`.

### `Vendor_Locations`

`vendor_location_id` (PK), `vendor_id` (FK → `Vendor_Master.vendor_id`),
`location_name`, `address_line1`, `city`, `state`, `postal_code`,
`contact_name`, `contact_email`, `contact_phone`, `status`.

**Integrity rule:** the seed data contains exactly three active vendors and
exactly two active locations for each vendor.

### `Vendor_Equipment_Catalog`

`vendor_equipment_id` (PK), `vendor_id` (FK → `Vendor_Master.vendor_id`),
`vendor_location_id` (FK → `Vendor_Locations.vendor_location_id`),
`equipment_category`, `equipment_name`, `model`, `daily_rate`, `weekly_rate`,
`monthly_rate`, `available_quantity`, `total_quantity`, `availability_status`,
`replacement_value`, `currency_code`, `last_availability_sync_at`.

**Integrity rule:** `vendor_location_id` must belong to `vendor_id`.

### `Vendor_Equipment_Availability`

`availability_id` (PK), `vendor_equipment_id` (FK →
`Vendor_Equipment_Catalog.vendor_equipment_id`), `availability_date`,
`total_quantity`, `reserved_quantity`, `available_quantity`,
`out_of_service_quantity`, `availability_status`, `source_system`,
`correlation_id`, `created_at`.

**Integrity rules:** exactly one row may exist for
`(vendor_equipment_id, availability_date)`; `available_quantity` must equal
`total_quantity - reserved_quantity - out_of_service_quantity`.

## Rental lifecycle data

### `Rental_Requests`

`rental_request_id` (PK), `request_number` (unique), `requested_by_staff_id`
(FK → `ACME_Staff.staff_id`), `department_id` (FK →
`ACME_Departments.department_id`), `delivery_location_id` (FK →
`ACME_Locations.location_id`), `request_date`, `needed_start_date`,
`needed_end_date`, `business_reason`, `estimated_cost`, `currency_code`,
`request_status`, `approved_by_staff_id` (FK → `ACME_Staff.staff_id`,
optional), `approval_date` (optional), plus shared audit fields.

Allowed `request_status`: `Draft`, `Submitted`, `Approved`, `Rejected`,
`Cancelled`, `Converted`.

### `Rental_Contracts`

`contract_id` (PK), `rental_request_id` (FK →
`Rental_Requests.rental_request_id`), `vendor_id` (FK →
`Vendor_Master.vendor_id`), `vendor_location_id` (FK →
`Vendor_Locations.vendor_location_id`), `department_id` (FK →
`ACME_Departments.department_id`), `requested_by_staff_id` (FK →
`ACME_Staff.staff_id`), `approved_by_staff_id` (FK → `ACME_Staff.staff_id`),
`delivery_location_id` (FK → `ACME_Locations.location_id`),
`billing_location_id` (FK → `ACME_Locations.location_id`, optional),
`contract_number` (unique), `start_date`, `end_date`, `original_end_date`,
`total_estimated_price`, `actual_total_price` (optional), `tax_amount`,
`damage_charge_amount`, `currency_code`, `billing_frequency`, `status`,
`uipath_case_id` (optional), `source_event_id` (unique, optional), plus shared
audit fields.

Allowed `status`: `Draft`, `Active`, `Extended`, `Return Requested`,
`Returned`, `Cancelled`, `Closed`.

**Integrity rules:**

- `start_date <= end_date` and `original_end_date <= end_date`.
- `vendor_location_id` must belong to `vendor_id`.
- A contract can only be created from an `Approved` request.

### `Rental_Equipment_Items`

`rental_item_id` (PK), `contract_id` (FK →
`Rental_Contracts.contract_id`), `vendor_equipment_id` (FK →
`Vendor_Equipment_Catalog.vendor_equipment_id`), `equipment_category`,
`equipment_name`, `model`, `serial_number`, `quantity`, `daily_rate`,
`weekly_rate`, `monthly_rate`, `delivery_fee`, `pickup_fee`, `currency_code`,
`condition_at_delivery`, `condition_at_return`, plus shared audit fields.

**Integrity rule:** the catalog record must belong to the same vendor and
vendor location as the parent contract.

### `Rental_Lifecycle_Events`

`event_id` (PK), `contract_id` (FK → `Rental_Contracts.contract_id`),
`event_type`, `event_timestamp`, `performed_by_staff_id` (FK →
`ACME_Staff.staff_id`, optional for system events), `old_end_date` (optional),
`new_end_date` (optional), `reason_code` (optional), `notes`,
`source_system`, `source_event_id` (unique), plus shared audit fields.

Allowed `event_type`: `Rent`, `Extend`, `Cancel`, `Return Requested`,
`Pickup Confirmed`, `Return`, `Alert`, `Inspection`, `Case Updated`.

### `Rental_Monitoring_Flags`

`flag_id` (PK), `contract_id` (FK → `Rental_Contracts.contract_id`),
`flag_type`, `flag_date`, `target_date`, `days_before_end`, `severity`,
`status`, `assigned_to_staff_id` (FK → `ACME_Staff.staff_id`, optional),
`resolution_notes`, `alert_window`, `alert_sent_at` (optional), plus shared
audit fields.

Allowed `flag_type`: `FourWeekExpiry`, `SevenDayExpiry`, `OneDayExpiry`,
`Overdue`, `DamageRisk`.

**Alert uniqueness rule:** only one record may exist for
`(contract_id, alert_window, target_date)`. Use `28`, `7`, `1`, and `0` for
the four-week, seven-day, one-day, and due-date alerts.

### `Pickup_Return_Requests`

`pickup_return_request_id` (PK), `contract_id` (FK →
`Rental_Contracts.contract_id`), `vendor_id` (FK → `Vendor_Master.vendor_id`),
`vendor_location_id` (FK → `Vendor_Locations.vendor_location_id`),
`request_type`, `requested_date`, `preferred_pickup_date`,
`scheduled_pickup_date` (optional), `vendor_confirmation_number` (unique,
optional), `request_status`, `inspection_result` (optional), `damage_flags`
(optional), `equipment_returned_date` (optional), plus shared audit fields.

Allowed `request_type`: `Standard Pickup`, `Immediate Pickup`, `Return`.
Allowed `request_status`: `Requested`, `Scheduled`, `Confirmed`, `Completed`,
`Cancelled`, `Failed`.

## Seed order and test scenarios

1. Seed locations before staff; initially leave cyclic manager/site-contact
   references empty, then update them after staff records exist.
2. Seed departments, staff, vendors, vendor locations, and equipment catalog.
3. Seed requests, then contracts, rental items, events, flags, and pickup/
   return records.
4. Include correlated examples for: new active rental, 28-day flag, 7-day
   alert, approved extension, cancelled contract, standard return, immediate
   pickup, damage inspection, and overdue rental.
