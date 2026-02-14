"""
Medicaid Analysis — Number & Currency Formatting
"""

import matplotlib.ticker as mticker


def usd_fmt(x, _=None):
    """Format number as compact USD string ($1.2B, $3.4M, $5.6K)."""
    if abs(x) >= 1e9:
        return f"${x/1e9:.1f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:.1f}M"
    if abs(x) >= 1e3:
        return f"${x/1e3:.1f}K"
    return f"${x:,.0f}"


def usd(ax, axis="y"):
    """Apply USD formatter to a matplotlib axis."""
    fmt = mticker.FuncFormatter(usd_fmt)
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def num_fmt(x, _=None):
    """Format number as compact string (1.2B, 3.4M, 5.6K)."""
    if abs(x) >= 1e9:
        return f"{x/1e9:.1f}B"
    if abs(x) >= 1e6:
        return f"{x/1e6:.1f}M"
    if abs(x) >= 1e3:
        return f"{x/1e3:.1f}K"
    return f"{x:,.0f}"


def pct_fmt(x, _=None):
    """Format number as percentage string."""
    return f"{x:.1f}%"
