import pytest
import pandas as pd
from core import DatalyCompare  # Make sure to replace with your actual module name

@pytest.fixture
def setup_data():
    data1 = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    data2 = {'A': [1, 2, 3], 'B': [4, 5, 7]}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    return DatalyCompare(df1, df2, join_columns=['A'])

def test_report_no_diff():
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df1 = pd.DataFrame(data)
    df2 = pd.DataFrame(data)
    comparison = DatalyCompare(df1, df2, join_columns=['A'])
    report = comparison.Regression_report()
    assert "Dataly Regression Test Output" in report
    assert "The report was generated on" in report
    assert "DataFrame Summary" in report
    assert "Columns with Unequal Values or Types" in report
    assert "Sample Rows with Unequal Values" in report

def test_report_with_diff(setup_data):
    comparison = setup_data
    report = comparison.Regression_report()
    assert "Dataly Regression Test Output" in report
    assert "The report was generated on" in report
    assert "DataFrame Summary" in report
    assert "Columns with Unequal Values or Types" in report
    assert "Sample Rows with Unequal Values" in report
    assert "Columns in df1 Have all Null values:" in report
    assert "Columns in df2 Have all Null values:" in report
    assert "Max Diff" in report
    assert "# Unequal" in report

def test_empty_dataframes():
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    comparison = DatalyCompare(df1, df2, join_columns=['A'])
    report = comparison.Regression_report()
    assert "Dataly Regression Test Output" in report
    assert "The report was generated on" in report
    assert "DataFrame Summary" in report

def test_column_summary(setup_data):
    comparison = setup_data
    report = comparison.Regression_report()
    assert "column_summary.txt" in report

def test_row_summary(setup_data):
    comparison = setup_data
    report = comparison.Regression_report()
    assert "row_summary.txt" in report
