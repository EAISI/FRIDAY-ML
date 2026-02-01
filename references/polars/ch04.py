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
    # Chapter 4: Data Structures and Data Types
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
    ## Series, DataFrames, and LazyFrames
    """)
    return


@app.cell
def _(pl):
    sales_series = pl.Series("sales", [150.00, 300.00, 250.00])

    sales_series
    return (sales_series,)


@app.cell
def _(pl, sales_series):
    sales_df = pl.DataFrame(
        {
            "sales": sales_series,
            "customer_id": [24, 25, 26],
        }
    )

    sales_df
    return


@app.cell
def _(pl):
    lazy_df = pl.scan_csv("data/fruit.csv").with_columns(
        is_heavy=pl.col("weight") > 200
    )

    lazy_df.show_graph()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Types
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Nested Data Types
    """)
    return


@app.cell
def _(pl):
    coordinates = pl.DataFrame(
        [
            pl.Series("point_2d", [[1, 3], [2, 5]]),
            pl.Series("point_3d", [[1, 7, 3], [8, 1, 0]]),
        ],
        schema={
            "point_2d": pl.Array(shape=2, inner=pl.Int64),
            "point_3d": pl.Array(shape=3, inner=pl.Int64),
        },
    )

    coordinates
    return


@app.cell
def _(pl):
    weather_readings = pl.DataFrame(
        {
            "temperature": [[72.5, 75.0, 77.3], [68.0, 70.2]],
            "wind_speed": [[15, 20], [10, 12, 14, 16]],
        }
    )

    weather_readings
    return


@app.cell
def _(pl):
    rating_series = pl.Series(
        "ratings",
        [
            {"Movie": "Cars", "Theatre": "NE", "Avg_Rating": 4.5},
            {"Movie": "Toy Story", "Theatre": "ME", "Avg_Rating": 4.9},
        ],
    )
    rating_series
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Missing Values
    """)
    return


@app.cell
def _(pl):
    missing_df = pl.DataFrame(
        {
            "value": [None, 2, 3, 4, None, None, 7, 8, 9, None],
        },
    )
    missing_df
    return (missing_df,)


@app.cell
def _(missing_df, pl):
    missing_df.with_columns(filled_with_single=pl.col("value").fill_null(-1))
    return


@app.cell
def _(missing_df, pl):
    missing_df.with_columns(
        forward=pl.col("value").fill_null(strategy="forward"),
        backward=pl.col("value").fill_null(strategy="backward"),
        min=pl.col("value").fill_null(strategy="min"),
        max=pl.col("value").fill_null(strategy="max"),
        mean=pl.col("value").fill_null(strategy="mean"),
        zero=pl.col("value").fill_null(strategy="zero"),
        one=pl.col("value").fill_null(strategy="one"),
    )
    return


@app.cell
def _(missing_df, pl):
    missing_df.with_columns(
        expression_mean=pl.col("value").fill_null(pl.col("value").mean())
    )
    return


@app.cell
def _(missing_df):
    missing_df.interpolate()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Type Conversion
    """)
    return


@app.cell
def _(pl):
    string_df = pl.DataFrame({"id": ["10000", "20000", "30000"]})
    print(string_df)
    print(f"Estimated size: {string_df.estimated_size('b')} bytes")
    return (string_df,)


@app.cell
def _(pl, string_df):
    int_df = string_df.select(pl.col("id").cast(pl.UInt16))
    print(int_df)
    print(f"Estimated size: {int_df.estimated_size('b')} bytes")
    return


@app.cell
def _(pl):
    data_types_df = pl.DataFrame(
        {
            "id": [10000, 20000, 30000],
            "value": [1.0, 2.0, 3.0],
            "value2": ["1", "2", "3"],
        }
    )

    data_types_df.cast(pl.UInt16)
    return (data_types_df,)


@app.cell
def _(data_types_df, pl):
    data_types_df.cast({"id": pl.UInt16, "value": pl.Float32, "value2": pl.UInt8})
    return


@app.cell
def _(data_types_df, pl):
    data_types_df.cast({pl.Float64: pl.Float32, pl.String: pl.UInt8})
    return


@app.cell
def _(data_types_df, pl):
    import polars.selectors as cs

    data_types_df.cast({cs.numeric(): pl.UInt16})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
