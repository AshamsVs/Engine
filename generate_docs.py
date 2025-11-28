import json

def load_json(path="combined_data.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_template(path="prompt_template.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(template, data):
    json_data = json.dumps(data, indent=2)
    return template.replace("<<PROJECT_DATA_JSON>>", json_data)

def simulate_llm(prompt):
    # This is a placeholder. 
    # In Django we replace this with a real API call.
    return """
# AutoDoc Documentation (Simulated)

This is a simulated output.
The real documentation will be generated once we integrate the LLM API.
"""

def main():
    data = load_json()
    template = load_template()
    final_prompt = build_prompt(template, data)

    print("=== Prompt Generated Successfully ===")
    print(final_prompt[:500])
    print("\n=== Simulated LLM Output ===")
    print(simulate_llm(final_prompt))

    with open("simulated_output.md", "w", encoding="utf-8") as f:
        f.write(simulate_llm(final_prompt))

    print("\nWrote simulated_output.md")


if __name__ == "__main__":
    main()
