import collections
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook

Item = collections.namedtuple("Item", ("weight", "value"))


def optimum_subject_to_capacity(items: List[Item], capacity: int) -> int:
    dp = [0] * (1 + capacity)
    tmp = [0] * (1 + capacity)
    for item in items:
        for weight in range(1, capacity + 1):
            tmp[weight] = dp[weight]
            if item.weight <= weight:
                tmp[weight] = max(tmp[weight], dp[weight - item.weight] + item.value)
        dp, tmp = tmp, dp

    return dp[-1]


@enable_executor_hook
def optimum_subject_to_capacity_wrapper(executor, items, capacity):
    items = [Item(*i) for i in items]
    return executor.run(functools.partial(optimum_subject_to_capacity, items, capacity))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "knapsack.py", "knapsack.tsv", optimum_subject_to_capacity_wrapper
        )
    )
