"""Custom Jinja2 filters for the storage_health_check role."""

from __future__ import annotations

_DISPLAY_UNITS = (
    (1024**4, "TiB"),
    (1024**3, "GiB"),
    (1024**2, "MiB"),
    (1024**1, "KiB"),
)


def storage_health_human_bytes(value: int | float | str) -> str:
    """Format a byte count as a human-readable string using binary (IEC) units."""
    try:
        nbytes = int(value)
    except (TypeError, ValueError):
        return "0 B"

    if nbytes < 0:
        nbytes = 0

    if nbytes < 1024:
        return f"{nbytes} B"

    for factor, suffix in _DISPLAY_UNITS:
        if nbytes >= factor:
            return f"{nbytes / factor:.2f} {suffix}"

    return f"{nbytes} B"


class FilterModule:
    """Register filters with Ansible."""

    def filters(self) -> dict[str, object]:
        return {
            "storage_health_human_bytes": storage_health_human_bytes,
        }
