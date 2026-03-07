# Hotel Management

A Frappe/ERPNext custom app for hotel property management — covering reservations, room management, housekeeping, rate contracts, guest profiles, and more.

Built by [Sahl](mailto:info@sahl-tech.com).

## Features

- **Reservation Management** — Create and manage reservations with workflow-driven status transitions (Confirmed, Checked-in, Checked-out, Cancelled). Automatic nightly rate calculation, room assignment, and Sales Invoice generation on checkout.
- **Room Management** — Track room status (Available, Occupied, Dirty), room types, features/amenities, and clean status. Color-coded list view indicators for quick visibility.
- **Housekeeping** — Submittable housekeeping tasks linked to rooms. Automatically updates room status and clean condition on completion.
- **Hotel Contracts** — Manage allotment and rate agreements with companies and travel agents, with automatic expiration via scheduled tasks.
- **Rate Management** — Flexible rate hierarchy with Rate Codes, Rate Details, and Rate Plan Details.
- **Guest & Partner Profiles** — Dedicated profiles for individual guests, companies, groups, and travel agents.
- **Restaurant** — Basic restaurant order and table management.
- **Availability Report** — Script report showing room availability by status and type.

## Prerequisites

- Python 3.10+
- Frappe v15+
- ERPNext (required app)

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench --site <site-name> install-app hotel_mgmt
bench --site <site-name> migrate
```

## Development

### Running the Dev Server

```bash
cd /path/to/frappe-bench
bench start
```

### Running Tests

```bash
# All tests
bench --site <site-name> run-tests --app hotel_mgmt

# Single test module
bench --site <site-name> run-tests --module hotel_mgmt.hotel.doctype.reservation.test_reservation

# Specific test method
bench --site <site-name> run-tests --module hotel_mgmt.hotel.doctype.reservation.test_reservation --test test_method_name
```

### Linting & Formatting

```bash
ruff check hotel_mgmt/
ruff format hotel_mgmt/
```

### Exporting Fixtures

```bash
bench --site <site-name> export-fixtures --app hotel_mgmt
```

Fixtures include: Custom Field, Property Setter, Workspace, Workflow, Workflow State, Client Script, Room Feature, and the Room DocType.

## Architecture

The app has a single module — **Hotel** (`hotel_mgmt/hotel/`).

Most server-side business logic is centralized in **`hotel_mgmt/api.py`** and wired through `doc_events` in `hooks.py`, rather than in individual DocType controllers. Key functions include:

| Function | Purpose |
|---|---|
| `reservation_validate` | Date validation, nights calculation, total amount |
| `reservation_on_submit` | Room status updates, auto-create Housekeeping |
| `reservation_on_cancel` | Free up assigned rooms |
| `housekeeping_on_submit` | Sync room status from housekeeping condition |
| `check_in` | Whitelisted API for check-in action |
| `make_sales_invoice` | Whitelisted API for invoice generation |
| `release_allotments` | Daily scheduled task |
| `expire_hotel_contracts` | Daily scheduled task |

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/hotel_mgmt
pre-commit install
```

Pre-commit is configured to use the following tools:

- ruff
- eslint
- prettier
- pyupgrade

## License

MIT
