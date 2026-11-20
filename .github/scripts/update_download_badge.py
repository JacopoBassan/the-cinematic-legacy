"""Build a Shields badge from the public installer asset counts."""

import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen


def list_releases(game):
    repo = f"JacopoBassan/the-cinematic-legacy-{game}"
    token = os.environ.get("GH_TOKEN")
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/releases?per_page=100&page={page}"
        request = Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "The-Cinematic-Legacy-download-badge",
        })
        if token:
            request.add_unredirected_header("Authorization", f"Bearer {token}")
        with urlopen(request, timeout=30) as response:
            releases = json.load(response)
        if not isinstance(releases, list):
            raise ValueError(f"Unexpected releases response for {repo}")
        yield from releases
        if len(releases) < 100:
            return
        page += 1


def count_installers(releases):
    total = 0
    for release in releases:
        if release["draft"] or release["prerelease"]:
            continue
        tag = release["tag_name"]
        names = {f"windows-{tag}.zip", f"macos-arm64-{tag}.tar.gz", f"linux-{tag}.tar.gz"}
        for asset in release["assets"]:
            if asset["name"] in names:
                count = asset["download_count"]
                if type(count) is not int or count < 0:
                    raise ValueError(f"Invalid download count for {asset['name']}")
                total += count
    return total


def main(output):
    total = sum(count_installers(list_releases(game)) for game in ("jak1", "jak2", "jak3"))
    badge = {"schemaVersion": 1, "label": "↓ Installer downloads",
             "message": f"{total:,}", "color": "6e59b9"}
    output.write_text(json.dumps(badge, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Counted {total:,} installer downloads")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
