# Project Documentation Report

Generated automatically by the Documentation Engine.

---

## 📁 Project Path
`C:\Users\91773\OneDrive\Desktop\Engine`

## 🕒 Generated At
`2025-11-29T15:05:42.273086`

---

# 1. Project Structure
{}

---

# 2. File Dependencies
{
  ".\\analyze_project.py": [],
  ".\\combine_data.py": [
    ".\\analyze_project.py",
    ".\\extract_commit_changes.py"
  ],
  ".\\demo.py": [],
  ".\\dependency_graph.py": [],
  ".\\detect_changed_functions.py": [
    ".\\function_ranges.py",
    ".\\parse_diff.py"
  ],
  ".\\example.py": [],
  ".\\extract_commit_changes.py": [
    ".\\detect_changed_functions.py",
    ".\\function_ranges.py"
  ],
  ".\\function_call_graph.py": [],
  ".\\function_ranges.py": [],
  ".\\generate_docs.py": [],
  ".\\parse_diff.py": [],
  ".\\read_commits.py": []
}

---

# 3. Function Dependencies
{
  "analyze_file": [],
  "analyze_imports": [],
  "analyze_project": [
    "get_python_files",
    "analyze_file"
  ],
  "attach_commit_changes": [],
  "build_dependency_data": [
    "build_file_dependency_graph",
    "build_filtered_call_graph"
  ],
  "build_file_dependency_graph": [
    "build_module_to_file_map",
    "get_python_files",
    "analyze_imports"
  ],
  "build_filtered_call_graph": [
    "get_python_files",
    "extract_defined_functions",
    "extract_calls"
  ],
  "build_index_by_file": [],
  "build_module_to_file_map": [
    "get_python_files",
    "get_module_name"
  ],
  "build_prompt": [],
  "combine": [
    "analyze_project",
    "extract_commit_changes",
    "build_index_by_file",
    "attach_commit_changes"
  ],
  "detect_changed_functions": [
    "get_function_ranges",
    "get_changed_lines"
  ],
  "extract_calls": [],
  "extract_commit_changes": [
    "detect_changed_functions"
  ],
  "extract_defined_functions": [],
  "farewell": [],
  "generate_markdown": [],
  "get_changed_lines": [],
  "get_function_ranges": [],
  "get_module_name": [],
  "get_python_files": [],
  "greet": [],
  "load_json": [],
  "load_template": [],
  "main": [
    "load_json",
    "load_template",
    "build_prompt",
    "simulate_llm",
    "simulate_llm"
  ],
  "simulate_llm": []
}

---

# 4. Git Commit History

- **Commit:** a534d38ce95db8db89afdb1f8c3fde4cef57a804
- **Message:** Refactor greet and add farewell function
- **Changed Functions:** ['farewell', 'greet']
---

- **Commit:** db08f4c0f9e9753b5221e12b92250a27d51a47d3
- **Message:** Improve greeting format
- **Changed Functions:** ['greet']
---

- **Commit:** 61828ed4f03c598ee8db21946e2b83d45e41bc85
- **Message:** Add greet function
- **Changed Functions:** ['greet']
---


---

# 5. Change Impact Analysis
{
  "61828ed4f03c598ee8db21946e2b83d45e41bc85": {
    "greet": {
      "direct_and_indirect_impact": [],
      "risk": "LOW"
    }
  },
  "a534d38ce95db8db89afdb1f8c3fde4cef57a804": {
    "farewell": {
      "direct_and_indirect_impact": [],
      "risk": "LOW"
    },
    "greet": {
      "direct_and_indirect_impact": [],
      "risk": "LOW"
    }
  },
  "db08f4c0f9e9753b5221e12b92250a27d51a47d3": {
    "greet": {
      "direct_and_indirect_impact": [],
      "risk": "LOW"
    }
  }
}

---

# 6. Evolution Timeline
{
  "farewell": [
    {
      "commit": "a534d38",
      "message": "Refactor greet and add farewell function"
    }
  ],
  "greet": [
    {
      "commit": "61828ed",
      "message": "Add greet function"
    },
    {
      "commit": "db08f4c",
      "message": "Improve greeting format"
    },
    {
      "commit": "a534d38",
      "message": "Refactor greet and add farewell function"
    }
  ]
}

