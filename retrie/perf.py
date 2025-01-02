import timeit

# Define constants
DEFAULT = object()

# # Functions to compare
# def check_none(x) -> bool:
#     return x is None


# def check_default(x) -> bool:
#     return x is DEFAULT


# Benchmark setup
setup_code = """
DEFAULT = object()
def check_none(x):
    return x is None

def check_default(x):
    return x is DEFAULT
"""

# Measure execution time
none_time = timeit.timeit("check_none(None)", setup=setup_code, number=10_000_000)
default_time = timeit.timeit(
    "check_default(DEFAULT)", setup=setup_code, number=10_000_000,
)

print(none_time, default_time)
