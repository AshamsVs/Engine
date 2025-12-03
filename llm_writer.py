

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

    return sections
