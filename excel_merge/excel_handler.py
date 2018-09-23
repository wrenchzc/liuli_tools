import xlrd
import xlwt
from xlutils.copy import copy
import os
from tempfile import mktemp


def get_refund_by_id(refund_ids, refund_amounts, trans_id) -> float:
    amount = 0
    for row_index, refund_id in enumerate(refund_ids):
        if not refund_id:
            continue
        refund_id = refund_id.strip()
        if refund_id == trans_id:
            amount = amount + float(refund_amounts[row_index])

    return amount

def strip_strs(strs: list):
    return [str(item).strip() for item in strs if item is not None]


def merge_excel(filename: str):
    if not os.path.exists(filename):
        raise FileNotFoundError

    excel_read_book = xlrd.open_workbook(filename)
    excel_write = copy(excel_read_book)
    w_trans_sheet = excel_write.get_sheet(1)
    w_refund_sheet = excel_write.get_sheet(2)

    sheet_trans = excel_read_book.sheet_by_index(1)
    sheet_refund = excel_read_book.sheet_by_index(2)

    trans_ids = strip_strs(sheet_trans.col_values(0))
    trans_rate = strip_strs(sheet_trans.col_values(9))
    refund_ids = strip_strs(sheet_refund.col_values(0))
    refund_amounts = strip_strs(sheet_refund.col_values(8))

    for row_index, trans_id in enumerate(trans_ids):
        # first line is head
        if row_index == 0:
            continue

        if not isinstance(trans_id, str):
            continue

        trans_id = trans_id.strip()
        refund_amount = get_refund_by_id(refund_ids, refund_amounts, trans_id)

        if refund_amount:
            try:
                rate = trans_rate[row_index]
                if not rate:
                    rate = 0

                if rate != 0:
                    w_trans_sheet.write(row_index, 5, str(refund_amount / float(rate)))
            except ValueError:
                print(trans_rate[row_index])

    for row_index, refund_id in enumerate(refund_ids):
        if refund_id not in trans_ids:
            w_refund_sheet.write(row_index, 13, "not found in trans")


    temp_xls_name = mktemp(".xls")
    excel_write.save(temp_xls_name)

    return temp_xls_name