---

# 7. Diff Explanations

### Commit: a534d38ce95db8db89afdb1f8c3fde4cef57a804 | Function: `farewell`
File: `.\demo.py`
- Summary: A docstring was added to the function. Return statement or returned value was modified. Function `farewell` was added: `def farewell(name):`.
---

### Commit: a534d38ce95db8db89afdb1f8c3fde4cef57a804 | Function: `greet`
File: `.\demo.py`
- Summary: A docstring was added to the function. Return statement or returned value was modified.
---

### Commit: db08f4c0f9e9753b5221e12b92250a27d51a47d3 | Function: `greet`
File: `.\demo.py`
- Summary: String/formatting change detected. Example removed: `return "Hello " + name` → added: `return "Hello, " + name + "!"`. Return statement or returned value was modified.
---

### Commit: 61828ed4f03c598ee8db21946e2b83d45e41bc85 | Function: `greet`
File: `.\demo.py`
- Summary: Return statement or returned value was modified. Function `greet` was added: `def greet(name):`.
---


---

# 8. Suggested Docstrings

### File: .\analyze_project.py | Function: **get_python_files**

**Arguments:** ['folder_path']  
**Has Return:** True

""" Get python files.

Parameters:
    folder_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\analyze_project.py | Function: **analyze_file**

**Arguments:** ['file_path']  
**Has Return:** True

""" Analyze file.

Parameters:
    file_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\analyze_project.py | Function: **analyze_project**

**Arguments:** ['folder_path']  
**Has Return:** True

""" Analyze project.

Parameters:
    folder_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\analyze_project.py | Function: **generate_markdown**

**Arguments:** ['project_data', 'output_file']  
**Has Return:** False

""" Generate markdown.

Parameters:
    project_data (any): Description.
    output_file (any): Description.

"""

---

### File: .\combine_data.py | Function: **combine**

**Arguments:** ['project_path']  
**Has Return:** True

""" Combine.

Parameters:
    project_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **get_python_files**

**Arguments:** ['folder']  
**Has Return:** True

""" Get python files.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **get_module_name**

**Arguments:** ['file_path']  
**Has Return:** True

""" Get module name.

Parameters:
    file_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **build_module_to_file_map**

**Arguments:** ['folder']  
**Has Return:** True

""" Build module to file map.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **analyze_imports**

**Arguments:** ['file_path']  
**Has Return:** True

""" Analyze imports.

Parameters:
    file_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **build_file_dependency_graph**

**Arguments:** ['folder']  
**Has Return:** True

""" Build file dependency graph.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **extract_defined_functions**

**Arguments:** ['tree']  
**Has Return:** True

""" Extract defined functions.

