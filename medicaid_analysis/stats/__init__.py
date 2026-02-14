"""Statistics — Statistical Analysis Package."""

from .anomaly import s06_anomaly_detection
from .concentration import s08_concentration, s18_spending_deciles
from .correlations import s09_correlations
from .distribution_tests import s17_statistical_tests
from .power_law import s15_power_law
from .benfords_law import s31_benfords_law

__all__ = [
    "s06_anomaly_detection", "s08_concentration", "s09_correlations",
    "s15_power_law", "s17_statistical_tests", "s18_spending_deciles",
    "s31_benfords_law",
]
