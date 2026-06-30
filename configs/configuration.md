# Configuration Classes

This project uses Pydantic settings classes for typed configuration.

- `src/config/settings.py`
  - `AppSettings` holds application configuration values.
  - Environment values are loaded from `.env` by default.
  - Use `settings` for access across the application.

Configuration includes:
- application metadata
- environment mode
- API keys and cloud credentials
- logging settings
