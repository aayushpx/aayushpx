"""
Updates the LIVE FEED block in README.md using the GitHub GraphQL API.

Environment variables:
    GH_TOKEN      GitHub token with read access
    GH_USERNAME   GitHub username to report on
"""

import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone

import requests


GH_TOKEN = os.environ["GH_TOKEN"]
GH_USERNAME = os.environ["GH_USERNAME"]
README_PATH = "README.md"

GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Content-Type": "application/json",
}


QUERY = """
query($login: String!) {
  user(login: $login) {

    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }

    repositories(
      first: 100
      ownerAffiliations: OWNER
      privacy: PUBLIC
      orderBy: {field: PUSHED_AT, direction: DESC}
    ) {
      nodes {
        name
        pushedAt
        primaryLanguage {
          name
        }

        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 1) {
                nodes {
                  committedDate
                  messageHeadline
                }
              }
            }
          }
        }
      }
    }
  }
}
"""


def fetch_data():
    """Fetch profile contribution and repository data."""
    response = requests.post(
        GRAPHQL_URL,
        json={
            "query": QUERY,
            "variables": {"login": GH_USERNAME},
        },
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()

    if "errors" in payload:
        print("GitHub GraphQL errors:", file=sys.stderr)
        for error in payload["errors"]:
            print(error, file=sys.stderr)
        raise SystemExit(1)

    return payload["data"]["user"]


def parse_date(value):
    """Convert an ISO timestamp into an aware datetime."""
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def compute_streak(days):
    """
    Calculate the current contribution streak.

    Only days up to today are considered.
    """
    today = datetime.now(timezone.utc).date()

    valid_days = [
        day
        for day in days
        if datetime.fromisoformat(day["date"]).date() <= today
    ]

    valid_days.sort(key=lambda day: day["date"])

    streak = 0

    for day in reversed(valid_days):
        if day["contributionCount"] > 0:
            streak += 1
        else:
            break

    return streak


def get_latest_commit(repositories):
    """Find the latest commit across owned public repositories."""
    latest = None

    for repo in repositories:
        ref = repo.get("defaultBranchRef")

        if not ref or not ref.get("target"):
            continue

        history = ref["target"].get("history", {}).get("nodes", [])

        if not history:
            continue

        commit = history[0]
        commit_date = parse_date(commit["committedDate"])

        candidate = (
            commit_date,
            repo["name"],
            commit["messageHeadline"],
        )

        if latest is None or commit_date > latest[0]:
            latest = candidate

    return latest


def get_active_repositories(repositories, since):
    """Return repositories pushed to since the supplied datetime."""
    return [
        repo
        for repo in repositories
        if repo.get("pushedAt")
        and parse_date(repo["pushedAt"]) >= since
    ]


def get_recent_languages(repositories):
    """
    Get languages from recently active repositories.

    Languages are ordered by how many active repositories use them.
    """
    languages = Counter()

    for repo in repositories:
        language = repo.get("primaryLanguage")

        if language and language.get("name"):
            languages[language["name"]] += 1

    return languages.most_common()


def format_age(timestamp, now):
    """Format a timestamp as a compact relative time."""
    delta = now - timestamp

    if delta < timedelta(minutes=1):
        return "just now"

    if delta < timedelta(hours=1):
        minutes = int(delta.total_seconds() // 60)
        return f"{minutes}m ago"

    if delta < timedelta(days=1):
        hours = int(delta.total_seconds() // 3600)
        return f"{hours}h ago"

    days = delta.days

    if days == 1:
        return "1d ago"

    return f"{days}d ago"


def truncate(value, max_length):
    """Keep long values from making the terminal box enormous."""
    if len(value) <= max_length:
        return value

    return value[: max_length - 1].rstrip() + "…"


def build_feed(user):
    """Build the formatted Live Feed block."""
    now = datetime.now(timezone.utc)

    calendar = user["contributionsCollection"]["contributionCalendar"]

    total_contributions = calendar["totalContributions"]

    days = [
        day
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    ]

    streak = compute_streak(days)

    repositories = user["repositories"]["nodes"]

    latest = get_latest_commit(repositories)

    month_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    active_since = now - timedelta(days=30)

    commits_this_month = sum(
        day["contributionCount"]
        for day in days
        if month_start.date()
        <= datetime.fromisoformat(day["date"]).date()
        <= now.date()
    )

    active_repositories = get_active_repositories(
        repositories,
        active_since,
    )

    recent_languages = get_recent_languages(active_repositories)

    language_names = [name for name, _ in recent_languages[:3]]

    if language_names:
        recent_work = " · ".join(language_names)
    else:
        recent_work = "no recent activity"

    if latest:
        commit_date, repo_name, headline = latest

        last_commit = (
            f"{repo_name}: "
            f"{truncate(headline, 62)} "
            f"({format_age(commit_date, now)})"
        )
    else:
        last_commit = "no recent commits found"

    rows_raw = [
        ("last commit", last_commit),
        ("streak", f"{streak} day{'s' if streak != 1 else ''}"),
        ("commits", f"{commits_this_month} this month"),
        (
            "active repos",
            f"{len(active_repositories)} in last 30 days",
        ),
        ("recent work", recent_work),
        ("as of", now.strftime("%Y-%m-%d %H:%M UTC")),
    ]

    label_width = 14

    content_width = max(
        label_width + len(value)
        for _, value in rows_raw
    )

    inner_width = max(content_width, 52)

    def fit(label, value):
        line = f"{label:<{label_width}}{value}"
        return f"  {line:<{inner_width}}"

    rows = [
        fit(label, value)
        for label, value in rows_raw
    ]

    border_len = inner_width + 4

    top_border = (
        "┌─ LIVE FEED "
        + "─" * (border_len - 13)
        + "┐"
    )

    bottom_border = "└" + "─" * border_len + "┘"

    return (
        "```text\n"
        f"{top_border}\n"
        + "\n".join(rows)
        + "\n"
        f"{bottom_border}\n"
        "```"
    )


def update_readme(block):
    """Replace the existing Live Feed block."""
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = r"<!--LIVE:START-->.*?<!--LIVE:END-->"

    replacement = (
        "<!--LIVE:START-->\n"
        f"{block}\n"
        "<!--LIVE:END-->"
    )

    new_content, replacements = re.subn(
        pattern,
        replacement,
        content,
        flags=re.DOTALL,
    )

    if replacements != 1:
        print(
            "Expected exactly one LIVE block in README.md",
            file=sys.stderr,
        )
        raise SystemExit(1)

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(new_content)


def main():
    user = fetch_data()
    block = build_feed(user)
    update_readme(block)


if __name__ == "__main__":
    main()
