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
    # Chapter 9: Combining Expressions
    """)
    return


@app.cell
def _():
    import polars as pl
    pl.__version__  # The book is built with Polars version 1.20.0
    return (pl,)


@app.cell
def _(pl):
    fruit = pl.read_csv("data/fruit.csv")
    fruit.filter(pl.col("is_round") & (pl.col("weight") > 1000))
    return (fruit,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inline Operators Versus Methods
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"i": [6.0, 0, 2, 2.5], "j": [7.0, 1, 2, 3]}).with_columns(
            (pl.col("i") * pl.col("j")).alias("*"),
            pl.col("i").mul(pl.col("j")).alias("Expr.mul()"),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Arithmetic Operations
    """)
    return


@app.cell
def _(fruit, pl):
    fruit.select(pl.col("name"), (pl.col("weight") / 1000))
    return


@app.cell
def _(pl):
    pl.Config(float_precision=2, tbl_cell_numeric_alignment="RIGHT")  

    (
        pl.DataFrame({"i": [0.0, 2, 2, -2, -2], "j": [1, 2, 3, 4, -5]}).with_columns(
            (pl.col("i") + pl.col("j")).alias("i + j"),
            (pl.col("i") - pl.col("j")).alias("i - j"),
            (pl.col("i") * pl.col("j")).alias("i * j"),
            (pl.col("i") / pl.col("j")).alias("i / j"),
            (pl.col("i") // pl.col("j")).alias("i // j"),
            (pl.col("i") ** pl.col("j")).alias("i ** j"),
            (pl.col("j") % 2).alias("j % 2"),  
            pl.col("i").dot(pl.col("j")).alias("i ⋅ j"),  
        )
    )
    return


@app.cell
def _(pl):
    pl.Config.set_float_precision()
    pl.Config.set_tbl_cell_numeric_alignment(None)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Comparison Operations
    """)
    return


@app.cell
def _(pl):
    pl.select(pl.lit("a") > pl.lit("b"))
    return


@app.cell
def _(fruit, pl):
    (
        fruit.select(
            pl.col("name"),
            pl.col("weight"),
        ).filter(pl.col("weight") >= 1000)
    )
    return


@app.cell
def _():
    x = 4
    3 < x < 5
    return (x,)


@app.cell
def _():
    # This raises a TypeError:
    # pl.select(pl.lit(3) < pl.lit(x) < pl.lit(5))
    return


@app.cell
def _(pl, x):
    pl.select((pl.lit(3) < pl.lit(x)) & (pl.lit(x) < pl.lit(5))).item()
    return


@app.cell
def _(pl, x):
    pl.select(pl.lit(x).is_between(3, 5)).item()
    return


@app.cell
def _(pl):
    (
        pl.DataFrame(
            {"a": [-273.15, 0, 42, 100], "b": [1.4142, 2.7183, 42, 3.1415]}
        ).with_columns(
            (pl.col("a") == pl.col("b")).alias("a == b"),
            (pl.col("a") <= pl.col("b")).alias("a <= b"),
            (pl.all() > 0).name.suffix(" > 0"),
            ((pl.col("b") - pl.lit(2).sqrt()).abs() < 1e-3).alias("b ≈ √2"),  
            ((1 < pl.col("b")) & (pl.col("b") < 3)).alias("1 < b < 3"),
        )
    )
    return


@app.cell
def _(pl):
    pl.select(
        bool_num=pl.lit(True) > 0,
        time_time=pl.time(23, 58) > pl.time(0, 0),
        datetime_date=pl.datetime(1969, 7, 21, 2, 56) < pl.date(1976, 7, 20),
        str_num=pl.lit("5") < pl.lit(3).cast(pl.String),  
        datetime_time=pl.datetime(1999, 1, 1).dt.time() != pl.time(0, 0),  
    ).transpose(  
        include_header=True, header_name="comparison", column_names=["allowed"]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Boolean Algebra Operations
    """)
    return


@app.cell
def _(pl):
    x_1 = 7
    p = pl.lit(3) < pl.lit(x_1)  # True
    q = pl.lit(x_1) < pl.lit(5)  # False
    pl.select(p & q).item()
    return


