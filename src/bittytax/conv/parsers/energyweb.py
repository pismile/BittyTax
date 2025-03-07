# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2020

from decimal import Decimal

from ..dataparser import DataParser
from ..exceptions import UnexpectedTypeError
from ..out_record import TransactionOutRecord

WALLET = "Energy Web"


def parse_energy_web(data_row, parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict["UnixTimestamp"])

    if row_dict["Type"] == "IN":
        data_row.t_record = TransactionOutRecord(
            TransactionOutRecord.TYPE_DEPOSIT,
            data_row.timestamp,
            buy_quantity=Decimal(row_dict["Value"]) / 10**18,
            buy_asset="EWT",
            wallet=WALLET,
        )
    elif row_dict["Type"] == "OUT":
        data_row.t_record = TransactionOutRecord(
            TransactionOutRecord.TYPE_WITHDRAWAL,
            data_row.timestamp,
            sell_quantity=Decimal(row_dict["Value"]) / 10**18,
            sell_asset="EWT",
            fee_quantity=Decimal(row_dict["Fee"]) / 10**18,
            fee_asset="EWT",
            wallet=WALLET,
        )
    else:
        raise UnexpectedTypeError(parser.in_header.index("Type"), "Type", row_dict["Type"])


DataParser(
    DataParser.TYPE_EXPLORER,
    "Energy Web",
    [
        "TxHash",
        "BlockNumber",
        "UnixTimestamp",
        "FromAddress",
        "ToAddress",
        "ContractAddress",
        "Type",
        "Value",
        "Fee",
        "Status",
        "ErrCode",
        "CurrentPrice",
        "TxDateOpeningPrice",
        "TxDateClosingPrice",
    ],
    worksheet_name="Energy Web",
    row_handler=parse_energy_web,
)
