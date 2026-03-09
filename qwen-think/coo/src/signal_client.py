"""Signal messaging output for COO nudges.

Stub — logs messages that would be sent.
Options for real delivery:
  - signal-cli-rest-api as sidecar container on timekeeper-internal
  - Shortcut/automation bridge
"""

import structlog

from config import SIGNAL_ENABLED

log = structlog.get_logger()


async def send_message(text: str) -> bool:
    """Send a message via Signal. Currently a stub."""
    if not SIGNAL_ENABLED:
        log.info("signal.stub", message=text, note="Signal disabled, logging only")
        return False

    # TODO: HTTP POST to signal-cli-rest-api sidecar
    log.warning("signal.not_implemented", message=text)
    return False
