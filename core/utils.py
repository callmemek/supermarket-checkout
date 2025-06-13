def round_half_up(value):
    from decimal import Decimal, ROUND_HALF_UP
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
