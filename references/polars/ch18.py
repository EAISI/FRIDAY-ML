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
    # Chapter 18: Polars Internals
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
    ## Polars' Architecture
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Arrow
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Multithreaded Computations and SIMD Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The String Data Type in Memory
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ChunkedArrays in Series
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Query Optimization
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### LazyFrame Scan-Level Optimizations
    """)
    return


@app.cell
def _(pl):
    taxis = pl.scan_parquet("data/taxi/yellow_tripdata_*.parquet")  
    taxis.select(pl.col("trip_distance")).show_graph()
    return (taxis,)


@app.cell
def _(pl, taxis):
    taxis.filter(pl.col("trip_distance") > 10).show_graph()
    return


@app.cell
def _(taxis):
    taxis.head(2).collect()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Optimizations
    """)
    return


@app.cell
def _(pl):
    values = pl.LazyFrame({"value": [10, 20, 30, 40, 50, 60]})

    common_subplan = values.with_columns(pl.col("value") * 2)

    branch1 = common_subplan.select(value2=pl.col("value") * 4)
    branch2 = common_subplan.select(value3=pl.col("value") * 2)

    combined = pl.concat([branch1, branch2])

    combined.show_graph(optimized=False)
    return (combined,)


@app.cell
def _(combined):
    combined.show_graph()
    return


@app.cell
def _(pl):
    bmi = pl.LazyFrame(
        {"weight_kg": [70, 80, 60, 90], "length_cm": [175, 180, 160, 190]}
    )
    return (bmi,)


@app.cell
def _(bmi, pl):
    bmi_1 = bmi.with_columns(weight_per_cm=pl.col('weight_kg') / pl.col('length_cm')).with_columns(weight_kg_average=pl.lit(0)).with_columns(length_m=pl.col('length_cm') / 100).with_columns(weight_kg_average=pl.col('weight_kg').mean())
    return (bmi_1,)


@app.cell
def _(bmi_1, pl):
    bmi_2 = bmi_1.with_columns(weight_per_cm=pl.col('weight_kg') / pl.col('length_cm'), weight_kg_average=pl.col('weight_kg').mean(), length_m=pl.col('length_cm') / 100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Checking Your Expressions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### meta Namespace Overview
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### meta Namespace Examples
    """)
    return


@app.cell
def _(pl):
    expr1 = pl.col("name")
    expr2 = pl.lit("constant")

    print(f"Is {expr1} a column: {expr1.meta.is_column()}")
    print(f"Is {expr2} a column: {expr2.meta.is_column()}")
    return expr1, expr2


@app.cell
def _(expr1, expr2):
    print(f"Is {expr1} a literal: {expr1.meta.is_literal()}")
    print(f"Is {expr2} a literal: {expr2.meta.is_literal()}")
    return


@app.cell
def _(pl):
    expr1_1 = pl.col('age') * 2
    expr2_1 = pl.col('name').alias('username')
    print(f'{expr1_1} output name: {expr1_1.meta.output_name()}')
    # Get output names
    print(f'{expr2_1} output name: {expr2_1.meta.output_name()}')
    return


@app.cell
def _(pl):
    _expr = (pl.col('age') * 2).alias('double_age')
    _expr.meta.show_graph()
    return


@app.cell
def _(pl):
    _expr = pl.col('original_name').alias('new_name')
    original_expr = _expr.meta.undo_aliases()
    original_expr.meta.output_name()
    return


@app.cell
def _(pl):
    _expr = pl.col('origin').alias('destination')
    _expr.meta.root_names()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Profiling Polars
    """)
    return


@app.cell
def _(pl):
    long_distance_taxis_per_vendor_sorted = (
        pl.scan_parquet("data/taxi/yellow_tripdata_*.parquet")
        .filter(pl.col("trip_distance") > 10)
        .select(pl.col("VendorID"), pl.col("trip_distance"), pl.col("total_amount"))
        .group_by("VendorID")
        .agg(
            total_distance=pl.col("trip_distance").sum(),
            total_amount=pl.col("total_amount").sum(),
        )
        .sort("total_distance", descending=True)
    )

    long_distance_taxis_per_vendor_sorted.show_graph()
    return (long_distance_taxis_per_vendor_sorted,)


@app.cell
def _(long_distance_taxis_per_vendor_sorted):
    result, profiling_info = long_distance_taxis_per_vendor_sorted.profile()
    return profiling_info, result


@app.cell
def _(result):
    result
    return


@app.cell
def _(profiling_info):
    profiling_info
    return


@app.cell
def _(long_distance_taxis_per_vendor_sorted):
    long_distance_taxis_per_vendor_sorted.profile(show_plot=True, figsize=(15, 5))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tests in Polars
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Comparing DataFrames and Series
    """)
    return


@app.cell
def _():
    from polars.testing import (
        assert_series_equal,
        assert_frame_equal,
        assert_series_not_equal,
        assert_frame_not_equal,
    )
    return (assert_frame_equal,)


@app.cell
def _(pl):
    floats = pl.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})

    different_floats = pl.DataFrame({"a": [1.001, 2.0, 3.0, 4.0]})
    return different_floats, floats


@app.cell
def _():
    # This raises an AssertionError:
    # assert_frame_equal(floats, different_floats)
    return


@app.cell
def _(assert_frame_equal, different_floats, floats):
    assert_frame_equal(floats, different_floats, rel_tol=0.01)
    print("The DataFrames are equal.")
    return


@app.cell
def _(assert_frame_equal, pl):
    result_1 = pl.DataFrame({'a': [1, 3], 'b': [2, 4]}).cast(pl.Schema({'a': pl.Int8, 'b': pl.Int8}))
    expected = pl.from_repr('\n┌─────┬─────┐\n│ a   ┆ b   │\n│ --- ┆ --- │\n│ i8  ┆ i8  │\n╞═════╪═════╡\n│ 1   ┆ 2   │\n│ 3   ┆ 4   │\n└─────┴─────┘\n    ')
    assert_frame_equal(result_1, expected)
    print('DataFrames are equal')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Common Antipatterns
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Using Brackets for Column Selection
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Misusing Collect
    """)
    return


@app.cell
def _(pl):
    taxis_1 = pl.scan_parquet('data/taxi/yellow_tripdata_*.parquet')
    _vendor0 = taxis_1.filter(pl.col('VendorID') == 0).collect()
    _vendor1 = taxis_1.filter(pl.col('VendorID') == 1).collect()
    return


@app.cell
def _(pl):
    taxis_2 = pl.scan_parquet('data/taxi/yellow_tripdata_*.parquet')
    vendors = taxis_2.filter(pl.col('VendorID').is_in([0, 1])).collect()
    _vendor0 = vendors.filter(pl.col('VendorID') == 0)
    _vendor1 = vendors.filter(pl.col('VendorID') == 1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Using Python Code in your Polars Queries
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
