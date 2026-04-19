import os

from data import market_records, actual_records
from validators import validate_records
from part2_deviation import settle_deviation_merged_table
from price_cal import PriceProvider


TARIFF_TARGET_YEAR = int(os.getenv("TARIFF_TARGET_YEAR", "2026"))
SIM_SEASON = os.getenv("SIM_SEASON", "").strip().lower() or None
TARIFF_AGG = os.getenv("TARIFF_AGG", "median").strip().lower()


SETTLEMENT_DISPLAY_FIELDS = [
    "household_id",
    "timeslot",
    "deviation_order_kwh",
    "unmatched_offset_kwh",
    "net_deviation_after_offset_kwh",
    "deviation_type",
    "internal_trade_direction",
    "internal_matched_kwh",
    "counterparty_list",
    "final_grid_trade_direction",
    "final_grid_kwh",
    "final_settlement_unit_price",
    "deviation_net_amount",
]


def filter_output(result):
    return [
        {k: row[k] for k in SETTLEMENT_DISPLAY_FIELDS if k in row}
        for row in result
    ]


def final_settle(
    market_records_final,
    actual_records_final,
    start=None,
    end=None,
):
    validate_records(market_records_final, actual_records_final)

    price_provider = PriceProvider(
        target_year=TARIFF_TARGET_YEAR,
        season=SIM_SEASON,
        agg=TARIFF_AGG,
    )

    return settle_deviation_merged_table(
        market_records_final,
        actual_records_final,
        price_provider,
    )


if __name__ == "__main__":
    result = final_settle(market_records, actual_records)
    display = filter_output(result)

    print("=== Final Settlement ===")
    for row in display:
        print(row)
