---
title: Security in Flutter and React Native
tags: [flutter, react-native, security]
date: 2026-08-28
---

## Flutter
- Recommends secure storage (Flutter Secure Storage, Keychain, Keystore), discourages unencrypted local storage.
- Emphasizes HTTPS, SSL/TLS, SSL pinning.
- Security strategy: Identify, Detect, Protect, Respond, Recover. Publishes updates, treats security reports as P0.

## React Native
- Secure storage and network communication.
- Security spans JS bundle, native modules, network; requires SCA, secure OTA updates, OWASP Mobile Top 10 mapping.
- Both: Avoid hardcoded credentials, encrypt credentials in transit, secure coding practices.

---

See also: [[Maintenance, Community, and Cost]]