

import json
from llm_client import call_llm


def safe_json(obj):
    """Safely convert data to compact JSON for LLM context."""
    try:
        return json.dumps(obj, indent=2)
    except:
        return str(obj)


def build_context(combined):
    """
    Build a compact summary for the LLM.
    Includes: summary, metadata, recent commits, and top active files.
    """

    ctx = {}

    ctx["summary"] = combined.get("summary", {})
    ctx["metadata"] = combined.get("metadata", {})
    ctx["recent_commits"] = combined.get("commit_history", [])[:6]

    files = combined.get("files", [])
    files_sorted = sorted(files, key=lambda f: len(f.get("file_history", [])), reverse=True)

    ctx["top_files"] = []
    for f in files_sorted[:6]:
        ctx["top_files"].append({
            "path": f.get("path"),
            "num_functions": len(f.get("functions", [])),
            "history": len(f.get("file_history", [])),
            "functions": [fn.get("name") for fn in f.get("functions", [])[:5]]
        })

    return safe_json(ctx)


# -------------------------------------------------------------------------
# PROMPTS (Balanced, simple, detailed)
# -------------------------------------------------------------------------

ABSTRACT_PROMPT = """
Write a balanced, clear abstract for a software project. 
Use the context below to explain:
- what the AutoDoc engine does
- why it is useful
- what data it analyzes
- what documentation it produces

Length: 5–7 clear sentences.
Context:
{context}
"""

OVERVIEW_PROMPT = """
Write a clean, easy-to-read project overview for the AutoDoc system.
Explain in simple terms:
- the purpose of the tool
- how it analyzes code + history
- why it is useful for developers
- the high-level workflow (analysis → combine → export → AI summary)

Keep it 2 short paragraphs.
Context:
{context}
"""

ARCHITECTURE_PROMPT = """
Write a structured architecture summary for the AutoDoc engine.
Explain these parts:
- static analysis pipeline
- dependency and function graph analysis
- git commit and evolution tracking
- combined JSON builder (v3)
- LLM documentation layer
- exporter creating MD/HTML/PDF

Write 3–5 short paragraphs, simple language.
Context:
{context}
"""

TOP_FILES_PROMPT = """
Using the context below, write an explanation of the most important, most actively changed files.
For each file:
- describe what it likely does
- why it changed often
- why it matters to the system

Write 3–4 sentences per file.
Context:
{context}
"""

FILE_SUMMARIES_PROMPT = """
Write readable summaries of the files listed below. 
For each file:
- explain its purpose
- mention the major functions
- keep language simple and balanced

Write 2–3 sentences per file.
Files:
{files}
"""
RISK_ANALYSIS_PROMPT = """
You are an expert software engineering assistant.

You are given structured analysis data for a codebase, including (when available):

- impact_report: which functions/modules affect others, and risk levels
- function_timeline: how often functions change
- quality_issues: long functions, deep nesting, TODOs, missing docs
- unused_functions: dead code candidates
- duplicate_functions: repeated logic
- commit_history: patterns of modifications
- dependency graphs: how modules relate

Using ONLY this context, write a clear **risk analysis** of the system.

Requirements:
- Start with a 2–3 sentence *overall risk summary* (Low / Medium / High)
- Then write bullet lists for:
    - High-risk or high-impact files to be careful with
    - Historically unstable areas (frequently changed functions)
    - Code smells that increase maintenance risk
    - Safe areas suitable for refactoring (unused/duplicate functions)
- Use simple English
- Keep total length ~300–400 words
- Do NOT invent data not present in the context

Context:
{context}
"""
ONBOARDING_PROMPT = """
Write a simple and friendly developer onboarding guide for this project.
Explain in clear language:
- What the AutoDoc engine does at a high level
- Which files or modules a new developer should read first
- How the major components fit together (static analysis, dependency graph, commit miner, combine engine, AI layer)
- What parts of the code are safe to modify
- What parts require caution due to high coupling or history of changes

Keep it under 3 short paragraphs.
Use simple English suitable for a student or junior developer.

Context:
{context}
"""
WORKFLOW_PROMPT = """
Explain the full workflow of the AutoDoc engine in clear, simple steps.

You must explain:
1. Static analysis of source files
2. Building file → file dependency graph (imports)
3. Building function → function call graph
4. Mining Git commit history and building evolution timeline
5. Combining all data into the v3 JSON model (unified dataset)
6. Running the LLM layer to generate AI documentation (abstract, overview, modules, risk, onboarding)
7. Exporting Markdown, HTML, and PDF

Requirements:
- Use simple English
- Write it as a developer-friendly explanation
- Keep it as 1–2 paragraphs, not too long
- Do NOT invent details outside the provided context

Context:
{context}
"""

RECOMMEND_PROMPT = """
Write 5 practical recommendations to improve the codebase.
Include suggestions about:
- documentation
- code quality
- structure
- testing
- maintainability

Keep each recommendation short and useful.
Context:
{context}
"""

# -------------------------------------------------------------------------
# MAIN GENERATION FUNCTION
# -------------------------------------------------------------------------

def generate_sections(combined):
    """Generate all AI-written documentation sections."""

    ctx = build_context(combined)

    def ask(prompt):
        return call_llm(prompt.format(context=ctx), max_tokens=900)

    sections = {}

    # Build file snippet as JSON for file summaries
    files = combined.get("files", [])
    files_sorted = sorted(files, key=lambda f: len(f.get("file_history", [])), reverse=True)

    file_snippets = json.dumps(
        [
            {
                "path": f.get("path"),
                "functions": [fn.get("name") for fn in f.get("functions", [])[:5]],
                "history": len(f.get("file_history", []))
            }
            for f in files_sorted[:6]
        ],
        indent=2
    )

    sections["abstract"] = ask(ABSTRACT_PROMPT)
    sections["overview"] = ask(OVERVIEW_PROMPT)
    sections["architecture"] = ask(ARCHITECTURE_PROMPT)
    sections["top_files"] = ask(TOP_FILES_PROMPT)
    sections["file_summaries"] = call_llm(FILE_SUMMARIES_PROMPT.format(files=file_snippets))
    sections["recommendations"] = ask(RECOMMEND_PROMPT)
    sections["risk_analysis"] = ask(RISK_ANALYSIS_PROMPT) 
    sections["onboarding_guide"] = ask(ONBOARDING_PROMPT)
    sections["system_workflow"] = ask(WORKFLOW_PROMPT)
    
    return sections
    


