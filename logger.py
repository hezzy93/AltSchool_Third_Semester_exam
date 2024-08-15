import logging
from logging.handlers import SysLogHandler

# Papertrail logging configuration
PAPERTRAIL_HOST = 'logs5.papertrailapp.com'
PAPERTRAIL_PORT = 48417

# Create a SysLogHandler for Papertrail
handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

# Set up basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[handler]  # Corrected spelling
)

# Function to get a logger
def get_logger(name):
    return logging.getLogger(name)

# Example usage
logger = get_logger(__name__)

logger.debug("This message will be recorded.")
logger.info("This message will be recorded.")
logger.warning("This message will be recorded.")
logger.error("This message will be recorded.")
logger.critical("This message will be recorded.")
