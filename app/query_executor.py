## Imports
import io
import contextlib

## Functions
def execute_query(code: str, df):
    """
    Executes dynamically generated code using the given DataFrame.
    Captures and returns printed output or error messages.
    """
    try:
        # Create an isolated local context with access only to the dataframe
        local_vars = {"df": df.copy()}
        stdout = io.StringIO()

        # Capture any printed output
        with contextlib.redirect_stdout(stdout):
            exec(code, {}, local_vars)

        # Get printed result
        result = stdout.getvalue().strip()

        return result if result else "No result."

    except Exception as e:
        error_msg = str(e)
        if "filter" in code or ".filter" in error_msg:
            return "[ERROR] Invalid use of `.filter()`. Use df[...] instead."
        return f"[ERROR] {error_msg}"
