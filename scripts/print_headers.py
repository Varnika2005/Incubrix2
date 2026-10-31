import csv

with open('submission/reports/QUESTION_COVERAGE.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    print("QUESTION_COVERAGE.csv headers:", next(r))
    print("First row:", next(r))

with open('submission/citation_plan/CITATION_TARGETS.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    print("\nCITATION_TARGETS.csv headers:", next(r))
    print("First row:", next(r))

