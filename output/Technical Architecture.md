---
title: Technical Architecture
tags: [architecture, rendering, ui, cross-platform]
date: 2026-08-28
---

## Rendering and UI

### Flutter
- Uses a custom GPU-based engine (Impeller).
- Draws every pixel directly for pixel-perfect, consistent UI.
- Supports iOS, Android, web, Windows, macOS, Linux, embedded devices from a single codebase.

### React Native
- Bridges JavaScript UI descriptions to native widgets (Fabric renderer).
- Provides platform-native look and feel.
- Primarily mobile-focused; web/desktop via community projects.

See also [[Performance Comparison]], [[Native Integration]].