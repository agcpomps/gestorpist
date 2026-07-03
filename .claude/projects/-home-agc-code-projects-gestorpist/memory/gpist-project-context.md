---
name: gpist-project-context
description: GPIST domain/workflow facts — government app, user provisioning, departamentos hub, projectos constraints
metadata:
  type: project
---

GPIST-DOP is an internal **government** management app for the Gabinete de Serviços Técnicos e Infraestruturas (Angola; currency AOA / "Kz").

Workflow & constraints the user stated:
- The **admin provisions users** (no public sign-up).
- [templates/departamentos.html](templates/departamentos.html) is the central **launcher/hub** — a menu of modules ("até seria apps"): Obras Públicas (empresas), Gestão Urbanística (gupagamentos), Conservação Infraestruturas (taxas), Tickets, Projectos, and RH (em construção).
- The **`ticket`** app is the most mature module.
- **`projectos`** is a project manager split by department.
- **Canonical `Department` lives in `accounts`** (since July 2026): `accounts.Department`, with `CustomUser.departamento` as FK. The old `ticket.Department` and `projectos.Department` models were merged into it. Department-based permissions: `CustomUser.manages(department)` — staff manages everything, others only their own department's records (tickets management panel, project edit/delete). Only staff creates departments.
- **No per-project budget/money**: it's a government app where the orçamento comes from central government, so do not add budget/MoneyField to projects.
