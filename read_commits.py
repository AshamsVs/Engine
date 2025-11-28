from git import Repo

repo = Repo(".")

for commit in repo.iter_commits():
    print("Commit ID:", commit.hexsha)
    print("Message:", commit.message.strip())
    print("Changed files:")

    for file_path, stats in commit.stats.files.items():
        print(f" - {file_path} | +{stats['insertions']} -{stats['deletions']}")

    print("\nDiff:")

    try:
        diff_text = repo.git.show(commit.hexsha, color=False)
        print(diff_text)
    except Exception as e:
        print("Could not read diff:", e)

    print("-" * 60)
