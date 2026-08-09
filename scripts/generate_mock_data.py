#!/usr/bin/env python3
"""Generate deterministic, human-readable EquipmentRENTAL LCversion mock data."""

from __future__ import annotations

import csv
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


PROJECT = "EquipmentRENTAL"
VERSION = "LCversion"
AS_OF = date(2026, 8, 9)
HISTORY_START = date(2024, 8, 9)
FORECAST_END = date(2029, 2, 9)
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "mock" / VERSION
RNG = random.Random(20260809)


def iso(day: date) -> str:
    return day.isoformat()


def timestamp(day: date, hour: int = 12) -> str:
    return datetime(day.year, day.month, day.day, hour, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    path = OUTPUT / f"{PROJECT}_{VERSION}_{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    locations = [
        ("LOC-CHI-001", "Chicago Plant", "1850 W Fulton St", "Chicago", "IL", "60612"),
        ("LOC-DAL-001", "Dallas Yard", "1020 Riverfront Blvd", "Dallas", "TX", "75207"),
        ("LOC-ATL-001", "Atlanta Field Office", "2300 Marietta Blvd", "Atlanta", "GA", "30318"),
        ("LOC-PHX-001", "Phoenix Operations Center", "4550 W Roosevelt St", "Phoenix", "AZ", "85043"),
    ]
    acme_locations = [
        {"location_id": key, "location_name": name, "address_line1": address, "city": city,
         "state": state, "postal_code": postal, "site_contact_staff_id": "", "status": "Active"}
        for key, name, address, city, state, postal in locations
    ]
    departments = [
        ("DEP-001", "Operations", "CC-4100", "Industrial Services", "LOC-CHI-001"),
        ("DEP-002", "Facilities", "CC-4200", "Corporate Services", "LOC-DAL-001"),
        ("DEP-003", "Field Services", "CC-4300", "Industrial Services", "LOC-ATL-001"),
        ("DEP-004", "Capital Projects", "CC-4400", "Project Delivery", "LOC-PHX-001"),
    ]
    first_names = ["Avery", "Blake", "Casey", "Devon", "Emerson", "Finley", "Gray", "Harper", "Jordan", "Kai", "Logan", "Morgan", "Nico", "Oakley", "Parker", "Quinn"]
    last_names = ["Bennett", "Carter", "Diaz", "Ellis", "Foster", "Garcia", "Hughes", "Irwin", "Jones", "Kim", "Lewis", "Morgan", "Nguyen", "Owens", "Patel", "Reed"]
    staff: list[dict[str, object]] = []
    for index in range(16):
        dept = departments[index // 4]
        role = ["Requester", "Manager", "Procurement", "Case Worker"][index % 4]
        first, last = first_names[index], last_names[index]
        staff.append({
            "staff_id": f"STF-{index + 1:03d}", "first_name": first, "last_name": last,
            "email": f"{first.lower()}.{last.lower()}@acme.example", "role": role,
            "department_id": dept[0], "location_id": dept[4],
            "approval_limit": "10000.00" if role == "Manager" else ("100000.00" if role == "Procurement" else "0.00"),
            "status": "Active",
        })
    managers = {d[0]: staff[(i * 4) + 1]["staff_id"] for i, d in enumerate(departments)}
    for row, dept in zip(acme_locations, departments):
        row["site_contact_staff_id"] = managers[dept[0]]
    department_rows = [{
        "department_id": dept_id, "department_name": name, "cost_center": cost_center,
        "business_unit": unit, "manager_staff_id": managers[dept_id],
        "default_location_id": location_id, "status": "Active",
    } for dept_id, name, cost_center, unit, location_id in departments]

    vendor_defs = [
        ("VND-001", "United Rentals Demonstration", "united-rentals-mock"),
        ("VND-002", "Sunbelt Demonstration", "sunbelt-mock"),
        ("VND-003", "Herc Rentals Portal Demonstration", "herc-portal-mock"),
    ]
    vendors = [{"vendor_id": vid, "vendor_name": name, "vendor_type": "Equipment Rental",
                "support_email": f"support@{system}.example", "support_phone": f"+1-555-01{index}0",
                "api_system_name": system, "status": "Active"}
               for index, (vid, name, system) in enumerate(vendor_defs, start=1)]
    vendor_locations: list[dict[str, object]] = []
    cities = [("Chicago", "IL", "60607"), ("Dallas", "TX", "75212")]
    for vendor_index, (vendor_id, vendor_name, _) in enumerate(vendor_defs, start=1):
        for loc_index, (city, state, postal) in enumerate(cities, start=1):
            key = f"VLOC-{vendor_index:02d}-{loc_index:02d}"
            vendor_locations.append({
                "vendor_location_id": key, "vendor_id": vendor_id,
                "location_name": f"{vendor_name.split()[0]} {city} Branch", "address_line1": f"{100 + vendor_index * 10 + loc_index} Rental Way",
                "city": city, "state": state, "postal_code": postal,
                "contact_name": f"{city} Rental Desk", "contact_email": f"{city.lower()}.{vendor_index}@vendor.example",
                "contact_phone": f"+1-555-02{vendor_index}{loc_index}0", "status": "Active",
            })
    equipment_types = [
        ("Lift", "60-ft Boom Lift", "JLG 600S", 485, 1455, 4850, 1),
        ("Generator", "Towable Generator", "CAT XQ35", 210, 630, 2100, 2),
        ("Forklift", "Rough Terrain Forklift", "JCB 930", 325, 975, 3250, 1),
        ("Excavator", "Mini Excavator", "CAT 305", 395, 1185, 3950, 1),
    ]
    catalog: list[dict[str, object]] = []
    for loc_index, location in enumerate(vendor_locations, start=1):
        for type_index, (category, name, model, daily, weekly, monthly, quantity) in enumerate(equipment_types, start=1):
            catalog.append({
                "vendor_equipment_id": f"VEQ-{loc_index:02d}-{type_index:02d}", "vendor_id": location["vendor_id"],
                "vendor_location_id": location["vendor_location_id"], "equipment_category": category,
                "equipment_name": name, "model": model, "daily_rate": f"{daily:.2f}",
                "weekly_rate": f"{weekly:.2f}", "monthly_rate": f"{monthly:.2f}",
                "available_quantity": quantity, "total_quantity": quantity, "availability_status": "Available",
                "replacement_value": f"{daily * 80:.2f}", "currency_code": "USD", "last_availability_sync_at": timestamp(AS_OF),
            })

    requests: list[dict[str, object]] = []
    contracts: list[dict[str, object]] = []
    items: list[dict[str, object]] = []
    events: list[dict[str, object]] = []
    flags: list[dict[str, object]] = []
    pickups: list[dict[str, object]] = []
    timeline = [HISTORY_START + timedelta(days=offset) for offset in range(0, (AS_OF - HISTORY_START).days, 9)]
    future_timeline = [AS_OF + timedelta(days=21 + offset * 25) for offset in range(36)]
    for index, start in enumerate(timeline + future_timeline, start=1):
        future = start > AS_OF
        dept = departments[(index - 1) % len(departments)]
        requester = next(row for row in staff if row["department_id"] == dept[0] and row["role"] == "Requester")
        approver = next(row for row in staff if row["department_id"] == dept[0] and row["role"] in {"Manager", "Procurement"})
        equipment = catalog[(index - 1) % len(catalog)]
        vendor_location = next(row for row in vendor_locations if row["vendor_location_id"] == equipment["vendor_location_id"])
        request_id, contract_id, correlation = f"RR-2026-{index:04d}", f"RC-2026-{index:04d}", f"ER-2026-{index:06d}"
        duration = 14 + (index % 4) * 7
        end = start + timedelta(days=duration)
        if future:
            status = "Draft"
            request_status = "Submitted" if index % 3 == 0 else "Approved"
        elif index % 17 == 0:
            status, request_status = "Cancelled", "Cancelled"
        elif end < AS_OF - timedelta(days=10):
            status, request_status = "Closed", "Approved"
        elif end < AS_OF:
            status, request_status = "Returned", "Approved"
        elif index % 7 == 0:
            status, request_status = "Extended", "Approved"
            end += timedelta(days=21)
        else:
            status, request_status = "Active", "Approved"
        created = start - timedelta(days=4)
        requests.append({
            "rental_request_id": request_id, "request_number": f"REQ-{start.year}-{index:04d}",
            "requested_by_staff_id": requester["staff_id"], "department_id": dept[0], "delivery_location_id": dept[4],
            "request_date": iso(created), "needed_start_date": iso(start), "needed_end_date": iso(end),
            "business_reason": ["Planned maintenance", "Plant outage support", "Field repair", "Capital project"][index % 4],
            "estimated_cost": f"{float(equipment['weekly_rate']) * max(1, duration // 7):.2f}", "currency_code": "USD",
            "request_status": request_status, "approved_by_staff_id": approver["staff_id"] if request_status == "Approved" else "",
            "approval_date": iso(start - timedelta(days=2)) if request_status == "Approved" else "",
            "created_at": timestamp(created), "updated_at": timestamp(start), "correlation_id": correlation,
        })
        if request_status != "Approved":
            continue
        contracts.append({
            "contract_id": contract_id, "rental_request_id": request_id, "vendor_id": equipment["vendor_id"],
            "vendor_location_id": equipment["vendor_location_id"], "department_id": dept[0],
            "requested_by_staff_id": requester["staff_id"], "approved_by_staff_id": approver["staff_id"] if request_status == "Approved" else "",
            "delivery_location_id": dept[4], "billing_location_id": dept[4], "contract_number": f"{vendor_location['vendor_id']}-CN-{start.year}-{index:04d}",
            "start_date": iso(start), "end_date": iso(end), "original_end_date": iso(start + timedelta(days=duration)),
            "total_estimated_price": f"{float(equipment['weekly_rate']) * max(1, duration // 7):.2f}",
            "actual_total_price": "" if future else f"{float(equipment['weekly_rate']) * max(1, duration // 7):.2f}",
            "tax_amount": "0.00", "damage_charge_amount": "0.00", "currency_code": "USD", "billing_frequency": "Weekly",
            "status": status, "uipath_case_id": f"CASE-ER-{index:06d}" if index % 3 != 0 else "",
            "source_event_id": f"VENDOR-EVT-{index:06d}", "created_at": timestamp(created), "updated_at": timestamp(min(end, AS_OF) if not future else created),
            "correlation_id": correlation,
        })
        items.append({
            "rental_item_id": f"RIT-{index:06d}", "contract_id": contract_id,
            "vendor_equipment_id": equipment["vendor_equipment_id"], "equipment_category": equipment["equipment_category"],
            "equipment_name": equipment["equipment_name"], "model": equipment["model"], "serial_number": f"{equipment['model'].replace(' ', '')}-{index:05d}",
            "quantity": 1, "daily_rate": equipment["daily_rate"], "weekly_rate": equipment["weekly_rate"],
            "monthly_rate": equipment["monthly_rate"], "delivery_fee": "125.00", "pickup_fee": "125.00", "currency_code": "USD",
            "condition_at_delivery": "Good", "condition_at_return": "Pending" if status in {"Active", "Draft", "Extended"} else "Good",
            "created_at": timestamp(created), "updated_at": timestamp(min(end, AS_OF) if not future else created), "correlation_id": correlation,
        })
        event_types = [("Rent", start, "")]
        if status == "Extended": event_types.append(("Extend", start + timedelta(days=duration), "Project Delay"))
        if status == "Cancelled": event_types.append(("Cancel", start + timedelta(days=2), "No Longer Needed"))
        if status in {"Returned", "Closed"}:
            event_types.extend([("Return Requested", end - timedelta(days=2), ""), ("Pickup Confirmed", end - timedelta(days=1), ""), ("Return", end, "")])
            if index % 13 == 0:
                event_types.extend([("Inspection", end, "Damage Found"), ("Case Updated", end, "Damage Review Required")])
        for event_number, (event_type, event_date, reason) in enumerate(event_types, start=1):
            events.append({
                "event_id": f"RLE-{index:06d}-{event_number}", "contract_id": contract_id, "event_type": event_type,
                "event_timestamp": timestamp(event_date), "performed_by_staff_id": requester["staff_id"],
                "old_end_date": iso(start + timedelta(days=duration)) if event_type == "Extend" else "",
                "new_end_date": iso(end) if event_type == "Extend" else "", "reason_code": reason,
                "notes": f"{event_type} event for {contract_id}", "source_system": "EquipmentRENTAL_LCversion",
                "source_event_id": f"{correlation}-{event_number}", "created_at": timestamp(event_date), "updated_at": timestamp(event_date), "correlation_id": correlation,
            })
        if status in {"Returned", "Closed"}:
            immediate_pickup = index % 11 == 0
            damage_found = index % 13 == 0
            pickups.append({
                "pickup_return_request_id": f"PRR-{index:06d}", "contract_id": contract_id, "vendor_id": equipment["vendor_id"],
                "vendor_location_id": equipment["vendor_location_id"], "request_type": "Immediate Pickup" if immediate_pickup else "Standard Pickup", "requested_date": iso(end - timedelta(days=3)),
                "preferred_pickup_date": iso(end - timedelta(days=1)), "scheduled_pickup_date": iso(end),
                "vendor_confirmation_number": f"PICK-{index:06d}", "request_status": "Completed", "inspection_result": "Damage Found" if damage_found else "Pass",
                "damage_flags": "Damage" if damage_found else "None", "equipment_returned_date": iso(end), "created_at": timestamp(end - timedelta(days=3)),
                "updated_at": timestamp(end), "correlation_id": correlation,
            })
        if status in {"Active", "Extended"} and end <= AS_OF + timedelta(days=28):
            days = (end - AS_OF).days
            window = 28 if days >= 8 else (7 if days >= 2 else (1 if days >= 0 else 0))
            flag_type = {28: "FourWeekExpiry", 7: "SevenDayExpiry", 1: "OneDayExpiry", 0: "Overdue" if days < 0 else "OneDayExpiry"}[window]
            flags.append({
                "flag_id": f"FLG-{index:06d}-{window}", "contract_id": contract_id, "flag_type": flag_type,
                "flag_date": iso(AS_OF), "target_date": iso(end), "days_before_end": max(days, 0),
                "severity": "High" if days <= 1 else "Medium", "status": "Open", "assigned_to_staff_id": approver["staff_id"],
                "resolution_notes": "", "alert_window": window, "alert_sent_at": timestamp(AS_OF),
                "created_at": timestamp(AS_OF), "updated_at": timestamp(AS_OF), "correlation_id": correlation,
            })
            events.append({
                "event_id": f"RLE-{index:06d}-ALERT", "contract_id": contract_id, "event_type": "Alert",
                "event_timestamp": timestamp(AS_OF), "performed_by_staff_id": approver["staff_id"],
                "old_end_date": "", "new_end_date": "", "reason_code": flag_type,
                "notes": f"{flag_type} monitoring alert for {contract_id}", "source_system": "EquipmentRENTAL_LCversion",
                "source_event_id": f"{correlation}-ALERT", "created_at": timestamp(AS_OF), "updated_at": timestamp(AS_OF), "correlation_id": correlation,
            })

    availability: list[dict[str, object]] = []
    total_days = (FORECAST_END - AS_OF).days + 1
    for equipment in catalog:
        total = int(equipment["total_quantity"])
        for offset in range(total_days):
            day = AS_OF + timedelta(days=offset)
            reserved = 1 if total > 1 and (offset + int(equipment["vendor_equipment_id"].split("-")[1])) % 23 in {0, 1, 2} else 0
            out = 1 if total > 1 and offset % 181 == 0 else 0
            available = total - reserved - out
            availability.append({
                "availability_id": f"AVL-{equipment['vendor_equipment_id']}-{day.strftime('%Y%m%d')}",
                "vendor_equipment_id": equipment["vendor_equipment_id"], "availability_date": iso(day),
                "total_quantity": total, "reserved_quantity": reserved, "available_quantity": available,
                "out_of_service_quantity": out, "availability_status": "Out of Service" if available == 0 else ("Reserved" if available < total else "Available"),
                "source_system": "EquipmentRENTAL_LCversion", "correlation_id": f"ER-AVAIL-{day.strftime('%Y%m%d')}", "created_at": timestamp(AS_OF),
            })

    write_csv("ACME_Departments", department_rows)
    write_csv("ACME_Staff", staff)
    write_csv("ACME_Locations", acme_locations)
    write_csv("Vendor_Master", vendors)
    write_csv("Vendor_Locations", vendor_locations)
    write_csv("Vendor_Equipment_Catalog", catalog)
    write_csv("Rental_Requests", requests)
    write_csv("Rental_Contracts", contracts)
    write_csv("Rental_Equipment_Items", items)
    write_csv("Rental_Lifecycle_Events", events)
    write_csv("Rental_Monitoring_Flags", flags)
    write_csv("Pickup_Return_Requests", pickups)
    write_csv("Vendor_Equipment_Availability", availability)
    (OUTPUT / "README.md").write_text(
        f"# {PROJECT} {VERSION} Mock Dataset\\n\\n"
        f"- History: {HISTORY_START.isoformat()} through {AS_OF.isoformat()}\\n"
        f"- Availability forecast: {AS_OF.isoformat()} through {FORECAST_END.isoformat()}\\n"
        "- Every CSV filename uses the project/version prefix for human traceability.\\n"
        "- Run `python3 scripts/generate_mock_data.py` to recreate this deterministic dataset.\\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
