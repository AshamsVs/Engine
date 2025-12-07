<!-- COVER PAGE -->
<div style="text-align: center; margin-top: 120px;">

# **AUTO-DOCUMENTATION ENGINE**  
### *(Static + AI Hybrid Documentation System)*

---

## **Project Report**

### **Submitted by**  
**Ashams**

### **College**  
**CMS College Kottayam (Autonomous)**  
Department of Computer Science

### **Academic Year**  
**2024 – 2025**

</div>

<div style="page-break-after: always;"></div>
<!-- END COVER PAGE -->
# 📑 Table of Contents

1. [Abstract](#1-abstract)  
2. [Project Overview](#2-project-overview)  
3. [System Architecture](#3-system-system-architecture)  
4. [File Dependency Graph](#4-file-dependency-graph)  
5. [Function Dependency Graph](#5-function-dependency-graph)  
6. [Important / Frequently Modified Files](#6-important--frequently-modified-files)  
7. [Module Summaries](#7-module-summaries)  
8. [Recommendations](#8-recommendations)  
9. [Risk Analysis](#9-risk-analysis-ai)  
10. [Developer Onboarding Guide](#10-developer-onboarding-guide-ai)  
11. [System Workflow Explanation](#11-system-workflow-explanation-ai)  
12. [Technical Summary](#12-technical-summary-static-analysis)  
13. [Code Quality Overview](#13-code-quality-overview)  
14. [Unused Functions](#14-unused-functions)  
15. [Duplicate Functions](#15-duplicate-functions)  
16. [Commit Timeline](#16-commit-timeline-summary)  
17. [Important Files](#17-important-files-static-summary)

<div style="page-break-after: always;"></div>
<!-- GLOBAL PDF STYLING -->
<style>

@page {
    size: A4;
    margin: 2cm;
    
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
    }
}

body {
    font-family: "Helvetica", "Arial", sans-serif;
    line-height: 1.5;
    font-size: 12pt;
}

h1, h2, h3, h4 {
    font-family: "Helvetica", sans-serif;
    margin-top: 24px;
    margin-bottom: 12px;
}

p, li, table {
    margin-top: 8px;
    margin-bottom: 8px;
}

code {
    font-family: "Courier New", monospace;
    background: #f2f2f2;
    padding: 3px 5px;
    border-radius: 4px;
    font-size: 11pt;
}

pre code {
    padding: 10px;
    display: block;
    background: #f5f5f5;
    border-radius: 6px;
    border: 1px solid #e0e0e0;
}

</style>

<div style="page-break-after: always;"></div>
<!-- END GLOBAL PDF STYLING -->


📘 Project Documentation Report

Generated automatically by the AutoDoc Engine (Static + AI Hybrid)

{% set ai = data.report.ai_summary if data.report is defined and data.report.ai_summary is defined else {} %}

🏷 Project Information

Project Path:
{{ data.metadata.project_root | default("unknown") }}

Generated At:
{{ data.metadata.generated_at | default("unknown") }}

Engine Version:
{{ data.metadata.version | default("unknown") }}

Match Mode:
{{ data.metadata.match_mode | default("strict") }}

🟦 1. Abstract

{{ ai.abstract | default("AI summary not available in CI build.") }}

🟩 2. Project Overview

{{ ai.overview | default("AI summary not available in CI build.") }}

🟧 3. System Architecture

{{ ai.architecture | default("AI summary not available in CI build.") }}

📊 4. File Dependency Graph
```mermaid
{{ data.file_dependency_graph | default("flowchart TD;\nA[No file dependency graph available]") }}
```

🔁 5. Function Dependency Graph
```mermaid
{{ data.function_dependency_graph | default("flowchart TD;\nA[No function dependency graph available]") }}
```
🟪 6. Important / Frequently Modified Files

{{ ai.top_files | default("AI summary not available in CI build.") }}

🟨 7. Module Summaries

{{ ai.file_summaries | default("AI summary not available in CI build.") }}

🟥 8. Recommendations

{{ ai.recommendations | default("AI summary not available in CI build.") }}

🔺 9. Risk Analysis (AI)

{{ ai.risk_analysis | default("AI risk analysis not available in this build.") }}

🧭 10. Developer Onboarding Guide (AI)

{{ ai.onboarding_guide | default("AI onboarding guide not available in this build.") }}

🔄 11. System Workflow Explanation (AI)

{{ ai.system_workflow | default("AI workflow explanation not available in this build.") }}


⚙️ 12. Technical Summary (Static Analysis)

Files analyzed: {{ data.summary.num_files }}
Functions detected: {{ data.summary.num_functions }}
Commits processed: {{ data.summary.num_commits }}

🧹 13. Code Quality Overview

{% set q = data.quality_issues | default({}) %}
{% if q %}
{% for file, issues in q.items() %}

{{ file }}

Missing docstrings: {{ issues.missing_docstrings | length }}

Long functions: {{ issues.long_functions | length }}

Too many parameters: {{ issues.too_many_parameters | length }}

Deep nesting: {{ issues.deep_nesting | length }}

TODO comments: {{ issues.todo_comments | length }}

{% endfor %}
{% else %}
No major quality issues detected by static analysis.
{% endif %}

🚫 14. Unused Functions

{% if data.unused_functions %}
{% for fn in data.unused_functions %}

{{ fn }}
{% endfor %}
{% else %}
No unused functions found.
{% endif %}

🔁 15. Duplicate Functions

{% if data.duplicate_functions %}
{% for file, items in data.duplicate_functions.items() %}

{{ file }} → {{ items|length }} duplicate(s)
{% endfor %}
{% else %}
No duplicate functions detected.
{% endif %}

🕒 16. Commit Timeline (Summary)

{% if data.commit_history %}
{% for c in data.commit_history %}

{{ c.commit }} — {{ c.message }}
({{ c.date }})
{% endfor %}
{% else %}
No commit history available.
{% endif %}

📂 17. Important Files (Static Summary)

{% for f in data.files %}

📌 File: {{ f.path | default("unknown") }}

Functions: {{ f.functions | length }}

Changes: {{ f.file_history | length }}

{% endfor %}

🏁 END OF REPORT

Generated by AutoDoc Engine.