load("@rules_python//python:defs.bzl", "py_test")
load("@pip//:requirements.bzl", "requirement")

py_test(
    name = "prompt_manager_test",
    srcs = ["test_prompt_manager.py"],
    deps = [
        "//:prompt_manager_lib",
        requirement("pytest"),
    ],
)

py_test(
    name = "test_llm_enhancement",
    srcs = ["test_llm_enhancement.py"],
    deps = [
        "//:prompt_manager_lib",
        requirement("pytest"),
    ],
)
