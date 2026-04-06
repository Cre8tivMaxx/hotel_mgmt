# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`hotel_mgmt` is a Frappe/ERPNext custom app for hotel property management. It depends on ERPNext (`required_apps = ["erpnext"]`) and runs on Frappe v15+ with Python 3.10+.

## Common Commands

```bash
# Run the development server
cd /home/frappe/frappe-bench
bench start

# Run all tests for this app
bench --site <site-name> run-tests --app hotel_mgmt

# Run a single test file
bench --site <site-name> run-tests --module hotel_mgmt.hotel.doctype.reservation.test_reservation

# Run a specific test class/method
bench --site <site-name> run-tests --module hotel_mgmt.hotel.doctype.reservation.test_reservation --test test_method_name

# Apply database migrations after doctype changes
bench --site <site-name> migrate

# Export fixtures to JSON (after changing Custom Fields, Property Setters, etc.)
bench --site <site-name> export-fixtures --app hotel_mgmt

# Lint
ruff check hotel_mgmt/
ruff format hotel_mgmt/
```

## Architecture

### Module Structure

The app has one primary module: **Hotel** (`hotel_mgmt/hotel/`). There is also a legacy `hotel_management/` module with a duplicate Hotel Settings doctype — the active one is under `hotel/`.

### Core DocTypes

- **Reservation** — Central document. Tracks check-in/check-out dates, room assignment, nightly rate, and total amount. Uses a Workflow (fixture) for status transitions (Confirmed → Checked-in → Checked-out, etc.).
- **Room** — Tracks room status (Available, Occupied, Dirty), clean status, and room type. Has custom list view indicators via `public/js/room_indicator.js`.
- **Housekeeping** — Submittable. Linked to a Room. On submit, updates the Room's status/clean_status.
- **Hotel Contract** — Manages allotment and rate agreements with companies/travel agents. Has a workflow (Active → Expired).
- **Rate Code / Rate Detail / Rate Plan Detail** — Rate management hierarchy.
- **Room Type / Room Feature** — Room classification and amenities.
- **Guest Profile / Company Profile / Group Profile / Travel Agent Profile** — Guest and partner profiles.
- **Restaurant Order / Restaurant Table** — Basic restaurant management.

### Business Logic Location

Most server-side business logic lives in **`hotel_mgmt/api.py`**, wired through `doc_events` in hooks.py — not in individual DocType controllers (which are all `pass`). This is the key architectural pattern:

- `reservation_validate` — Date validation, nights calculation, total amount computation
- `reservation_on_submit` (hooked to `after_save`) — Room status updates, auto-creates Housekeeping records
- `reservation_on_cancel` — Frees up rooms
- `housekeeping_on_submit` — Syncs Room status from Housekeeping condition
- `check_in` / `make_sales_invoice` — Whitelisted API actions for UI buttons
- `release_allotments` / `expire_hotel_contracts` — Daily scheduled tasks

### Customer Customization

`hotel_mgmt/custom/customer.py` hooks into the ERPNext **Customer** doctype via `doc_events` (before_insert, validate, before_save). Currently commented out — was intended to format customer_name from custom first/last name fields.

### Fixtures

Exported via `bench export-fixtures`. Includes: Custom Field, Property Setter, Workspace, Workflow, Client Script, Room Feature, and the Room DocType itself. Fixture JSON files are in `hotel_mgmt/fixtures/`.

### Frontend

- `public/js/hotel.js` — Global styling (banner image, background)
- `public/js/guest_profile.js` — Guest profile client-side logic
- `public/js/room_indicator.js` — Custom list view color indicators for Room
- `public/css/dashboard.css` — Dashboard styling

### Reports

- **Availability** (`hotel/report/availability/`) — Script report showing room availability by status and type.

## Code Style

- **Indentation:** Tabs (configured in ruff)
- **Line length:** 110 chars
- **Formatter/Linter:** ruff (see `pyproject.toml` for full config)
- **JS:** eslint + prettier (via pre-commit)
- **Quote style:** Double quotes
