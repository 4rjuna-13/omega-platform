"""
Cleanup helpers for JAIDA (Phase 1.5).
Minimal refactoring without breaking existing code.
"""

def split_long_function(func, max_lines=30):
    """
    Utility to identify when to split functions.
    Returns True if function should be considered for splitting.
    """
    import inspect
    source = inspect.getsource(func)
    lines = source.split('\n')
    return len(lines) > max_lines

def add_function_docs():
    """Add missing docstrings to long functions."""
    # This is a placeholder - would use ast to analyze and add docs
    return "Use this to auto-add docstrings to functions > 20 lines"
