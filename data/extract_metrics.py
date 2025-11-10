#!/usr/bin/env python3
"""
extract_metrics.py (Sprint 2 - para Project en ORGANIZATION)
Extrae issues reales del Project Kanban (ProjectV2) de una organización en GitHub.
"""
import os
import requests
import datetime
import json
from pathlib import Path

# === CONFIGURACIÓN ===
GITHUB_TOKEN = os.getenv("PROJECT_TOKEN")
ORG = "Grupo2-CC3S2"             # tu organización EXACTA
PROJECT_NUMBER = 14               # número del proyecto (ajústalo según corresponda)

# === CONSULTA GRAPHQL CORRECTA ===
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
              ... on ProjectV2ItemFieldTextValue {
                field { ... on ProjectV2FieldCommon { name } }
                text
              }
              ... on ProjectV2ItemFieldNumberValue {
                field { ... on ProjectV2FieldCommon { name } }
                number
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                field { ... on ProjectV2FieldCommon { name } }
                name
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
    url = "https://api.github.com/graphql"
    variables = {"org": ORG, "number": PROJECT_NUMBER}

    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    data = response.json()
    print("🔍 Código:", response.status_code)
    print(json.dumps(data, indent=2))

    if "errors" in data:
        raise Exception(data["errors"][0]["message"])

    items = data["data"]["organization"]["projectV2"]["items"]["nodes"]

    issues = []
    for it in items:
        if not it["content"]:
            continue
        issue = {
            "issue_id": it["content"]["number"],
            "title": it["content"]["title"],
            "status": it["content"]["state"],
            "assignees": [a["login"] for a in it["content"]["assignees"]["nodes"]],
            "fields": {}
        }
        for f in it["fieldValues"]["nodes"]:
            field_type = f["__typename"]
            if "field" not in f or not f["field"]:
                continue
            field_name = f["field"]["name"]
            if field_type == "ProjectV2ItemFieldNumberValue":
                issue["fields"][field_name] = f.get("number")
            elif field_type == "ProjectV2ItemFieldSingleSelectValue":
                issue["fields"][field_name] = f.get("name")
            elif field_type == "ProjectV2ItemFieldTextValue":
                issue["fields"][field_name] = f.get("text")
        issues.append(issue)

    return issues


def main():
    Path("data/snapshots").mkdir(parents=True, exist_ok=True)
    snapshot_file = f"data/snapshots/snapshot-{datetime.date.today()}.json"

    items = fetch_data()
    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"✅ Snapshot generado: {snapshot_file} ({len(items)} issues)")

if __name__ == "__main__":
    main()
