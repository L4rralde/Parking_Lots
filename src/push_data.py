"""
Pushes most recent version of data.csv to github
Author: Emmanuel Larralde
"""
from misc import git_repo, now


def main():
    """
    Pusehes new data to update_data branch on GitHub
    """
    git_repo.index.add('data/data.csv')
    git_repo.index.commit(f"Updating csv file at {now()}")
    if "update_data" not in git_repo.references:
        git_repo.git.checkout("-b", "update_data")
    else:
        git_repo.git.checkout("update_data")
    git_repo.git.push("--set-upstream", "origin", "update_data")
    git_repo.git.checkout("main")


if __name__ == '__main__':
    main()
