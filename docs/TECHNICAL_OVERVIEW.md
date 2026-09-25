# Technical Overview

This document intentionally stays at a high level. Exact private hooks, maintenance gestures, reverse-engineering notes, and development reasoning are kept out of the public repository.

## Design principles
- **Favorites first:** everyday navigation should converge on one predictable Phone screen.
- **Call aware:** active cellular/CallKit calls take priority over kiosk behavior.
- **Event driven:** behavior is triggered by system/user events rather than continuous polling.
- **Fail safe:** reboot/respring defaults to Grandma Mode.
- **Minimal scope:** GrandmaClock is separate from GrandmaPhone so readability experiments do not destabilize calling behavior.
- **Conservative compatibility:** only physically tested hardware/software combinations are claimed.

## Packaging
Both packages are rootless `iphoneos-arm64` packages and are distributed through a standard APT repository hosted on GitHub Pages.
