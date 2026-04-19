import sys
from pathlib import Path
import pandas as pd

REPO_ROOT = Path("/repos/market_operator")
sys.path.insert(0, str(REPO_ROOT))

from tariff import load_tou_profile, load_fit_profile


class PriceProvider:
    def __init__(
        self,
        tou_csv: str = "csv_agile_L_South_Western_England.csv",
        fit_csv: str = "csv_agileoutgoing_L_South_Western_England.csv",
        target_year: int = 2025,
        season: str | None = None,
        agg: str = "median",
    ):
        self.tou_profile = load_tou_profile(
            csv_path=tou_csv,
            target_year=target_year,
            season=season,
            agg=agg,
        )
        self.fit_profile = load_fit_profile(
            csv_path=fit_csv,
            target_year=target_year,
            season=season,
            agg=agg,
        )

    def get_prices(self, timeslot: str) -> dict[str, float]:
        ts = pd.to_datetime(timeslot, errors="coerce")

        if pd.isna(ts):
            hour_key = str(timeslot).strip()
            if ":" not in hour_key:
                raise ValueError(f"Invalid or unsupported timeslot: {timeslot}")
            hour = int(hour_key.split(":")[0])
        else:
            hour = int(ts.hour)

        return {
            "buy": float(self.tou_profile.get_price(hour)),
            "sell": float(self.fit_profile.get_price(hour)),
        }