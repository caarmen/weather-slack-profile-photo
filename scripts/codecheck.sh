for project in .
do
  black $project
  ruff check $project
done
