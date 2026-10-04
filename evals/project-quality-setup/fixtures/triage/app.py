"""Synthetic source for static inspection only; do not execute expressions."""

def calculate(request_expression):
    # request_expression comes directly from an untrusted API request.
    return eval(request_expression)
