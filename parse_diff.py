import re

def get_changed_lines(diff_text):
    """
    Extract the line numbers of added lines ('+') in the new file.
    """
    changed_lines = []

    # Split the diff into lines
    lines = diff_text.split("\n")

    current_line = None

    for line in lines:
        # Detect hunk header, e.g. "@@ -1,2 +1,8 @@"
        hunk_match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if hunk_match:
            current_line = int(hunk_match.group(1))
            continue

        # Detect added lines starting with "+"
        if line.startswith("+") and not line.startswith("+++"):
            changed_lines.append(current_line)

        # Move to next line in new file
        if current_line is not None:
            current_line += 1

    return changed_lines


# Test (with example diff)
if __name__ == "__main__":
    sample = """@@ -1,2 +1,8 @@
-def greet(name):
-    return "Hello " + name
+def greet(name):
+    message = "HELLO, " + name.upper() + "!"
+    return message
+
+def farewell(name):
+    return "Goodbye, " + name
"""
    print(get_changed_lines(sample))
