import subprocess
import os
PLATFORM = os.getenv("PLATFORM") or "Windows-10-Chrome-61"
VERTICAL = os.getenv("VERTICAL") or "tonic"
test_report = "test-report/" + VERTICAL
test_reports = "test-reports/" + VERTICAL

# Decompress the tar files with allure results from previous runs.
subprocess.call([
    "tar", "zxvf", "test-report.tar.gz"
])
subprocess.call([
    "tar", "zxvf", "test-reports.tar.gz"
])


# Run the test
subprocess.call([
    'pytest',
    'android_test.py',
    '--alluredir=test-report/{}'.format(VERTICAL)
])

# Allure plugin
subprocess.call([
    "python3",
    "circleci_allure_plugin.py",
    test_report,
    test_reports
])
subprocess.call([
    "./allure-2.5.0/bin/allure",
    "generate",
    test_report,
    "-c",
    "-o",
    test_reports
])

# Compress the new results, and old results for the next run.
subprocess.call([
    "tar", "zcvf", "test-reports.tar.gz", "test-reports"
])
subprocess.call([
    "tar", "zcvf", "test-report.tar.gz", "test-report"
])
