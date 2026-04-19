import os

from data import market_records, actual_records
from validators import validate_records
from part1_unmatched import settle_unmatched_table
from part2_deviation import settle_deviation_merged_table
from price_cal import PriceProvider


TARIFF_TARGET_YEAR = int(os.getenv("TARIFF_TARGET_YEAR", "2026"))
SIM_SEASON = os.getenv("SIM_SEASON", "").strip().lower() or None
TARIFF_AGG = os.getenv("TARIFF_AGG", "median").strip().lower()


PART1_DISPLAY_FIELDS = [
    "household_id",
    "timeslot",
    "unmatched_buy_kwh",
    "unmatched_sell_kwh",
    "grid_trade_direction",
    "penalty_amount",
    "final_settlement_unit_price",
    "unmatched_net_amount",
]

PART2_DISPLAY_FIELDS = [
    "household_id",
    "timeslot",
    "deviation_order_kwh",
    "deviation_type",
    "internal_trade_direction",
    "internal_matched_kwh",
    "counterparty_list",
    "final_grid_trade_direction",
    "final_grid_kwh",
    "penalty_amount",
    "final_settlement_unit_price",
    "deviation_net_amount",
]


def filter_output(result):
    return {
        "part_1_unmatched_table": [
            {k: row[k] for k in PART1_DISPLAY_FIELDS if k in row}
            for row in result["part_1_unmatched_table"]
        ],
        "part_2_deviation_merged_table": [
            {k: row[k] for k in PART2_DISPLAY_FIELDS if k in row}
            for row in result["part_2_deviation_merged_table"]
        ],
    }


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

    return {
        "part_1_unmatched_table": settle_unmatched_table(
            market_records_final,
            price_provider,
        ),
        "part_2_deviation_merged_table": settle_deviation_merged_table(
            market_records_final,
            actual_records_final,
            price_provider,
        ),
    }


if __name__ == "__main__":
    full_result = final_settle(market_records, actual_records)
    display = filter_output(full_result)

    print("=== Part 1: Unmatched Settlement ===")
    for row in display["part_1_unmatched_table"]:
        print(row)

    print("\n=== Part 2: Deviation Settlement ===")
    for row in display["part_2_deviation_merged_table"]:
        print(row)