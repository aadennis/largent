# python -m unittest -v test_module
import unittest
import pandas as pd
from pprint import pprint
from nw_to_homebank_csv import (
    set_placeholder_values,
    mark_statement_boundary,
    handle_special_payees,
    format_paid_columns,
)

class TestPreprocessData(unittest.TestCase):
    def setUp(self):
        # Sample input data
        nw_src_data = {
            "Date": ["01 Jan 2022", "31 Jan 2022", "02 Feb 2022"],
            "Transactions": ["PURCHASE ax", "PurCHAse b", "purchase c"],
            "Location": ["London", "Manchester", "London"],
            "Paid out": ["£100.00", "", "£254.23"],
            "Paid in": ["", "£10.00", ""]
        }
       
        # Amazon.co.uk*HB8CO4G74
        nw_imported_data = pd.DataFrame({
            "Date": pd.to_datetime(["2022-01-01", "2022-01-31", "2022-02-02"]),
            "payment type": [1, 1, 1],
            "info": ["info 1", "info 1", "info 1"],
            "Transactions": ["Purchase A", "Purchase B", "Purchase C"],
            "Location": ["London", "Manchester", "London"],
            "Paid out": ["100.00", "", "254.23"],
            "Paid in": ["", "10.00", ""],
            "category": ["category 1", "category 1", "category 1"],
            "Tags": ["tag1 tag2", "tag1 tag2", "tag1 tag2"],
        })
        nw_amazon_data = pd.DataFrame({
            "Date": pd.to_datetime(["2022-01-01", "2022-01-31", "2022-02-02"]),
            "payment type": [1, 1, 1],
            "info": ["info 1", "info 1", "info 1"],
            "Transactions": ["AmaZOn.co.uk*HB8CO4G74", "AMZNMktplace", "Purchase C"],
            "Location": ["London", "Manchester", "London"],
            "Paid out": ["100.00", "", "254.23"],
            "Paid in": ["", "10.00", ""],
            "category": ["category 1", "category 1", "category 1"],
            "Tags": ["tag1 tag2", "tag1 tag2", "tag1 tag2"],
        })
        amazon_capped_data = pd.DataFrame({
            "Date": pd.to_datetime(["2022-01-01", "2022-01-31", "2022-02-02", "2024-02-02"]),
            "payment type": [1, 1, 1,1],
            "info": ["info 1", "info 1", "info 1", "info 1"],
            "Transactions": ["Amazon.co.uk*hb8co4g74", "Amznmktplace", "Www.amazon* 204-33", "DIrECt DeBIT PAYMENT"],
            "Location": ["London", "Manchester", "London", "Chicago"],
            "Paid out": ["100.00", "", "254.23", "2030.34"],
            "Paid in": ["", "10.00", "", ""],
            "category": ["category 1", "category 1", "category 1", "snood farm"],
            "Tags": ["tag1 tag2", "tag1 tag2", "tag1 tag2", "tag3 tag4"],
        })

        self.input_df = pd.DataFrame(nw_src_data)
        self.nw_imported_data = pd.DataFrame(nw_imported_data)
        self.nw_amazon_data = pd.DataFrame(nw_amazon_data)
        self.amazon_capped_data = pd.DataFrame(amazon_capped_data)
        
    #@unittest.skip('Work in progress')
    def test_preprocess_data(self):
        expected_output = pd.DataFrame({
            "Date": pd.to_datetime(["2022-01-01", "2022-01-31", "2022-02-02"]),
            "payment type": [1, 1, 1],
            "info": ["info 1", "info 1", "info 1"],
            "Transactions": ["Purchase ax", "Purchase b", "Purchase c"],
            "Location": ["London", "Manchester", "London"],
            "Paid out": ["100.00", "", "254.23"],
            "Paid in": ["", "10.00", ""],
            "category": ["category 1", "category 1", "category 1"],
            "Tags": ["tag1 tag2", "tag1 tag2", "tag1 tag2"],
        })

        actual_output = set_placeholder_values(self.input_df)

        # Compare DataFrames
        pd.testing.assert_frame_equal(expected_output, actual_output)

    #@unittest.skip('Work in progress')
    def test_first_last_in_statement(self):
        expected_output = pd.DataFrame({
            "Date": pd.to_datetime(["2022-01-01", "2022-01-31", "2022-02-02"]),
            "payment type": [1, 1, 1],
            "info": ["First transaction in statement", "info 1", "Last transaction in statement"],
            "Transactions": ["Purchase A", "Purchase B", "Purchase C"],
            "Location": ["London", "Manchester", "London"],
            "Paid out": ["100.00", "", "254.23"],
            "Paid in": ["", "10.00", ""],
            "category": ["category 1", "category 1", "category 1"],
            "Tags": ["tag1 tag2", "tag1 tag2", "tag1 tag2"],
        })

        actual_output = mark_statement_boundary(self.nw_imported_data)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_lcase_for_txns(self):
        expected_output = pd.DataFrame({
            "Date": pd.to_datetime(["2022-01-01", "2022-01-31", "2022-02-02"]),
            "payment type": [1, 1, 1],
            "info": ["info 1", "info 1", "info 1"],
            "Transactions": ["Amazon.co.uk*hb8co4g74", "Amznmktplace", "Purchase c"],
            "Location": ["London", "Manchester", "London"],
            "Paid out": ["100.00", "", "254.23"],
            "Paid in": ["", "10.00", ""],
            "category": ["category 1", "category 1", "category 1"],
            "Tags": ["tag1 tag2", "tag1 tag2", "tag1 tag2"],
        })


        actual_output = set_placeholder_values(self.nw_amazon_data)
        pd.testing.assert_frame_equal(expected_output, actual_output)


    def test_special_payees(self):
            expected_output = pd.DataFrame({
                "Date": pd.to_datetime(["2022-01-01", "2022-01-31", "2022-02-02", "2024-02-02"]),
                "payment type": ["1", "1", "1", "11"],
                "info": ["info 1", "info 1", "info 1", "info 1"],
                "Transactions": ["Amazon", "Amazon", "Amazon", "DIrECt DeBIT PAYMENT"],
                "Location": ["London", "Manchester", "London", "Chicago"],
                "Paid out": ["100.00", "", "254.23", "2030.34"],
                "Paid in": ["", "10.00", "", ""],
                "category": ["category 1", "category 1", "category 1", "snood farm"],
                "Tags": ["tag1 tag2", "tag1 tag2", "tag1 tag2", "tag3 tag4"],
            })
            pprint(self.amazon_capped_data)
            x = expected_output.iloc[:, 0]
            actual_output = handle_special_payees(self.amazon_capped_data)
            pprint(actual_output)
            pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_format_paid_columns_handles_string_amounts_and_blanks(self):
        input_df = pd.DataFrame({
            "Paid out": pd.Series(["100.00", ""], dtype="string"),
            "Paid in": pd.Series([pd.NA, "10.00"], dtype="string"),
        })

        actual_output = format_paid_columns(input_df)

        pd.testing.assert_series_equal(
            actual_output["Paid"],
            pd.Series([-100.0, 10.0], name="Paid"),
        )

    def test_preprocess_data_handles_misdecoded_currency_symbol(self):
        input_df = self.input_df.copy()
        input_df["Paid out"] = ["�100.00", "", "�254.23"]
        input_df["Paid in"] = ["", "�10.00", ""]

        actual_output = format_paid_columns(set_placeholder_values(input_df))

        pd.testing.assert_series_equal(
            actual_output["Paid"],
            pd.Series([-100.0, 10.0, -254.23], name="Paid"),
        )

        
if __name__ == "__main__":
    unittest.main()
