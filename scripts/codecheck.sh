for project in wspp
do
  black $project
  ruff check $project
done
