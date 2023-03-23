import pandas as pd
import io

#  packTable   Py :: pack   => (["str"], [["str"]]) -> ""


def packTable(serial):
    tableStr = "\n".join([",".join(row) for row in serial[1]])
    table = pd.read_csv(io.StringIO(tableStr), header=serial[0])
    return table

#  unpackTable Py :: unpack => "" -> (["str"], [["str"]])
def unpackTable(table):
    pass
