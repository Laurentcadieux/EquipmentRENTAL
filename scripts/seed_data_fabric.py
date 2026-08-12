#!/usr/bin/env python3
"""Create and seed the approved EquipmentRENTAL LCversion Data Fabric schema."""
from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from pathlib import Path

FOLDER_KEY = os.environ.get("UIPATH_DATA_FABRIC_FOLDER_KEY", "11b28f3b-294e-4593-aba1-a5079c54e7aa")
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "mock" / "LCversion"
ENTITIES = [
    "ACME_Locations", "ACME_Departments", "ACME_Staff", "Vendor_Master",
    "Vendor_Locations", "Vendor_Equipment_Catalog", "Rental_Requests",
    "Rental_Contracts", "Rental_Equipment_Items", "Rental_Lifecycle_Events",
    "Rental_Monitoring_Flags", "Pickup_Return_Requests", "Vendor_Equipment_Availability",
]
RELATIONS = {
    "ACME_Departments": {"manager_staff_id": "ACME_Staff", "default_location_id": "ACME_Locations"},
    "ACME_Staff": {"department_id": "ACME_Departments", "location_id": "ACME_Locations"},
    "ACME_Locations": {"site_contact_staff_id": "ACME_Staff"},
    "Vendor_Locations": {"vendor_id": "Vendor_Master"},
    "Vendor_Equipment_Catalog": {"vendor_id": "Vendor_Master", "vendor_location_id": "Vendor_Locations"},
    "Vendor_Equipment_Availability": {"vendor_equipment_id": "Vendor_Equipment_Catalog"},
    "Rental_Requests": {"requested_by_staff_id": "ACME_Staff", "department_id": "ACME_Departments", "delivery_location_id": "ACME_Locations", "approved_by_staff_id": "ACME_Staff"},
    "Rental_Contracts": {"rental_request_id": "Rental_Requests", "vendor_id": "Vendor_Master", "vendor_location_id": "Vendor_Locations", "department_id": "ACME_Departments", "requested_by_staff_id": "ACME_Staff", "approved_by_staff_id": "ACME_Staff", "delivery_location_id": "ACME_Locations", "billing_location_id": "ACME_Locations"},
    "Rental_Equipment_Items": {"contract_id": "Rental_Contracts", "vendor_equipment_id": "Vendor_Equipment_Catalog"},
    "Rental_Lifecycle_Events": {"contract_id": "Rental_Contracts", "performed_by_staff_id": "ACME_Staff"},
    "Rental_Monitoring_Flags": {"contract_id": "Rental_Contracts", "assigned_to_staff_id": "ACME_Staff"},
    "Pickup_Return_Requests": {"contract_id": "Rental_Contracts", "vendor_id": "Vendor_Master", "vendor_location_id": "Vendor_Locations"},
}
DISPLAY_FIELDS = {
    "ACME_Staff": "Email", "ACME_Departments": "DepartmentName", "ACME_Locations": "LocationName",
    "Vendor_Master": "VendorName", "Vendor_Locations": "LocationName", "Vendor_Equipment_Catalog": "EquipmentName",
    "Rental_Requests": "RequestNumber", "Rental_Contracts": "ContractNumber",
}


def run(*args: str) -> dict:
    print(f"Running: {' '.join(args)}", flush=True)
    command = ["uip", *args, "--output", "json"]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        print(result.stderr, flush=True)
        print(result.stdout, flush=True)
        raise RuntimeError(f"{' '.join(command)}\n{result.stderr}\n{result.stdout}")
    payload = json.loads(result.stdout)
    if payload.get("Result") != "Success":
        raise RuntimeError(json.dumps(payload, indent=2))
    return payload["Data"]


def list_all_records(entity_id: str) -> list[dict]:
    """Read every record through the cursor-free pagination surface."""
    offset = 0
    items: list[dict] = []
    while True:
        page = run("df", "records", "list", entity_id, "--folder-key", FOLDER_KEY, "--limit", "200", "--offset", str(offset))
        page_items = page["Items"]
        items.extend(page_items)
        if not page.get("HasNextPage"):
            return items
        offset += len(page_items)


def field_name(column: str) -> str:
    return "".join(part.capitalize() for part in column.split("_"))


def field_type(column: str) -> str:
    if column.endswith("_date") or column in {"request_date", "start_date", "end_date", "original_end_date", "needed_start_date", "needed_end_date", "flag_date", "target_date", "preferred_pickup_date", "scheduled_pickup_date", "equipment_returned_date", "approval_date"}:
        return "DATE"
    if column.endswith("_at") or column == "event_timestamp":
        return "DATETIME_WITH_TZ"
    if any(token in column for token in ("rate", "price", "fee", "amount", "value", "limit")):
        return "DECIMAL"
    if column in {"quantity", "days_before_end", "alert_window", "reserved_quantity", "available_quantity", "total_quantity", "out_of_service_quantity"}:
        return "DECIMAL"
    return "STRING"


