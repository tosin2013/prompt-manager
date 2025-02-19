"""Bazel build file for CLI tests."""

load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_base_commands",
    srcs = ["test_base_commands.py"],
    deps = [
        "//prompt_manager/cli",
        "//prompt_manager:prompt_manager_lib",
    ],
)

py_test(
    name = "test_debug_commands",
    srcs = ["test_debug_commands.py"],
    deps = [
        "//prompt_manager/cli",
        "//prompt_manager:prompt_manager_lib",
    ],
)

py_test(
    name = "test_llm_commands",
    srcs = ["test_llm_commands.py"],
    deps = [
        "//prompt_manager/cli",
        "//prompt_manager:prompt_manager_lib",
    ],
)
