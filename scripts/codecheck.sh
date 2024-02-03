error=0
for project in wspp
do
  black $project || error=$?
  ruff check $project --output-format=github || error=$?
  isort --profile black --check-only $project || error=$?
done
exit $error