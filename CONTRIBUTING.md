# Maintenance

## Launcher list

After publishing a game release, add its version at the start of that mod’s `versions` list in [docs/mods.json](docs/mods.json). Use the release’s publication date and exact asset URLs. Keep older stable entries while their downloads remain available, then update `lastUpdated`.

Keep `sourceName` and the three mod IDs unchanged. The launcher uses them to identify installed mods. Keep platform support consistent with the [install guide](README.md#install).

The **Check launcher source** workflow validates the JSON against the [official launcher schema](https://github.com/open-goal/launcher/blob/9e4fc050d98ed452e7e340b62c981e3df00699c0/schemas/mod-source/v1/mod-source-schema.v1.json).

Each game repository holds its own installer builds and releases.

[Back to the main page](README.md)