Parameters:
    tree (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **extract_calls**

**Arguments:** ['func_node']  
**Has Return:** True

""" Extract calls.

Parameters:
    func_node (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **build_filtered_call_graph**

**Arguments:** ['folder']  
**Has Return:** True

""" Build filtered call graph.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\dependency_graph.py | Function: **build_dependency_data**

**Arguments:** ['folder']  
**Has Return:** True

""" Build dependency data.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\detect_changed_functions.py | Function: **detect_changed_functions**

**Arguments:** ['file_path', 'diff_text']  
**Has Return:** True

""" Detect changed functions.

Parameters:
    file_path (any): Description.
    diff_text (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diagram_generator.py | Function: **load_dependencies**

**Arguments:** []  
**Has Return:** True

""" Load dependencies.

Returns:
    any: Description.

"""

---

### File: .\diagram_generator.py | Function: **generate_file_dependency_mermaid**

**Arguments:** ['files']  
**Has Return:** True

""" Generate file dependency mermaid.

Parameters:
    files (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diagram_generator.py | Function: **generate_function_dependency_mermaid**

**Arguments:** ['funcs']  
**Has Return:** True

""" Generate function dependency mermaid.

Parameters:
    funcs (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **load_commit_changes**

**Arguments:** ['path']  
**Has Return:** True

""" Load commit changes.

Parameters:
    path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **normalize_code_line**

**Arguments:** ['s']  
**Has Return:** True

""" Normalize code line.

Parameters:
    s (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **detect_punctuation_change**

**Arguments:** ['added', 'removed']  
**Has Return:** True

""" Detect punctuation change.

Parameters:
    added (any): Description.
    removed (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **detect_signature_change**

**Arguments:** ['added', 'removed', 'func_name']  
**Has Return:** True

""" Detect signature change.

Parameters:
    added (any): Description.
    removed (any): Description.
    func_name (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **detect_docstring_change**

**Arguments:** ['added', 'removed']  
**Has Return:** True

""" Detect docstring change.

Parameters:
    added (any): Description.
    removed (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **detect_return_change**

**Arguments:** ['added', 'removed']  
**Has Return:** True

""" Detect return change.

Parameters:
    added (any): Description.
    removed (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **detect_logic_change**

**Arguments:** ['added', 'removed']  
**Has Return:** True

""" Detect logic change.

Parameters:
    added (any): Description.
    removed (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **explain_changes_for_function**

**Arguments:** ['file_path', 'func_name', 'diff_text']  
**Has Return:** True

""" Explain changes for function.

Parameters:
    file_path (any): Description.
    func_name (any): Description.
    diff_text (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **build_explanations**

**Arguments:** ['output_md', 'output_json']  
**Has Return:** True

""" Build explanations.

Parameters:
    output_md (any): Description.
    output_json (any): Description.

Returns:
    any: Description.

"""

---

### File: .\diff_explainer.py | Function: **get_python_files**

**Arguments:** ['folder']  
**Has Return:** True

""" Get python files.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\docstring_generator.py | Function: **get_python_files**

**Arguments:** ['folder']  
**Has Return:** False

""" Get python files.

Parameters:
    folder (any): Description.

"""

---

### File: .\docstring_generator.py | Function: **build_docstring**

**Arguments:** ['func_name', 'args', 'has_return']  
**Has Return:** True

""" Build docstring.

Parameters:
    func_name (any): Description.
    args (any): Description.
    has_return (any): Description.

Returns:
    any: Description.

"""

---

### File: .\docstring_generator.py | Function: **analyze_file**

**Arguments:** ['file_path']  
**Has Return:** True

""" Analyze file.

Parameters:
    file_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\docstring_generator.py | Function: **generate_docstrings**

**Arguments:** []  
**Has Return:** True

""" Generate docstrings.

Returns:
    any: Description.

"""

---

### File: .\extract_commit_changes.py | Function: **extract_commit_changes**

**Arguments:** []  
**Has Return:** True

""" Extract commit changes.

Returns:
    any: Description.

"""

---

### File: .\function_call_graph.py | Function: **get_python_files**

**Arguments:** ['folder']  
**Has Return:** True

""" Get python files.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\function_call_graph.py | Function: **extract_defined_functions**

**Arguments:** ['tree']  
**Has Return:** True

""" Extract defined functions.

Parameters:
    tree (any): Description.

Returns:
    any: Description.

"""

---

### File: .\function_call_graph.py | Function: **extract_calls**

**Arguments:** ['func_node']  
**Has Return:** True

""" Extract calls.

Parameters:
    func_node (any): Description.

Returns:
    any: Description.

"""

---

### File: .\function_call_graph.py | Function: **build_filtered_call_graph**

**Arguments:** ['folder']  
**Has Return:** True

""" Build filtered call graph.

Parameters:
    folder (any): Description.

Returns:
    any: Description.

"""

---

### File: .\function_ranges.py | Function: **get_function_ranges**

**Arguments:** ['file_path']  
**Has Return:** True

""" Get function ranges.

Parameters:
    file_path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\function_timeline.py | Function: **load_commit_changes**

**Arguments:** []  
**Has Return:** True

""" Load commit changes.

Returns:
    any: Description.

"""

---

### File: .\function_timeline.py | Function: **build_timeline**

**Arguments:** []  
**Has Return:** True

""" Build timeline.

Returns:
    any: Description.

"""

---

### File: .\generate_docs.py | Function: **load_json**

**Arguments:** ['path']  
**Has Return:** True

""" Load json.

Parameters:
    path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\generate_docs.py | Function: **load_template**

**Arguments:** ['path']  
**Has Return:** True

""" Load template.

Parameters:
    path (any): Description.

Returns:
    any: Description.

"""

---

### File: .\generate_docs.py | Function: **build_prompt**

**Arguments:** ['template', 'data']  
**Has Return:** True

""" Build prompt.

Parameters:
    template (any): Description.
    data (any): Description.

Returns:
    any: Description.

"""

---

### File: .\generate_docs.py | Function: **simulate_llm**

**Arguments:** ['prompt']  
**Has Return:** True

""" Simulate llm.

Parameters:
    prompt (any): Description.

Returns:
    any: Description.

"""

---

### File: .\generate_docs.py | Function: **main**

**Arguments:** []  
**Has Return:** False

""" Main.

"""

---

### File: .\impact_analysis.py | Function: **load_dependencies**

**Arguments:** []  
**Has Return:** True

""" Load dependencies.

Returns:
    any: Description.

"""

---

### File: .\impact_analysis.py | Function: **load_commit_changes**

**Arguments:** []  
**Has Return:** True

""" Load commit changes.

Returns:
    any: Description.

"""

---

### File: .\impact_analysis.py | Function: **build_reverse_dependency_graph**

**Arguments:** ['func_graph']  
**Has Return:** True

""" Build reverse dependency graph.

Parameters:
    func_graph (any): Description.

Returns:
    any: Description.

"""

---

### File: .\impact_analysis.py | Function: **get_full_impact**

**Arguments:** ['changed_function', 'reverse_graph']  
**Has Return:** True

""" Get full impact.

Parameters:
    changed_function (any): Description.
    reverse_graph (any): Description.

Returns:
    any: Description.

"""

---

### File: .\impact_analysis.py | Function: **calculate_risk_level**

**Arguments:** ['impact_list']  
**Has Return:** True

""" Calculate risk level.

Parameters:
    impact_list (any): Description.

Returns:
    any: Description.

"""

---

### File: .\impact_analysis.py | Function: **build_cia_report**

**Arguments:** []  
**Has Return:** True

""" Build cia report.

Returns:
    any: Description.

"""

---


---

# 9. Quality Issues
{
  ".\\analyze_project.py": {
    "deep_nesting": [
      {
        "function": "analyze_file",
        "nesting_depth": 5,
        "threshold": 3
      },
      {
        "function": "generate_markdown",
        "nesting_depth": 5,
        "threshold": 3
      }
    ],
    "long_functions": [
      {
        "function": "analyze_file",
        "length": 49,
        "threshold": 30
      },
      {
        "function": "generate_markdown",
        "length": 33,
        "threshold": 30
      }
    ],
    "missing_docstrings": [
      "get_python_files",
      "analyze_file",
      "analyze_project",
      "generate_markdown"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\combine_data.py": {
    "deep_nesting": [
      {
        "function": "attach_commit_changes",
        "nesting_depth": 6,
        "threshold": 3
      }
    ],
    "long_functions": [
      {
        "function": "attach_commit_changes",
        "length": 36,
        "threshold": 30
      },
      {
        "function": "combine",
        "length": 55,
        "threshold": 30
      }
    ],
    "missing_docstrings": [
      "combine"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\demo.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\dependency_graph.py": {
    "deep_nesting": [
      {
        "function": "analyze_imports",
        "nesting_depth": 4,
        "threshold": 3
      },
      {
        "function": "extract_calls",
        "nesting_depth": 4,
        "threshold": 3
      }
    ],
    "long_functions": [],
    "missing_docstrings": [
      "get_python_files",
      "get_module_name",
      "build_module_to_file_map",
      "analyze_imports",
      "build_file_dependency_graph",
      "extract_defined_functions",
      "extract_calls",
      "build_filtered_call_graph",
      "build_dependency_data"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\detect_changed_functions.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [
      "detect_changed_functions"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\diagram_generator.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [
      "load_dependencies",
      "generate_file_dependency_mermaid",
      "generate_function_dependency_mermaid"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\diff_explainer.py": {
    "deep_nesting": [
      {
        "function": "collect_added_removed_lines_in_func",
        "nesting_depth": 5,
        "threshold": 3
      },
      {
        "function": "detect_signature_change",
        "nesting_depth": 4,
        "threshold": 3
      },
      {
        "function": "explain_changes_for_function",
        "nesting_depth": 5,
        "threshold": 3
      },
      {
        "function": "build_explanations",
        "nesting_depth": 5,
        "threshold": 3
      }
    ],
    "long_functions": [
      {
        "function": "extract_hunks",
        "length": 39,
        "threshold": 30
      },
      {
        "function": "explain_changes_for_function",
        "length": 90,
        "threshold": 30
      },
      {
        "function": "build_explanations",
        "length": 59,
        "threshold": 30
      }
    ],
    "missing_docstrings": [
      "load_commit_changes",
      "normalize_code_line",
      "detect_punctuation_change",
      "detect_signature_change",
      "detect_docstring_change",
      "detect_return_change",
      "detect_logic_change",
      "explain_changes_for_function",
      "build_explanations",
      "get_python_files"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\docstring_generator.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [
      "get_python_files",
      "build_docstring",
      "analyze_file",
      "generate_docstrings"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\example.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\extract_commit_changes.py": {
    "deep_nesting": [
      {
        "function": "extract_commit_changes",
        "nesting_depth": 4,
        "threshold": 3
      }
    ],
    "long_functions": [],
    "missing_docstrings": [
      "extract_commit_changes"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\function_call_graph.py": {
    "deep_nesting": [
      {
        "function": "extract_calls",
        "nesting_depth": 4,
        "threshold": 3
      }
    ],
    "long_functions": [],
    "missing_docstrings": [
      "get_python_files",
      "extract_defined_functions",
      "extract_calls",
      "build_filtered_call_graph"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\function_ranges.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [
      "get_function_ranges"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\function_timeline.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [
      "load_commit_changes",
      "build_timeline"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\generate_docs.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [
      "load_json",
      "load_template",
      "build_prompt",
      "simulate_llm",
      "main"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\impact_analysis.py": {
    "deep_nesting": [
      {
        "function": "get_full_impact",
        "nesting_depth": 4,
        "threshold": 3
      }
    ],
    "long_functions": [],
    "missing_docstrings": [
      "load_dependencies",
      "load_commit_changes",
      "build_reverse_dependency_graph",
      "get_full_impact",
      "calculate_risk_level",
      "build_cia_report"
    ],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\parse_diff.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\quality_checker.py": {
    "deep_nesting": [
      {
        "function": "detect_long_functions",
        "nesting_depth": 4,
        "threshold": 3
      },
      {
        "function": "analyze_quality",
        "nesting_depth": 4,
        "threshold": 3
      }
    ],
    "long_functions": [
      {
        "function": "analyze_quality",
        "length": 39,
        "threshold": 30
      }
    ],
    "missing_docstrings": [],
    "todo_comments": [],
    "too_many_parameters": []
  },
  ".\\read_commits.py": {
    "deep_nesting": [],
    "long_functions": [],
    "missing_docstrings": [],
    "todo_comments": [],
    "too_many_parameters": []
  }
}

---

# 10. Naming Issues
{
  ".\\analyze_project.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\combine_data.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\demo.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\dependency_graph.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\detect_changed_functions.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\diagram_generator.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\diff_explainer.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\docstring_generator.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\example.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\extract_commit_changes.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\function_call_graph.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\function_ranges.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\function_timeline.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\generate_docs.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\impact_analysis.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\naming_checker.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\parse_diff.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\quality_checker.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\read_commits.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  },
  ".\\unused_function_detector.py": {
    "bad_classes": [],
    "bad_constants": [],
    "bad_functions": [],
    "bad_variables": []
  }
}

---

# 11. Duplicate Functions
{
  "1b264798cb01680e5826fcf3f602958c": [
    {
      "file": ".\\diagram_generator.py",
      "hash": "1b264798cb01680e5826fcf3f602958c",
      "name": "load_dependencies"
    },
    {
      "file": ".\\impact_analysis.py",
      "hash": "1b264798cb01680e5826fcf3f602958c",
      "name": "load_dependencies"
    }
  ],
  "2afbc069f21d7ff2e7db723fd6a7e530": [
    {
      "file": ".\\dependency_graph.py",
      "hash": "2afbc069f21d7ff2e7db723fd6a7e530",
      "name": "get_python_files"
    },
    {
      "file": ".\\diff_explainer.py",
      "hash": "2afbc069f21d7ff2e7db723fd6a7e530",
      "name": "get_python_files"
    },
    {
      "file": ".\\function_call_graph.py",
      "hash": "2afbc069f21d7ff2e7db723fd6a7e530",
      "name": "get_python_files"
    }
  ],
  "308610df5ddea9dda404ecb64205a586": [
    {
      "file": ".\\duplicate_detector.py",
      "hash": "308610df5ddea9dda404ecb64205a586",
      "name": "get_python_files"
    },
    {
      "file": ".\\naming_checker.py",
      "hash": "308610df5ddea9dda404ecb64205a586",
      "name": "get_python_files"
    }
  ],
  "4598621cea21282720223f6cfa672a6c": [
    {
      "file": ".\\diff_explainer.py",
      "hash": "4598621cea21282720223f6cfa672a6c",
      "name": "load_commit_changes"
    },
    {
      "file": ".\\generate_docs.py",
      "hash": "4598621cea21282720223f6cfa672a6c",
      "name": "load_json"
    }
  ],
  "4d5e807fc3c2a3f86c3df65bb66b5ee9": [
    {
      "file": ".\\function_timeline.py",
      "hash": "4d5e807fc3c2a3f86c3df65bb66b5ee9",
      "name": "load_commit_changes"
    },
    {
      "file": ".\\impact_analysis.py",
      "hash": "4d5e807fc3c2a3f86c3df65bb66b5ee9",
      "name": "load_commit_changes"
    }
  ],
  "58f3e1b2b6b717d869dbf30266b2cac1": [
    {
      "file": ".\\dependency_graph.py",
      "hash": "58f3e1b2b6b717d869dbf30266b2cac1",
      "name": "extract_calls"
    },
    {
      "file": ".\\function_call_graph.py",
      "hash": "58f3e1b2b6b717d869dbf30266b2cac1",
      "name": "extract_calls"
    }
  ],
  "b7666d20d7ce046aed487160015b520f": [
    {
      "file": ".\\dependency_graph.py",
      "hash": "b7666d20d7ce046aed487160015b520f",
      "name": "extract_defined_functions"
    },
    {
      "file": ".\\function_call_graph.py",
      "hash": "b7666d20d7ce046aed487160015b520f",
      "name": "extract_defined_functions"
    }
  ],
  "eeac32903a387104467ff303f577beef": [
    {
      "file": ".\\quality_checker.py",
      "hash": "eeac32903a387104467ff303f577beef",
      "name": "get_python_files"
    },
    {
      "file": ".\\unused_function_detector.py",
      "hash": "eeac32903a387104467ff303f577beef",
      "name": "get_python_files"
    }
  ],
  "f7f8181915de8dcf1d6f5641d25e81d4": [
    {
      "file": ".\\dependency_graph.py",
      "hash": "f7f8181915de8dcf1d6f5641d25e81d4",
      "name": "build_filtered_call_graph"
    },
    {
      "file": ".\\function_call_graph.py",
      "hash": "f7f8181915de8dcf1d6f5641d25e81d4",
      "name": "build_filtered_call_graph"
    }
  ]
}

---

# 12. Unused Functions
{
  ".\\demo.py": [
    "greet",
    "farewell"
  ],
  ".\\example.py": [
    "greet",
    "say_hi"
  ]
}

---

# 13. Metadata
{
  "generated_at": "2025-11-29T15:05:42.273086",
  "merged_unused_at": "2025-11-29T15:18:16.089804",
  "project_path": "C:\\Users\\91773\\OneDrive\\Desktop\\Engine",
  "unused_source": "C:\\Users\\91773\\OneDrive\\Desktop\\Engine\\unused_functions.json",
  "version": "2.0"
}

---

*End of Report*