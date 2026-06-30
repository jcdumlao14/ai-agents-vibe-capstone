# Logging Configuration

This project uses Python's built-in `logging` module.

Configuration is driven by `src/config/settings.py` using the following variables:

- `LOG_LEVEL` - default: `INFO`
- `LOG_FORMAT` - default: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

The logger is created in `src/config/logger.py` and can be imported wherever needed.
