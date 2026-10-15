"""Exercise area handoff in the actual JavaScript used by the planner."""
import json
import re
import subprocess
from pathlib import Path


def test_embedding_area_handoff():
    source = (Path(__file__).parent / "webapp/index.html").read_text()
    function = re.search(r"function embeddingAtlasURL\(bounds,group\)\{.*?\n\}", source, re.S).group()
    script = function + """
const bounds=(w,s,e,n)=>({getWest:()=>w,getSouth:()=>s,getEast:()=>e,getNorth:()=>n});
console.log(JSON.stringify([
  embeddingAtlasURL(bounds(-124,48,-122,50),"Plantae"),
  embeddingAtlasURL(bounds(-200,-91,200,91),"All biodiversity"),
  embeddingAtlasURL(bounds(170,-20,190,20),"Aves")
]));
"""
    urls = json.loads(subprocess.check_output(["node", "-e", script], text=True))
    from urllib.parse import parse_qs, urlparse

    parsed = [urlparse(url) for url in urls]
    assert all(url.hostname == "wietzesuijker.github.io" for url in parsed)
    assert parse_qs(parsed[0].query) == {"group": ["Plantae"], "bbox": ["-124.00000,48.00000,-122.00000,50.00000"]}
    assert not parsed[1].query
    assert parse_qs(parsed[2].query) == {"group": ["Aves"]}
