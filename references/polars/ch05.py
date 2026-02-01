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
    # Chapter 5: Eager and Lazy APIs
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
    ## Eager API: DataFrame
    """)
    return


@app.cell
def _(pl):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    _trips = pl.read_parquet('data/taxi/yellow_tripdata_*.parquet')
    _sum_per_vendor = _trips.group_by('VendorID').sum()
    _income_per_distance_per_vendor = _sum_per_vendor.select('VendorID', income_per_distance=pl.col('total_amount') / pl.col('trip_distance'))
    _top_three = _income_per_distance_per_vendor.sort(by='income_per_distance', descending=True).head(3)
    _top_three
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lazy API: LazyFrame
    """)
    return


@app.cell
def _():
    # This raises a SchemaError:
    # names_lf = pl.LazyFrame({"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]})

    # erroneous_query = names_lf.with_columns(
    #     sliced_age=pl.col("age").str.slice(1, 3)
    # )

    # result_df = erroneous_query.collect()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Performance Differences
    """)
    return


@app.cell
def _(pl):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    _trips = pl.scan_parquet('data/taxi/yellow_tripdata_*.parquet')
    _sum_per_vendor = _trips.group_by('VendorID').sum()
    _income_per_distance_per_vendor = _sum_per_vendor.select('VendorID', income_per_distance=pl.col('total_amount') / pl.col('trip_distance'))
    _top_three = _income_per_distance_per_vendor.sort(by='income_per_distance', descending=True).head(3)
    _top_three.collect()
    return


@app.cell
def _(pl):
    _lf = pl.LazyFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
    print(_lf.collect())
    # ... Some heavy computation ...
    print(_lf.with_columns(pl.col('col1') + 1).collect())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Functionality Differences
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Attributes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aggregation Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Computation Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Descriptive Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### GroupBy Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exporting Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Manipulation and Selection Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Miscellaneous Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tips and Tricks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Going from LazyFrame to DataFrame and Vice Versa
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Joining a DataFrame with a LazyFrame
    """)
    return


@app.cell
def _():
    # This raises a TypeError:
    # big_sales_data = pl.LazyFrame(
    #     {"sale_id": [101, 102, 103], "amount": [250, 150, 300]}
    # )
    #
    # sales_metadata = pl.DataFrame(
    #     {"sale_id": [101, 102, 103], "category": ["A", "B", "A"]}
    # )
    #
    # big_sales_data.join(sales_metadata, on="sale_id").collect()
    return


@app.cell
def _(pl):
    big_sales_data = pl.LazyFrame(
        {"sale_id": [101, 102, 103], "amount": [250, 150, 300]}
    )

    sales_metadata = pl.DataFrame(
        {"sale_id": [101, 102, 103], "category": ["A", "B", "A"]}
    )

    big_sales_data.join(sales_metadata.lazy(), on="sale_id").collect()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Caching Intermittent Results
    """)
    return


@app.cell
def _(pl):
    _lf = pl.LazyFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
    _lf = _lf.collect().lazy()
    # ... Some heavy computation ...
    print(_lf.collect())
    print(_lf.with_columns(pl.col('col1') + 1).collect())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
