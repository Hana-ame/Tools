CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo $CUR_BRANCH

git add .;
git stash;

git checkout master;
git pull;
git checkout $CUR_BRANCH;

git stash pop;