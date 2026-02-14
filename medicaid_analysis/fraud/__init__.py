"""Fraud Detection — Fraud Analysis Package."""

from .upcoding import s33_upcoding_detection
from .velocity import s34_billing_velocity_anomalies
from .phantom import s35_phantom_billing
from .clustering import s36_provider_clustering
from .cost_outliers import s37_cost_outliers_by_procedure
from .relationships import s38_billing_servicing_anomalies
from .temporal import s39_temporal_anomalies
from .composite import s40_composite_fraud_score

__all__ = [
    "s33_upcoding_detection", "s34_billing_velocity_anomalies",
    "s35_phantom_billing", "s36_provider_clustering",
    "s37_cost_outliers_by_procedure", "s38_billing_servicing_anomalies",
    "s39_temporal_anomalies", "s40_composite_fraud_score",
]
