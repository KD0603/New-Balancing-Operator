"""
Part 1: Unmatched Settlement (Day-Ahead Forecast).

The unmatched portions of market orders represent a FORECAST/ASSUMPTION only.
These are NOT real trades with the grid yet — actual grid settlement happens
in Part 2 after real deviations are resolved.

"""

from utils import round6


def settle_unmatched_table(market_records_u, price_provider):
    settle_res = []

    for record in market_records_u:
        household_id = record["household_id"]
        timeslot = record["timeslot"]
        unmatched_buy_kwh = round6(record.get("unmatched_buy_kwh", 0) or 0)
        unmatched_sell_kwh = round6(record.get("unmatched_sell_kwh", 0) or 0)

        prices = price_provider.get_prices(timeslot)
        grid_buy = round6(prices["buy"])
        grid_sell = round6(prices["sell"])

        trade_direction = ""
        grid_price_used = 0.0
        settled_kwh = 0.0
        gross_amount = 0.0
        unmatched_net_amount = 0.0 

        if unmatched_buy_kwh > 0:
            trade_direction = "buy_from_grid"
            grid_price_used = grid_buy
            settled_kwh = unmatched_buy_kwh
            gross_amount = round6(unmatched_buy_kwh * grid_buy)
            unmatched_net_amount = round6(-gross_amount)
        elif unmatched_sell_kwh > 0:
            trade_direction = "sell_to_grid"
            grid_price_used = grid_sell
            settled_kwh = unmatched_sell_kwh
            gross_amount = round6(unmatched_sell_kwh * grid_sell)
            unmatched_net_amount = round6(gross_amount)

        final_settlement_unit_price = 0.0
        if settled_kwh > 0:
            final_settlement_unit_price = round6(abs(unmatched_net_amount) / settled_kwh)

        settle_res.append(
            {
                "household_id": household_id,
                "timeslot": timeslot,
                "unmatched_buy_kwh": unmatched_buy_kwh,
                "unmatched_sell_kwh": unmatched_sell_kwh,
                "is_forecast": True,
                "grid_trade_direction": trade_direction,
                "grid_trade_kwh": settled_kwh,
                "grid_price_used": grid_price_used,
                "gross_grid_amount": gross_amount,
                "final_settlement_unit_price": final_settlement_unit_price,
                "unmatched_net_amount": unmatched_net_amount, # Forecast net amount — not a real settlement figure
            }
        )

    return settle_res
