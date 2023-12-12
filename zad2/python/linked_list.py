from typing import Any, TypeAlias

DataType: TypeAlias = 0 | 1 | 2 | 3



class Node:
    def __init__(self, data_type: DataType, data: Any):
        self.data_type = data_type
        self.data = data
        self.next = None