def csv_rows(entity: str) -> list[dict[str, str]]:
    with (DATA / f"EquipmentRENTAL_LCversion_{entity}.csv").open(encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    existing = run("df", "entities", "list", "--native-only", "--folder-key", FOLDER_KEY)
    entity_ids = {item["Name"]: item["Id"] for item in existing if item["Name"] in ENTITIES}
    schemas: dict[str, list[str]] = {}
    for entity in ENTITIES:
        rows = csv_rows(entity)
        columns = list(rows[0])
        schemas[entity] = columns
        if entity in entity_ids:
            continue
        scalar_columns = [column for column in columns if column not in RELATIONS.get(entity, {})]
        fields = []
        for column in scalar_columns:
            name, kind = field_name(column), field_type(column)
            field = {"fieldName": name, "displayName": column, "type": kind, "isRequired": False}
            if kind == "STRING":
                field["lengthLimit"] = 512
            if kind == "DECIMAL":
                field["decimalPrecision"] = 0 if column in {"quantity", "days_before_end", "alert_window", "reserved_quantity", "available_quantity", "total_quantity", "out_of_service_quantity"} else 2
            if column.endswith("_id") and column not in {"correlation_id", "source_event_id"}:
                field["isUnique"] = True
            if column in {"email", "contract_number", "request_number", "availability_id", "source_event_id"}:
                field["isUnique"] = True
            fields.append(field)
        body = {"displayName": f"EquipmentRENTAL LCversion {entity}", "description": "EquipmentRENTAL LCversion approved mock dataset", "fields": fields}
        created = run("df", "entities", "create", entity, "--folder-key", FOLDER_KEY, "--body", json.dumps(body))
        entity_ids[entity] = created["Id"]
    metadata = {entity: run("df", "entities", "get", identifier, "--folder-key", FOLDER_KEY) for entity, identifier in entity_ids.items()}
    for entity, relation_columns in RELATIONS.items():
        existing_fields = {field["Name"] for field in metadata[entity]["Fields"]}
        additions = []
        for column, target in relation_columns.items():
            if field_name(column) in existing_fields:
                continue
            target_fields = {field["Name"]: field["Id"] for field in metadata[target]["Fields"]}
            additions.append({"fieldName": field_name(column), "displayName": column, "type": "RELATIONSHIP", "referenceEntityId": entity_ids[target], "referenceFieldId": target_fields[DISPLAY_FIELDS[target]], "referenceFolderKey": FOLDER_KEY, "isRequired": False})
        if additions:
            run("df", "entities", "update", entity_ids[entity], "--folder-key", FOLDER_KEY, "--body", json.dumps({"addFields": additions}))
    record_ids: dict[str, dict[str, str]] = {entity: {} for entity in ENTITIES}
    for entity in ENTITIES:
        rows = csv_rows(entity)
        key = next(column for column in schemas[entity] if column.endswith("_id") and column not in RELATIONS.get(entity, {}))
        name = field_name(key)
        listed = list_all_records(entity_ids[entity])
        record_ids[entity] = {item[name]: item["Id"] for item in listed}
        scalar_rows = []
        for row in rows:
            if row[key] in record_ids[entity]:
                continue
            scalar_rows.append({field_name(column): value for column, value in row.items() if column not in RELATIONS.get(entity, {}) and value != ""})
        for offset in range(0, len(scalar_rows), 200):
            run("df", "records", "insert", entity_ids[entity], "--folder-key", FOLDER_KEY, "--body", json.dumps(scalar_rows[offset:offset + 200]))
        if scalar_rows:
            listed = list_all_records(entity_ids[entity])
            record_ids[entity] = {item[name]: item["Id"] for item in listed}
    for entity, relation_columns in RELATIONS.items():
        rows = csv_rows(entity)
        key = next(column for column in schemas[entity] if column.endswith("_id") and column not in relation_columns)
        updates = []
        for row in rows:
            update = {"Id": record_ids[entity][row[key]]}
            for column, target in relation_columns.items():
                if row[column]:
                    update[field_name(column)] = record_ids[target][row[column]]
            if len(update) > 1:
                updates.append(update)
        for offset in range(0, len(updates), 200):
            run("df", "records", "update", entity_ids[entity], "--folder-key", FOLDER_KEY, "--body", json.dumps(updates[offset:offset + 200]))
    print(json.dumps({"folderKey": FOLDER_KEY, "entities": entity_ids, "recordCounts": {name: len(csv_rows(name)) for name in ENTITIES}}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise
