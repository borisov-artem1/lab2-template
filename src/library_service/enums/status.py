from enum import Enum


class ConditionStatus(str, Enum):
    EXCELLENT = 'EXCELLENT'
    GOOD = 'GOOD'
    BAD = 'BAD'


# class PrivilegeHistoryStatus(str, Enum):
#     FILL_IN_BALANCE = 'FILL_IN_BALANCE'
#     DEBIT_THE_ACCOUNT = 'DEBIT_THE_ACCOUNT'
