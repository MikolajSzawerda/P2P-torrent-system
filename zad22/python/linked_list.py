from typing import Any, TypeAlias

DataType: TypeAlias = 0 | 1 | 2 | 3

DATA_TYPE_MAPPING = {
    0: "int16",
    1: "int32",
    2: "fixed",
    3: "var-size",
}


class Node:
    def __init__(self, data_type: DataType, data: Any):
        self.data_type = data_type
        self.data = data
        self.next = None

    def display(self):
        curr = self
        while curr:
            print(f"{curr.data} (type: {DATA_TYPE_MAPPING[curr.data_type]})")
            curr = curr.next
