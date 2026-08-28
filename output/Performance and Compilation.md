---
title: Performance and Compilation
tags: [flutter, react-native, performance, compilation]
date: 2026-08-28
---

## Flutter
- Compiles Dart code directly to native ARM code (AOT compilation).
- Faster startup times, no JavaScript engine or bridge required.
- Impeller engine precompiles shaders, eliminating runtime jank and ensuring smooth animations.
- Larger native binary size due to bundled rendering engine.

## React Native
- Uses JavaScript (Hermes engine by default), communicates with native UI via JavaScript Interface (JSI).
- New Architecture (JSI, Fabric, TurboModules) eliminates old async bridge, achieves reliable 60fps for standard UI animations.

---

Related: [[Rendering and UI Consistency]], [[Developer Experience and Ecosystem]]