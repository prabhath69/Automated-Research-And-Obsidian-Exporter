---
title: Security Considerations
tags: [security, encryption, storage, api-keys]
date: 2026-08-28
---

- Developers must implement secure storage, encryption, API key management; not provided by default.
- Storing sensitive data in unencrypted storage (SharedPreferences/Async Storage) is insecure.
- Use platform-secure storage (iOS Keychain, Android Keystore/EncryptedSharedPreferences).
- Avoid hardcoding API keys; use environment variables and server-side orchestration.

See [[Maintenance and Release Cycle]], [[Native Integration]].