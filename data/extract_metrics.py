#!/usr/bin/env python3
"""
extract_metrics.py (Día 3 - transición)
Intenta obtener datos reales desde GitHub Projects, si falla usa datos simulados.
"""
import os, requests, json, datetime
from pathlib import Path

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG = os.getenv("ORG", "Grupo2-CC3S2")
PROJECT_NUMBER = int(os.getenv("PROJECT_NUMBER", "14"))

def fetch_api():
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    query = """
    query($org:String!, $number:Int!){
      organization(login:$org){
        projectV2(number:$number){
          items(first:5){
            nodes{
              content{... on Issue{number title state}}
            }
          }
        }
      }
    }"""
    res = requests.post(url, json={"query": query, "variables": {"org": ORG, "number": PROJECT_NUMBER}}, headers=headers)
    data = res.json()
    project = data.get("data", {}).get("organization", {}).get("projectV2")
    if not project:
        print("No se pudo obtener datos del Project, usando simulación local")
        return None
    issues = []
    for item in project["items"]["nodes"]:
        c = item["content"]
        if c:
            issues.append({"issue_id": c["number"], "title": c["title"], "status": c["state"]})
    return issues

def main():
    Path("data/snapshots").mkdir(parents=True, exist_ok=True)
    snapshot = f"data/snapshots/snapshot-{datetime.date.today()}.json"
    data = fetch_api() or [{"issue_id": 1, "title": "Simulado", "status": "To Do"}]
    json.dump(data, open(snapshot, "w"), indent=2)
    print(f"Snapshot generado: {snapshot} ({len(data)} items)")

if __name__ == "__main__":
    main()
