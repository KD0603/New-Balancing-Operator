import os

from data import market_records, actual_records
from validators import validate_records
from part1_unmatched import settle_unmatched_table
from part2_deviation import settle_deviation_merged_table
from price_cal import PriceProvider


TARIFF_TARGET_YEAR = int(os.getenv("TARIFF_TARGET_YEAR", "2026"))
SIM_SEASON = os.getenv("SIM_SEASON", "").strip().lower() or None
TARIFF_AGG = os.getenv("TARIFF_AGG", "median").strip().lower()


# Part 1: forecast settlement fields
FORECAST_DISPLAY_FIELDS = [
    "household_id",
    "timeslot",
    "unmatched_buy_kwh",
    "unmatched_sell_kwh",
    "grid_trade_direction",
    "grid_trade_kwh",
    "grid_price_used",
    "final_settlement_unit_price",
    "unmatched_net_amount",
]

# Part 2: real settlement fields
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


def filter_forecast(forecast_rows):
    return [
        {k: row[k] for k in FORECAST_DISPLAY_FIELDS if k in row}
        for row in forecast_rows
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

    forecast = settle_unmatched_table(market_records_final, price_provider)
    settlement = settle_deviation_merged_table(
        market_records_final,
        actual_records_final,
        price_provider,
    )

    return forecast, settlement


if __name__ == "__main__":
    forecast, settlement = final_settle(market_records, actual_records)

    print("=== Part 1: Forecast Balancing Settlement (prediction only, no real transactions) ===")
    for row in filter_forecast(forecast):
        print(row)

    print("\n=== Part 2: Final Balancing Settlement (real transactions) ===")
    for row in filter_output(settlement):
        print(row)
