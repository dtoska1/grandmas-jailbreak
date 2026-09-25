# Grandma's Jailbreak

A small Sileo repository for two rootless iOS 15 tweaks:

- **GrandmaPhone** — simplifies the Phone app around Favorites, provides Grandma/Admin/Super Admin modes, preserves calling, and returns to Favorites after calls.
- **GrandmaClock** — enlarges the status-bar and Lock Screen clock and improves date/charging-status readability.

## Compatibility

Tested on:
- iPhone 7
- iOS 15.8.8
- Dopamine rootless / ElleKit

Packages are built for the rootless `iphoneos-arm64` package architecture. Other devices should be physically validated before being listed as officially supported.

## Sileo repository

GitHub Pages URL:

`https://dtoska1.github.io/grandmas-jailbreak/`

Once the first device-tested release packages are published, add that URL to **Sileo → Sources**, refresh, then install **GrandmaPhone** and/or **GrandmaClock**.

## Package IDs

- `com.local.grandmaphonetest`
- `com.local.grandmaclock`

The GrandmaPhone package ID intentionally keeps its earlier `grandmaphonetest` identifier so existing installed copies can upgrade in place.

## Release status

The public repository shell is online. The first `1.0.0` package files and Sileo indexes will be published only after the exact release builds are produced with the established Theos environment and physically validated on the tested iPhone 7.

## Important

These packages rely on private iOS classes and are intended for the tested iOS 15 environment. Do not update or restore a device solely to use these packages.
