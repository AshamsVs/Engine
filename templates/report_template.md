# Project Documentation Report

Generated automatically by the Documentation Engine.

---

## 📁 Project Path
`{{ data.project.root_path }}`

## 🕒 Generated At
Generated during the run.

---

# 1. Files Analyzed

{{ data.files | tojson(indent=2) }}

---

# 2. Commit Index

{{ data.commit_index | tojson(indent=2) }}

---

# 3. Summary

{{ data.summary | tojson(indent=2) }}

---

# 4. Per-File Details

{% for f in data.files %}
## File: {{ f.path }}
Functions Found: {{ f.functions | length }}
Changes: {{ f.file_history | length }}

{{ f | tojson(indent=2) }}
---
{% endfor %}

---

# END
