from requester import Requester
from data import Data
from misc import git_repo, now


def main():
    scrapper = Requester()
    db = Data()
    db.append(scrapper.step())
    scrapper.finish()
    db.finish()

    when = now()
    git_repo.index.add('data/data.csv')
    git_repo.index.commit(f"Updating csv file at {when}")
    git_repo.git.stash('save')
    if "update_data" not in git_repo.references:
        git_repo.git.checkout("-b", "update_data")
    else:
        git_repo.git.checkout("update_data")
    git_repo.git.checkout("main", "data/data.csv")
    git_repo.index.add('data/data.csv')
    git_repo.index.commit(f"Updating csv file at {when}")
    git_repo.git.push("--set-upstream", "origin", "update_data")
    git_repo.git.checkout("main")
    git_repo.head.reset('HEAD~1', index=True, working_tree=True)
    if git_repo.git.stash('list'):
        git_repo.git.stash('pop')

if __name__ == '__main__':
    main()
