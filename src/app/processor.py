"""Processor module for computing volatility signals from input messages.

This module validates incoming messages and computes a derived volatility signal
based on the input data. All operations are logged for observability.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import ValidatedMessage
from app.utils.validate_data import validate_message_schema

logger = setup_logger(__name__)


def validate_input_message(message: dict[str, Any]) -> ValidatedMessage:
    """Validate the incoming raw message against the expected schema.

    Parameters
    ----------
        message (dict[str, Any]): The raw message payload.

    Returns
    -------
        ValidatedMessage: A validated message object.

    """
    logger.debug("🔍 Validating message schema...")
    if not validate_message_schema(message):
        logger.error("❌ Message schema invalid: %s", message)
        raise ValueError("Invalid message format")
    return message  # type: ignore[return-value]


def compute_volatility_signal(message: ValidatedMessage) -> dict[str, Any]:
    """Compute a volatility signal from the validated input message.

    This function is a placeholder for actual volatility models,
    such as standard deviation, ATR, or Bollinger bands.

    Parameters
    ----------
        message (ValidatedMessage): The validated message input.

    Returns
    -------
        dict[str, Any]: Dictionary with volatility-related data.

    """
    logger.debug("🌪️ Computing volatility signal for %s", message["symbol"])
    volatility_score = 1.0  # Placeholder logic

    return {
        "symbol": message["symbol"],
        "timestamp": message["timestamp"],
        "volatility_score": volatility_score,
    }


def process_message(raw_message: dict[str, Any]) -> ValidatedMessage:
    """Main entry point for processing a single message.

    Parameters
    ----------
        raw_message (dict[str, Any]): Raw input from the message queue.

    Returns
    -------
        ValidatedMessage: Enriched and validated message ready for output.

    """
    logger.info("🚦 Processing new message...")
    validated = validate_input_message(raw_message)
    volatility_data = compute_volatility_signal(validated)

    enriched: ValidatedMessage = {
        "symbol": validated["symbol"],
        "timestamp": validated["timestamp"],
        "data": {**validated["data"], **volatility_data},
    }
    logger.debug("✅ Final enriched message: %s", enriched)
    return enriched
