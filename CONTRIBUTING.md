# Maintenance

## Launcher list

After publishing a game release, add its version at the start of that mod’s `versions` list in [docs/mods.json](docs/mods.json). Use the release’s publication date and exact asset URLs. Keep older stable entries while their downloads remain available, then update `lastUpdated`.

Keep `sourceName` and the three mod IDs unchanged. The launcher uses them to identify installed mods. Keep platform support consistent with the [install guide](README.md#install).

The **Check launcher source** workflow validates the JSON against the [official launcher schema](https://github.com/open-goal/launcher/blob/9e4fc050d98ed452e7e340b62c981e3df00699c0/schemas/mod-source/v1/mod-source-schema.v1.json).

Each game repository holds its own installer builds and releases.

## OpenGOAL updates

The **Check OpenGOAL updates** workflow checks stable releases of the tooling and Launcher daily on GitHub. Run it manually from Actions for an immediate check. Each new version gets one compatibility issue assigned to the hub owner.

Use the issue to record which installers and game builds work with the new release. Change the supported pins only after verification. Record the reviewed tag in [the check script](.github/scripts/check_opengoal_updates.py) when the review is complete.

## Comparison images

When a release changes how a model looks, capture the affected comparisons again from that build before publishing. Use the same view in the original game and the mod. Update the gallery, its image manifest, and any docs or launcher artwork that show the old model as current.

[Back to the main page](README.md)
