"""
Script. Requests parking lot data from website, appends the new data (one row)
to the databases and pushes to github
"""

from requester import Requester
from data import Data
from misc import git_repo, now


DST_BRANCH = "main" #WARNING. Currently it only works on this branch


def main():
    """
    Main script. Same description as file docstring
    """
    scrapper = Requester()
    db = Data()
    db.append(scrapper.step())
    scrapper.finish()
    db.finish()

    when = now()
    branch = git_repo.active_branch.name
    git_repo.index.add('data/data.csv')
    git_repo.index.commit(f"Updating csv file at {when}")
    git_repo.git.stash('save')
    if DST_BRANCH not in git_repo.references:
        git_repo.git.checkout("-b", DST_BRANCH)
    else:
        git_repo.git.checkout(DST_BRANCH)
    git_repo.git.checkout(branch, "data/data.csv")
    git_repo.index.add('data/data.csv')
    git_repo.index.commit(f"Updating csv file at {when}")
    git_repo.git.push("--set-upstream", "origin", DST_BRANCH)
    git_repo.git.checkout(branch)
    git_repo.head.reset('HEAD~1', index=True, working_tree=True)
    if git_repo.git.stash('list'):
        git_repo.git.stash('pop')


if __name__ == '__main__':
    main()
