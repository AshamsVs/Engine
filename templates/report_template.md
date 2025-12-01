# 📘 Project Documentation Report  
Generated automatically by the AutoDoc Engine.

---

## 📁 Project Path  
`{{ data.metadata.project_root | default("unknown") }}`  

## 🕒 Generated At  
`{{ data.metadata.generated_at | default("unknown") }}`  

## ⚙️ Engine Version  
`{{ data.metadata.version | default("unknown") }}`  
Match mode: `{{ data.metadata.match_mode | default("strict") }}`  

---

# 1. Summary  
{{ data.summary | default({}) | tojson(indent=2) }}  

---

# 2. Commit History  
{{ data.commit_history | default([]) | tojson(indent=2) }}  

---

# 3. Dependencies  
{{ data.dependencies | default({}) | tojson(indent=2) }}  

---

# 4. Function Timeline  
{% set timeline = data.evolution_timeline | default({}) %}

{% if timeline is mapping %}
{% for func, events in timeline.items() %}
- **{{ func }}** → {{ events|length }} updates
{% endfor %}
{% else %}
No timeline data available.
{% endif %}

---

# 5. Quality Issues  
{% set q = data.quality_issues | default({}) %}

{% if q is mapping %}
{% for file, issues in q.items() %}
## {{ file }}
- Missing docstrings: {{ issues.missing_docstrings|length }}
- Long functions: {{ issues.long_functions|length }}
- Too many params: {{ issues.too_many_parameters|length }}
- Deep nesting: {{ issues.deep_nesting|length }}
- TODO comments: {{ issues.todo_comments|length }}

{% endfor %}
{% else %}
No quality issues found.
{% endif %}

---

# 6. Unused Functions  
{% set unused = data.unused_functions | default([]) %}
{% if unused %}
{% for item in unused %}
- {{ item }}
{% endfor %}
{% else %}
No unused functions detected.
{% endif %}

---

# 7. Duplicate Functions  
{% set dup = data.duplicate_functions | default({}) %}
{% if dup %}
{% for file, items in dup.items() %}
- **{{ file }}** → {{ items|length }} duplicates
{% endfor %}
{% else %}
No duplicates found.
{% endif %}

---

# 8. Diff Explanations  
{{ data.diff_explanations | default([]) | tojson(indent=2) }}

---

# 9. Impact Report  
{{ data.impact_report | default({}) | tojson(indent=2) }}

---

# 10. Per-File Details  
{% set files = data.files | default([]) %}
{% for f in files %}
## File: {{ f.path | default("unknown") }}
- Functions: {{ f.functions|length }}
- History events: {{ f.file_history|length }}

{{ f | tojson(indent=2) }}

---
{% endfor %}

---

# END
