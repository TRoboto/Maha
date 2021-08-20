# Remove old rule cache files
# This scipt should be run before commiting modified cache files to prevent repo bloat
# Should be run from the root of the repository
git rm --cached maha/rexy/cache/*
rm maha/rexy/cache/*