@app.cell
def _(pl):
    (
        pl.DataFrame(
            {"p": [True, True, False, False], "q": [True, False, True, False]}
        ).with_columns(
            (pl.col("p") & pl.col("q")).alias("p & q"),
            (pl.col("p") | pl.col("q")).alias("p | q"),
            (~pl.col("p")).alias("~p"),
            (pl.col("p") ^ pl.col("q")).alias("p ^ q"),
            (~(pl.col("p") & pl.col("q"))).alias("p ↑ q"),  
            ((pl.col("p").or_(pl.col("q"))).not_()).alias("p ↓ q"),  
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bitwise Operations
    """)
    return


@app.cell
def _(pl):
    pl.select(pl.lit(10) | pl.lit(34)).item()
    return


@app.cell
def _(pl):
    bits = pl.DataFrame(
        {"x": [1, 1, 0, 0, 7, 10], "y": [1, 0, 1, 0, 2, 34]},
        schema={"x": pl.UInt8, "y": pl.UInt8},
    ).with_columns(  
        (pl.col("x") & pl.col("y")).alias("x & y"),
        (pl.col("x") | pl.col("y")).alias("x | y"),
        (~pl.col("x")).alias("~x"),
        (pl.col("x") ^ pl.col("y")).alias("x ^ y"),
    )
    bits
    return (bits,)


@app.cell
def _(bits, pl):
    bits.select(pl.all().map_elements("{0:08b}".format, return_dtype=pl.String))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Using Functions
    """)
    return


@app.cell
def _(pl):
    scientists = pl.DataFrame(
        {
            "first_name": ["George", "Grace", "John", "Kurt", "Ada"],
            "last_name": ["Boole", "Hopper", "Tukey", "Gödel", "Lovelace"],
            "country": [
                "England",
                "United States",
                "United States",
                "Austria-Hungary",
                "England",
            ],
        }
    )
    scientists
    return (scientists,)


@app.cell
def _(pl, scientists):
    scientists.select(
        concat_list=pl.concat_list(pl.col("^*_name$")),
        struct=pl.struct(pl.all()),
    )
    return


@app.cell
def _(pl, scientists):
    scientists.select(
        concat_str=pl.concat_str(pl.all(), separator=" "),
        format=pl.format("{}, {} from {}", "last_name", "first_name", "country"),
    )
    return


@app.cell
def _(pl):
    prefs = pl.DataFrame(
        {
            "id": [1, 7, 42, 101, 999],
            "has_pet": [True, False, True, False, True],
            "likes_travel": [False, False, False, False, True],
            "likes_movies": [True, False, True, False, True],
            "likes_books": [False, False, True, True, True],
        }
    ).with_columns(
        all=pl.all_horizontal(pl.exclude("id")),
        any=pl.any_horizontal(pl.exclude("id")),
    )

    prefs
    return (prefs,)


@app.cell
def _(pl, prefs):
    prefs.select(
        sum=pl.sum_horizontal(pl.all()),
        max=pl.max_horizontal(pl.all()),
        min=pl.min_horizontal(pl.all()),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### When, Then, Otherwise
    """)
    return


@app.cell
def _(pl, prefs):
    prefs.select(
        pl.col("id"),
        likes_what=pl.when(pl.all_horizontal(pl.col("^likes_.*$")))
        .then(pl.lit("Likes everything"))
        .when(pl.any_horizontal(pl.col("^likes_.*$")))
        .then(pl.lit("Likes something"))
        .otherwise(pl.lit("Likes nothing")),
    )
    return


@app.cell
def _(pl):
    orders = pl.DataFrame(
        {
            "order_amount": [500, 750, 1200, 800, 1100],
            "status": [
                "Approved",
                "Processing",
                "Processing",
                "Declined",
                "Processing",
            ],
        }
    )
    orders.with_columns(
        status=pl.when(pl.col("order_amount") > 1000).then(pl.lit("Flagged"))
    )
    return (orders,)


@app.cell
def _(orders, pl):
    orders.with_columns(
        status=pl.when(pl.col("order_amount") > 1000)
        .then(pl.lit("Flagged"))
        .otherwise(pl.col("status"))
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
