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
    # Chapter 7: Beginning Expressions
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
    ## Methods and Namespaces
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Expressions by Example
    """)
    return


@app.cell
def _(pl):
    fruit = pl.read_csv("data/fruit.csv")
    fruit
    return (fruit,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Selecting Columns with Expressions
    """)
    return


@app.cell
def _(fruit, pl):
    fruit.select(
        pl.col("name"),  
        pl.col("^.*or.*$"),  
        pl.col("weight") / 1000,  
        "is_round",  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Creating New Columns with Expressions
    """)
    return


@app.cell
def _(fruit, pl):
    fruit.with_columns(
        pl.lit(True).alias("is_fruit"),  
        is_berry=pl.col("name").str.ends_with("berry"),  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtering Rows with Expressions
    """)
    return


@app.cell
def _(fruit, pl):
    fruit.filter(
        (pl.col("weight") > 1000)  
        & pl.col("is_round")  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aggregating with Expressions
    """)
    return


@app.cell
def _(fruit, pl):
    fruit.group_by(pl.col("origin").str.split(" ").list.last()).agg(  
        pl.len(),  
        average_weight=pl.col("weight").mean()  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting Rows with Expressions
    """)
    return


@app.cell
def _(fruit, pl):
    fruit.sort(
        pl.col("name").str.len_bytes(),  # <1> <2>
        descending=True,  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Definition of an Expression
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"a": [1, 2, 3], "b": [0.4, 0.5, 0.6]}).with_columns(
            pl.all().mul(10).name.suffix("_times_10")
        )
    )
    return


@app.cell
def _(pl):
    pl.all().mul(10).name.suffix("_times_10").meta.has_multiple_outputs()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Properties of Expressions
    """)
    return


@app.cell
def _(fruit, pl):
    is_orange = (pl.col("color") == "orange").alias("is_orange")

    fruit.with_columns(is_orange)
    return (is_orange,)


@app.cell
def _(fruit, is_orange):
    fruit.filter(is_orange)
    return


@app.cell
def _(fruit, is_orange):
    fruit.group_by(is_orange).len()
    return


@app.cell
def _(is_orange, pl):
    flowers = pl.DataFrame(
        {
            "name": ["Tiger lily", "Blue flag", "African marigold"],
            "latin": ["Lilium columbianum", "Iris versicolor", "Tagetes erecta"],
            "color": ["orange", "purple", "orange"],
        }
    )

    flowers.filter(is_orange)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating Expressions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### From Existing Columns
    """)
    return


@app.cell
def _(fruit, pl):
    fruit.select(pl.col("color")).columns
    return


@app.cell
def _():
    # This raises a ColumnNotFoundError:
    # fruit.select(pl.col("is_smelly")).columns
    return


@app.cell
def _(fruit, pl):
    fruit.select(pl.col("^.*or.*$")).columns
    return


@app.cell
def _(fruit, pl):
    fruit.select(pl.all()).columns
    return


@app.cell
def _(fruit, pl):
    fruit.select(pl.col(pl.String)).columns
    return


@app.cell
def _(fruit, pl):
    fruit.select(pl.col(pl.Boolean, pl.Int64)).columns
    return


@app.cell
def _(fruit, pl):
    fruit.select(pl.col(["name", "color"])).columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### From Literal Values
    """)
    return


@app.cell
def _(pl):
    pl.select(pl.lit(42))
    return


@app.cell
def _(pl):
    pl.select(pl.lit(42).alias("answer"))
    return


@app.cell
def _(pl):
    pl.select(answer=pl.lit(42))
    return


@app.cell
def _(fruit, pl):
    fruit.with_columns(planet=pl.lit("Earth"))
    return


@app.cell
def _():
    # This raises a ShapeError:
    # fruit.with_columns(pl.lit(pl.Series([False, True])).alias("row_is_even"))
    return


@app.cell
def _(fruit, pl):
    fruit.with_columns(row_is_even=pl.lit([False, True]))
    return


@app.cell
def _(pl):
    pl.select(pl.repeat("Ella", 3).alias("umbrella"), pl.zeros(3), pl.ones(3))
    return


@app.cell
def _():
    # This raises a ShapeError:
    # fruit.with_columns(planet=pl.repeat("Earth", 9))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### From Ranges
    """)
    return


@app.cell
def _(pl):
    pl.select(
        start=pl.int_range(0, 5), end=pl.arange(0, 10, 2).pow(2)
    ).with_columns(int_range=pl.int_ranges("start", "end")).with_columns(
        range_length=pl.col("int_range").list.len()
    )
    return


@app.cell
def _(pl):
    pl.select(
        start=pl.date_range(pl.date(1985, 10, 21), pl.date(1985, 10, 26)),
        end=pl.repeat(pl.date(2021, 10, 21), 6),
    ).with_columns(range=pl.datetime_ranges("start", "end", interval="1h"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Functions to Create Expressions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Renaming Expressions
    """)
    return


@app.cell
def _(pl):
    df = pl.DataFrame({"text": "value", "An integer": 5040, "BOOLEAN": True})
    df
    return (df,)


@app.cell
def _(df, pl):
    df.select(
        pl.col("text").name.to_uppercase(),
        pl.col("An integer").alias("int"),
        pl.col("BOOLEAN").name.to_lowercase(),
    )
    return


@app.cell
def _():
    # This raises an InvalidOperationError:
    # df.select(
    #     pl.all()
    #     .name.to_lowercase()
    #     .name.map(lambda s: s.replace(" ", "_"))
    # )
    return


@app.cell
def _(df, pl):
    df.select(
        pl.all().name.map(lambda s: s.lower().replace(" ", "_"))
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Expressions Are Idiomatic
    """)
    return


@app.cell
def _(fruit):
    fruit.filter((fruit["weight"] > 1000) & fruit["is_round"])
    return


@app.cell
def _(fruit, pl):
    (
        fruit.lazy()
        .filter((pl.col("weight") > 1000) & pl.col("is_round"))
        .with_columns(is_berry=pl.col("name").str.ends_with("berry"))
        .collect()
    )
    return


@app.cell
def _():
    # This raises a ShapeError:
    # (
    #     fruit
    #     .lazy()
    #     .filter((fruit["weight"] > 1000) & fruit["is_round"])
    #     .with_columns(is_berry=fruit["name"].str.ends_with("berry"))
    #     .collect()
    # )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
