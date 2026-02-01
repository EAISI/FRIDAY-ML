# Security

- **NEVER** store secrets, API keys, or passwords in code. Only store them in `.env`.
  - Ensure `.env` is declared in `.gitignore`.
  - **NEVER** print or log URLs to console if they contain an API key.
- **MUST** use environment variables for sensitive configuration
- **NEVER** log sensitive information (passwords, tokens, PII)