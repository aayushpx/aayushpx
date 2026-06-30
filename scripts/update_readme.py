"""
Pulls real contribution data from the GitHub GraphQL API and rewrites the
block between <!--LIVE:START--> and <!--LIVE:END--> in README.md.

Requires env vars:
    GH_TOKEN      a token with read access (the default GITHUB_TOKEN works)
    GH_USERNAME   the GitHub username to report on
"""

import os
import re
import sys
from datetime import datetime, timedelta, timezone

import requests

GH_TOKEN = os.environ["GH_TOKEN"]
GH_USERNAME = os.environ["GH_USERNAME"]
README_PATH = "README.md"

GRAPHQL_URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {GH_TOKEN}"}

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
    repositories(first: 10, ownerAffiliations: OWNER, orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes {
        name
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
    response = requests.post(
        GRAPHQL_URL,
        json={"query": QUERY, "variables": {"login": GH_USERNAME}},
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if "errors" in payload:
        print(payload["errors"], file=sys.stderr)
        raise SystemExit(1)
    return payload["data"]["user"]


def compute_streak(days):
    streak = 0
    for day in reversed(days):
        if day["contributionCount"] > 0:
            streak += 1
        else:
            break
    return streak


def most_recent_commit(repositories):
    latest = None
    for repo in repositories:
        ref = repo.get("defaultBranchRef")
        if not ref or not ref.get("target"):
            continue
        history = ref["target"]["history"]["nodes"]
        if not history:
            continue
        commit = history[0]
        commit_date = datetime.fromisoformat(commit["committedDate"].replace("Z", "+00:00"))
        if latest is None or commit_date > latest[0]:
            latest = (commit_date, repo["name"], commit["messageHeadline"])
    return latest


def main():
    user = fetch_data()
    calendar = user["contributionsCollection"]["contributionCalendar"]
    total = calendar["totalContributions"]

    days = []
    for week in calendar["weeks"]:
        days.extend(week["contributionDays"])

    streak = compute_streak(days)
    latest = most_recent_commit(user["repositories"]["nodes"])
    now = datetime.now(timezone.utc)

    if latest:
        commit_date, repo_name, headline = latest
        delta = now - commit_date
        if delta < timedelta(hours=1):
            when = f"{int(delta.total_seconds() // 60)}m ago"
        elif delta < timedelta(days=1):
            when = f"{int(delta.total_seconds() // 3600)}h ago"
        else:
            when = f"{delta.days}d ago"
        last_commit_line = f"{repo_name}: {headline}"
    else:
        last_commit_line = "no recent commits found"
        when = ""

    # fixed inner width for the box, every line gets truncated/padded to fit
    inner_width = 46
    label_width = 14

    def fit(label, value):
        text = f"{value}"
        max_value_len = inner_width - label_width
        if len(text) > max_value_len:
            text = text[: max_value_len - 1] + "…"
        line = f"{label:<{label_width}}{text}"
        return f"  {line:<{inner_width}}"

    rows = [
        fit("last commit", f"{last_commit_line} ({when})" if when else last_commit_line),
        fit("streak", f"{streak} day{'s' if streak != 1 else ''}"),
        fit("commits", f"{total} this year"),
        fit("as of", now.strftime("%Y-%m-%d %H:%M UTC")),
    ]

    border_len = inner_width + 4
    block = (
        "```\n"
        f"┌─ LIVE FEED {'─' * (border_len - 13)}┐\n"
        + "\n".join(rows) + "\n"
        + f"└{'─' * border_len}┘\n"
        "```"
    )

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r"<!--LIVE:START-->.*?<!--LIVE:END-->",
        f"<!--LIVE:START-->\n{block}\n<!--LIVE:END-->",
        content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
