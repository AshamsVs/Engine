from function_ranges import get_function_ranges
from parse_diff import get_changed_lines

def detect_changed_functions(file_path, diff_text):
    functions = get_function_ranges(file_path)
    changed_lines = get_changed_lines(diff_text)

    changed_functions = []

    for func in functions:
        start = func["start"]
        end = func["end"]

        # if ANY changed line falls inside the function block
        if any(start <= line <= end for line in changed_lines):
            changed_functions.append(func["name"])

    return changed_functions


# Test with sample diff
if __name__ == "__main__":
    sample_diff = """@@ -1,2 +1,8 @@
-def greet(name):
-    return "Hello " + name
+def greet(name):
+    message = "HELLO, " + name.upper() + "!"
+    return message
+
+def farewell(name):
+    return "Goodbye, " + name
"""
    changed = detect_changed_functions("demo.py", sample_diff)
    print("Changed functions:", changed)
