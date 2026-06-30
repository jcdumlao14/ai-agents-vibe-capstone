# Secrets Management

Store secret values securely outside the repository.

Local development:
- Add secrets to `.env` or use local secret storage.

Production:
- Use managed secret storage services such as:
  - Google Secret Manager
  - HashiCorp Vault
  - AWS Secrets Manager

Do not commit secrets to source control.
