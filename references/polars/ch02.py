import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import subprocess
    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 2: Getting Started
    """)
    return


@app.cell
def _():
    import polars as pl
    pl.__version__  # The book is built with Polars version 1.20.0
    return (pl,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setting Up Your Environment
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Downloading the Project
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Installing uv
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Installing the Project
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Working with the Virtual Environment
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Verifying Your Installation
    """)
    return


@app.cell
def _(pl):
    pl.show_versions()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Crash Course in JupyterLab
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Keyboard Shortcuts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Any mode
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Command mode
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Edit mode
    """)
    return


@app.cell
def _(subprocess):
    #! ls
    subprocess.call(['ls'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Installing Polars on Other Projects
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### All Optional Dependencies
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional Dependencies for Interoperability
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional Dependencies for Working with Spreadsheets
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional Dependencies for Working with Databases
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional Dependencies for Working with Remote Filesystems
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional Dependencies for Other I/O Formats
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional Dependencies for Extra Functionality
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Installing Optional Dependencies
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Configuring Polars
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Temporary Configuration Using a Context Manager
    """)
    return


@app.cell
def _(pl):
    with pl.Config() as cfg:
        cfg.set_verbose(True)
        # Polars operation for which you want to see the verbose logging

    # Code outside of the scope is not affected
    return


@app.cell
def _(pl):
    with pl.Config(verbose=True):
        # Polars operation you want to see the verbose logging of
        pass
    return


@app.cell
def _(pl):
    import random
    import string


    def generate_random_string(length: int) -> str:
        return "".join(random.choice(string.ascii_letters) for i in range(length))


    data = {}
    for i in range(1, 11):
        data[f"column_{i}"] = [generate_random_string(50) for _ in range(5)]  

    df = pl.DataFrame(data)
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(df, pl):
    with pl.Config(tbl_cols=-1, fmt_str_lengths=4):
        print(df)
    return


@app.cell
def _():
    class YourContextManager:
        def __enter__(self):
            print("Entering context")

        def __exit__(self, type, value, traceback):
            print("Exiting context")


    with YourContextManager():
        print("Your code")
    return


@app.cell
def _():
    with open("data/fruit.csv", "r") as file:
        print(file.readline())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Local Configuration Using a Decorator
    """)
    return


@app.cell
def _(pl):
    @pl.Config(ascii_tables=True)
    def write_ascii_frame_to_stdout(df: pl.DataFrame) -> None:
        print(str(df))


    @pl.Config(verbose=True)
    def function_that_im_debugging(df: pl.DataFrame) -> None:
        # Polars operation for which you want to see the verbose logging
        pass
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compiling Polars from Scratch
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Edge Case: Very Large Datasets
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Edge Case: Processors Lacking AVX Support
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
