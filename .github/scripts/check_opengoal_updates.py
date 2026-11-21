"""Open a compatibility issue for a newer stable OpenGOAL release."""

import json
import os
import re
import subprocess


REVIEWED_RELEASES = (
    (
        "tooling", "open-goal/jak-project", "v0.3.9",
        "Check the official tool binaries, source, and disc and graphics fingerprints. "
        "Build all three mods and check installation, updates, and representative gameplay "
        "on Windows, macOS, and Linux before updating the tooling pins.",
    ),
    (
        "Launcher", "open-goal/launcher", "v2.11.2",
        "Check custom source import and validate the launcher catalog against the release's schema. "
        "Test installation and updates for all three mods with the current pinned tooling. "
        "Check that saves survive an update.",
    ),
)


def version(tag):
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", tag)
    if not match:
        raise ValueError(f"Unexpected stable release tag {tag!r}")
    return tuple(map(int, match.groups()))


def github(*args, data=None):
    payload = json.dumps(data) if data is not None else None
    return json.loads(subprocess.check_output(["gh", "api", *args], input=payload, text=True))


def main():
    repo = os.environ["GH_REPO"]
    pending = []
    for component, upstream, reviewed, checks in REVIEWED_RELEASES:
        tag = github(f"repos/{upstream}/releases/latest")["tag_name"]
        print(f"OpenGOAL {component} latest {tag}, reviewed {reviewed}", flush=True)
        if version(tag) > version(reviewed):
            pending.append((component, upstream, reviewed, checks, tag))
    if not pending:
        return

    endpoint = f"repos/{repo}/issues"
    pages = github("--paginate", "--slurp", f"{endpoint}?state=all&per_page=100")
    issue_bodies = [issue.get("body") or "" for page in pages for issue in page]
    for component, upstream, reviewed, checks, tag in pending:
        marker = f"<!-- opengoal-release {upstream}@{tag} -->"
        if any(marker in body for body in issue_bodies):
            print(f"An issue already tracks OpenGOAL {component} {tag}.", flush=True)
            continue

        title = f"Check OpenGOAL {component} {tag} compatibility"
        url = f"https://github.com/{upstream}/releases/tag/{tag}"
        body = (
            f"OpenGOAL {component} {tag} is available. "
            f"The last reviewed version was {reviewed}. [Release notes]({url})\n\n"
            f"{checks}\n\n"
            "Record the compatibility results here before changing the supported versions.\n\n"
            f"{marker}\n"
        )
        issue = github(
            endpoint, "--method", "POST", "--input", "-",
            data={"title": title, "body": body, "assignees": [repo.split("/", 1)[0]]},
        )
        print(f"Opened {issue['html_url']}", flush=True)


if __name__ == "__main__":
    main()
