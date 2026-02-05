# --- Service-Funktionen für user_api.py ---
# --- path: /app/service/user_service.py ---

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from sqlalchemy import select
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Final

from app.db.orm_models.products import Product
from app.db.repositories.product.user_repository import get_department_by_name
from app.pydantic_models.user_models import CalculatorIn, CalculatorOut, CalculatorItemOut


HOURS_PER_DAY: Final[int] = 8
WORKDAYS_PER_YEAR: Final[int] = 220
ELECTRICITY_PRICE: Final[Decimal] = Decimal("0.35")


class UsageMode(str, Enum):
    mobile = "mobile"
    stationary = "stationary"


async def calculate_results_service(session: AsyncSession, *, payload: CalculatorIn) -> list[CalculatorOut]:
    # 1) Abteilung laden (inkl. Packages + Items + Product-Relation, per Repository)
    department = await get_department_by_name(session, department_name=payload.department)
    if not department:
        raise ValueError("Abteilung nicht gefunden.")

    # 2) usage_mode aus Request validieren
    try:
        request_usage_mode = UsageMode(payload.usage_mode)
    except ValueError:
        raise ValueError("Variable payload.usage_mode nicht in UsageMode.")

    results: list[CalculatorOut] = []

    for pkg in department.packages:
        # Nur Pakete mit gewünschtem usage_mode berücksichtigen
        if getattr(pkg, "usage_mode", None) != request_usage_mode:
            continue

        hardware_cost_per_seat = Decimal("0")
        power_total_watt = Decimal("0")
        items_out: list[CalculatorItemOut] = []

        for item in pkg.items:
            result = await session.execute(
                select(with_polymorphic(Product, "*")).where(with_polymorphic(Product, "*").id == item.product_id)
            )
            product = result.scalar_one()

            quantity = item.quantity

            unit_price: Decimal = product.price
            hardware_cost_per_seat += unit_price * quantity

            # Stromverbrauch falls vorhanden (nicht jedes Produkt hat power_usage)
            power_usage = getattr(product, "power_usage", None)
            if power_usage is not None:
                power_total_watt += power_usage * quantity
            else:
                # Für die Ausgabe trotzdem einen Wert haben
                power_usage = Decimal("0")

            price_rounded = unit_price.quantize(Decimal("0.01"))  # 2 Nachkommastellen

            power_usage_rounded: Decimal | None = None
            if power_usage is not None and power_usage != 0:
                power_usage_rounded = power_usage.quantize(Decimal("0.001"))

            # Item fürs Frontend
            items_out.append(
                CalculatorItemOut(
                    product_name=product.name,
                    price=price_rounded,
                    power_usage=power_usage_rounded,
                )
            )

        # 5) Energiekosten berechnen (pro Arbeitsplatz)
        power_kw = power_total_watt / Decimal("1000")  # Watt → kW
        energy_kwh_year = power_kw * HOURS_PER_DAY * WORKDAYS_PER_YEAR
        energy_cost_per_seat = energy_kwh_year * ELECTRICITY_PRICE

        # 6) Auf Teamgröße hochskalieren
        members = payload.team_members

        hardware_cost_total = hardware_cost_per_seat * members
        energy_cost_total = energy_cost_per_seat * members

        hardware_cost_member_rounded = hardware_cost_per_seat.quantize(Decimal("0.01"))
        hardware_cost_total_rounded = hardware_cost_total.quantize(Decimal("0.01"))
        energy_cost_member_rounded = energy_cost_per_seat.quantize(Decimal("0.01"))
        energy_cost_total_rounded = energy_cost_total.quantize(Decimal("0.01"))

        # 7) Output-DTO für dieses Paket bauen
        results.append(
            CalculatorOut(
                department_name=department.name,
                tier=pkg.tier,
                usage_mode=request_usage_mode,
                items=items_out,
                members=members,
                os=payload.os,
                include_software=payload.included_software,
                hardware_cost_member=hardware_cost_member_rounded,
                hardware_cost_total=hardware_cost_total_rounded,
                energy_cost_member=energy_cost_member_rounded,
                energy_cost_total=energy_cost_total_rounded,
            )
        )

    return results
