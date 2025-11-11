#!/usr/bin/env python3
import os
import requests
import datetime
import json
from pathlib import Path

GITHUB_TOKEN = os.getenv("PROJECT_TOKEN")
ORG = "Grupo2-CC3S2"
PROJECT_NUMBER = 14

GRAPHQL_URL = "https://api.github.com/graphql"

# === CONSULTA GraphQL ===
query = """
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      items(first: 50) {
        nodes {
          content {
            ... on Issue {
              number
              title
              state
              assignees(first: 5) {
                nodes { login }
              }
            }
          }
          fieldValues(first: 10) {
            nodes {
              __typename
              ... on ProjectV2ItemFieldNumberValue {
                field { ... on ProjectV2FieldCommon { name } }
                number
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                field { ... on ProjectV2FieldCommon { name } }
                name
              }
              ... on ProjectV2ItemFieldTextValue {
                field { ... on ProjectV2FieldCommon { name } }
                text
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
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    variables = {"org": ORG, "number": PROJECT_NUMBER}
    r = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers)
    data = r.json()
    if "errors" in data:
        raise Exception(data["errors"])

    items = data["data"]["organization"]["projectV2"]["items"]["nodes"]
    issues = []

    for it in items:
        if not it["content"]:
            continue
        issue = {
            "issue_id": it["content"]["number"],
            "title": it["content"]["title"],
            "status": it["content"]["state"],
            "assignees": [a["login"] for a in it["content"]["assignees"]["nodes"]]        }

        for f in it["fieldValues"]["nodes"]:
            field_type = f["__typename"]
            field_name = f["field"]["name"].lower().replace(" ", "_") if f.get("field") else "unknown"

            if field_type == "ProjectV2ItemFieldNumberValue":
                issue[field_name] = f.get("number")
            elif field_type == "ProjectV2ItemFieldSingleSelectValue":
                issue[field_name] = f.get("name")  # aquí vendrá "Sprint 1", "Sprint 2", etc.
            elif field_type == "ProjectV2ItemFieldTextValue":
                issue[field_name] = f.get("text")

        # Si no hay campo Sprint asignado, lo ponemos explícitamente
        if "sprint" not in issue:
            issue["sprint"] = "Sin asignar"

        issues.append(issue)
    return issues

def main():
    Path("data/snapshots").mkdir(parents=True, exist_ok=True)
    snapshot_file = f"data/snapshots/snapshot-{datetime.date.today()}.json"
    items = fetch_data()
    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"Snapshot generado: {snapshot_file} ({len(items)} issues)")

if __name__ == "__main__":
    main()
