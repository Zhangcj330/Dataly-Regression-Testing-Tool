
import os
from typing import Any, Dict, List, Optional, Union, cast

import numpy as np
import pandas as pd

from datacompy import Compare, render

class DatalyCompare(Compare):
    def Regression_report(
        self,
        sample_count: int = 10,
        html_file: Optional[str] = None,
    ) -> str:
        def df_to_str(pdf: pd.DataFrame) -> str:
            if not self.on_index:
                pdf = pdf.reset_index(drop=True)
            return pdf.to_string()

        # Header
        report = ("Dataly Regression Test Output")
        report += "\n"
        report += "--------------------"
        report += "\n\n"
        report += "DataFrame Summary"
        report += "\n"
        report += "-----------------"
        report += "\n\n"
        df_header = pd.DataFrame(
            {
                "DataFrame": [self.df1_name, self.df2_name],
                "Columns": [self.df1.shape[1], self.df2.shape[1]],
                "Rows": [self.df1.shape[0], self.df2.shape[0]],
            }
        )
        report += df_header[["DataFrame", "Columns", "Rows"]].to_string()
        report += "\n\n"

        # Column Summary
        report += render(
            "column_summary.txt",
            len(self.intersect_columns()),
            len(self.df1_unq_columns()),
            len(self.df2_unq_columns()),
            self.df1_name,
            self.df2_name,
        )
        report += "Columns in " + self.df1_name + " Have all Null values: " + str(', '.join(self.df1.columns[self.df1.isna().all()].tolist()))
        report += "\n"
        report += "Columns in " + self.df2_name + " Have all Null values: "  + str(', '.join(self.df2.columns[self.df1.isna().all()].tolist()))
        report += "\n\n"


        # Row Summary
        if self.on_index:
            match_on = "index"
        else:
            match_on = ", ".join(self.join_columns)
        report += render(
            "row_summary.txt",
            match_on,
            self.abs_tol,
            self.rel_tol,
            self.intersect_rows.shape[0],
            self.df1_unq_rows.shape[0],
            self.df2_unq_rows.shape[0],
            self.intersect_rows.shape[0] - self.count_matching_rows(),
            self.count_matching_rows(),
            self.df1_name,
            self.df2_name,
            "Yes" if self._any_dupes else "No",
        )

        match_stats = []
        match_sample = []
        any_mismatch = False
        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                match_stats.append(
                    {
                        "Column": column["column"],
                        f"{self.df1_name} dtype": column["dtype1"],
                        f"{self.df2_name} dtype": column["dtype2"],
                        "# Unequal": column["unequal_cnt"],
                        "Max Diff": column["max_diff"],
                        "# Null Diff": column["null_diff"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    match_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )

        if any_mismatch:
            report += "Columns with Unequal Values or Types\n"
            report += "------------------------------------\n"
            report += "\n"
            df_match_stats = pd.DataFrame(match_stats)
            df_match_stats.sort_values("Column", inplace=True)
            # Have to specify again for sorting
            report += df_match_stats[
                [
                    "Column",
                    f"{self.df1_name} dtype",
                    f"{self.df2_name} dtype",
                    "# Unequal",
                    "Max Diff",
                    "# Null Diff",
                ]
            ].to_string()
            report += "\n\n"

            if sample_count > 0:
                report += "Sample Rows with Unequal Values\n"
                report += "-------------------------------\n"
                report += "\n"
                for sample in match_sample:
                    report += df_to_str(sample)
                    report += "\n\n"

        return report

