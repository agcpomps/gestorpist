from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def kwanza(value):
    """Format a numeric value as Angolan Kwanza, e.g. ``Kz 250.000,00``.

    Locale-independent so it stays consistent regardless of the active
    LANGUAGE_CODE: groups thousands with ``.`` and uses ``,`` for decimals
    (pt-AO convention). Non-numeric values are returned unchanged.
    """
    try:
        amount = Decimal(value or 0)
    except (TypeError, ValueError, InvalidOperation):
        return value

    # Format with English separators, then swap to pt-AO style.
    formatted = f"{amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"Kz {formatted}"
