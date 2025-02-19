load("@rules_python//python:defs.bzl", "py_library")

# Common library that works with both Python versions
py_library(
    name = "prompt_manager_lib",
    srcs = glob(["prompt_manager/**/*.py"]),
    visibility = ["//visibility:public"],
)

# Python 3.9 specific target
py_library(
    name = "prompt_manager_py39",
    deps = [":prompt_manager_lib"],
    tags = ["python3.9"],
    visibility = ["//visibility:public"],
)

# Python 3.13 specific target
py_library(
    name = "prompt_manager_py313",
    deps = [":prompt_manager_lib"],
    tags = ["python3.13"],
    visibility = ["//visibility:public"],
)
