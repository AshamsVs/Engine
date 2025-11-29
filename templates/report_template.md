# Project Documentation Report

Generated automatically by the Documentation Engine.

---

## 📁 Project Path
`{{ data.metadata.project_path }}`

## 🕒 Generated At
`{{ data.metadata.generated_at }}`

---

# 1. Project Structure
{{ data.project_structure | tojson(indent=2) }}

---

# 2. File Dependencies
{{ data.dependencies.files | tojson(indent=2) }}

---

# 3. Function Dependencies
{{ data.dependencies.functions | tojson(indent=2) }}

---

# 4. Git Commit History
{% for entry in data.git_history %}
- **Commit:** {{ entry.commit }}
- **Message:** {{ entry.message }}
- **Changed Functions:** {{ entry.changed_functions }}
---
{% endfor %}

---

# 5. Change Impact Analysis
{{ data.change_impact | tojson(indent=2) }}

---

# 6. Evolution Timeline
{{ data.evolution_timeline | tojson(indent=2) }}

---

# 7. Diff Explanations
{% for diff in data.diff_explanations %}
### Commit: {{ diff.commit }} | Function: `{{ diff.function }}`
File: `{{ diff.file }}`
- Summary: {{ diff.summary }}
---
{% endfor %}

---

# 8. Suggested Docstrings
{% for doc in data.docstrings %}
### File: {{ doc.file }} | Function: **{{ doc.function }}**

**Arguments:** {{ doc.arguments }}  
**Has Return:** {{ doc.has_return }}

{{ doc.suggested_docstring }}

---
{% endfor %}

---

# 9. Quality Issues
{{ data.quality_issues | tojson(indent=2) }}

---

# 10. Naming Issues
{{ data.naming_issues | tojson(indent=2) }}

---

# 11. Duplicate Functions
{{ data.duplicate_functions | tojson(indent=2) }}

---

# 12. Unused Functions
{{ data.unused_functions | tojson(indent=2) }}

---

# 13. Metadata
{{ data.metadata | tojson(indent=2) }}

---

*End of Report*
