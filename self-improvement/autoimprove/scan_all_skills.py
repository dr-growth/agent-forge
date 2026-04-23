"""Quick heuristic scan of all skills -- no API calls needed."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from src.evaluate import score_completeness, score_structure, score_confidence_calibration
from src.runner import load_skill, TestCase, run_skill
from src.config import TEST_CASES_DIR

SKILLS_DIR = Path.home() / "claude-code-skills" / "skills"

# For skills WITH test cases, run full scoring
# For skills WITHOUT test cases, create a generic test and run
GENERIC_PROMPTS = {
    "editing-copy": "Review and improve this landing page copy for a B2B SaaS platform:\n\nHeadline: Acme - Data Quality Monitoring\nSubheadline: We help companies monitor their data quality automatically.\nSection: Features - Automated monitoring, ML powered, Easy setup\nCTA: Learn More",
    "engineering-prompts": "Improve this prompt: 'Write a blog post outline about data quality.' It keeps giving me generic results.",
    "building-skills": "Create a Claude Code skill for generating changelog entries from git diffs.",
    "optimizing-pages": "Our SaaS homepage has a 65% bounce rate and 2.1% conversion rate. Traffic is 60% organic. Average time on page is 45 seconds. Help me optimize it.",
    "auditing-seo": "Audit the SEO health of example.com. Focus on technical issues, content quality, and quick wins.",
}

GENERIC_SCHEMA = {
    "required_sections": [],
    "required_fields": [],
    "min_word_count": 300
}

results = []
for skill_dir in sorted(SKILLS_DIR.iterdir()):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        continue
    name = skill_dir.name
    
    # Check if we have test cases
    tc_dir = TEST_CASES_DIR / name
    has_tests = tc_dir.exists() and list(tc_dir.glob("*.json"))
    
    results.append({
        "skill": name,
        "has_test_cases": has_tests,
        "lines": len(skill_md.read_text().splitlines()),
    })

# Sort by has_test_cases (True first), then name
results.sort(key=lambda x: (not x["has_test_cases"], x["skill"]))

print(f"Total skills: {len(results)}")
print(f"With test cases: {sum(1 for r in results if r['has_test_cases'])}")
print(f"Without test cases: {sum(1 for r in results if not r['has_test_cases'])}")
print()

for r in results:
    flag = " [HAS TESTS]" if r["has_test_cases"] else ""
    print(f"  {r['skill']:40s} {r['lines']:4d} lines{flag}")
