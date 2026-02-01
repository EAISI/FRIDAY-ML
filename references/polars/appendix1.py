import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Accelerating Polars with the GPU
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
    ## NVIDIA RAPIDS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Installing the GPU Engine
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 1: Install WSL2 on Windows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2: Install Ubuntu Linux on WSL2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 3: Install Prerequisite Ubuntu Linux Packages
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 4: Install the CUDA Toolkit
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 5: Install Python Dependencies
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 6: Test Your Installation
    """)
    return


@app.cell
def _(pl):
    pl.LazyFrame({'x': [1, 2, 3]}).collect(engine=pl.GPUEngine(raise_on_fail=True))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Using the Polars GPU Engine
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Configuration
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Unsupported Features
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Benchmarking the Polars GPU Engine
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solutions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Queries and Data
    """)
    return


@app.cell
def _(pl):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    lineitem = pl.scan_parquet("data/benchmark/lineitem.parquet")  
    supplier = pl.scan_parquet("data/benchmark/supplier.parquet")

    var1 = pl.date(1996, 1, 1)
    var2 = pl.date(1996, 4, 1)

    revenue = (
        lineitem.filter(pl.col("l_shipdate").is_between(var1, var2, closed="left"))
        .group_by("l_suppkey")
        .agg(
            (pl.col("l_extendedprice") * (1 - pl.col("l_discount")))
            .sum()
            .alias("total_revenue")
        )
        .select(pl.col("l_suppkey").alias("supplier_no"), pl.col("total_revenue"))
    )

    query_15 = (
        supplier.join(revenue, left_on="s_suppkey", right_on="supplier_no")
        .filter(pl.col("total_revenue") == pl.col("total_revenue").max())
        .with_columns(pl.col("total_revenue").round(2))
        .select("s_suppkey", "s_name", "s_address", "s_phone", "total_revenue")
        .sort("s_suppkey")
    )

    query_15.collect(engine="cpu")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Method
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Results and Discussion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Polars GPU engine versus CPU engine
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Performance on different hardware
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Polars GPU engine versus other packages
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### The effect of the Polars optimizer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Conclusion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Future of Polars on the GPU
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
