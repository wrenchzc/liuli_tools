from excel_merge.excel_handler import merge_excel
import xlrd

def test_excel_merge():
    dest_file = merge_excel("tests/liuli_test.xlsx")
    excel_read_book = xlrd.open_workbook(dest_file)
    trans_sheet = excel_read_book.sheet_by_index(1)
    refund_sheet = excel_read_book.sheet_by_index(2)

    assert trans_sheet.cell(1, 5).value == 321.1904
    assert trans_sheet.cell(2, 5).value == 422.01423
    v = trans_sheet.cell(3, 5).value
    assert v is None or str(v).strip() == '-' or str(v).strip() == ''

    assert refund_sheet.cell(1, 13).value == ""
    assert refund_sheet.cell(2, 13).value == "not found in trans"
    assert refund_sheet.cell(3, 13).value == "not found in trans"




