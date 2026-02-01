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
    # Chapter 10: Selecting and Creating Columns
    """)
    return


@app.cell
def _():
    import polars as pl
    pl.__version__  # The book is built with Polars version 1.20.0
    return (pl,)


@app.cell
def _(pl):
    starwars = pl.read_parquet("data/starwars.parquet")
    rebels = starwars.drop("films").filter(
        pl.col("name").is_in(["Luke Skywalker", "Leia Organa", "Han Solo"])
    )

    print(rebels[:, :6])  
    print(rebels[:, 6:11])
    print(rebels[:, 11:])
    return rebels, starwars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Selecting Columns
    """)
    return


@app.cell
def _(pl, rebels):
    rebels.select(
        "name",
        pl.col("homeworld"),
        pl.col("^.*_color$"),
        (pl.col("height") / 100).alias("height_m"),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Introducing Selectors
    """)
    return


@app.cell
def _():
    import polars.selectors as cs
    return (cs,)


@app.cell
def _(cs, rebels):
    rebels.select(
        "name",
        cs.by_name("homeworld"),
        cs.by_name("^.*_color$"),
        (cs.by_name("height") / 100).alias("height_m"),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Selecting Based on Name
    """)
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.starts_with("birth_"))
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.ends_with("_color"))
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.contains("_"))
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.matches("^[a-z]{4}$"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Selecting Based on Data Type
    """)
    return


@app.cell
def _(cs, rebels):
    rebels.group_by("hair_color").agg(cs.numeric().mean())
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.string())
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.temporal())
    return


@app.cell
def _(cs, pl, rebels):
    rebels.select(cs.by_dtype(pl.List(pl.String)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Selecting Based on Position
    """)
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.by_index(range(0, 999, 3), require_all=False))
    return


@app.cell
def _(cs, rebels):
    rebels.select("name", cs.by_index(range(-2, 0)))
    return


@app.cell
def _():
    # This raises a ColumnNotFoundError:
    # rebels.select(cs.by_index(20))
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.by_index(range(20, 22), require_all=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Combining Selectors
    """)
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.by_name("hair_color") | cs.numeric())
    return


@app.cell
def _(cs, pl):
    df = pl.DataFrame({"d": 1, "i": True, "s": True, "c": True, "o": 1.0})

    print(df)

    x = cs.by_name("d", "i", "s")
    y = cs.boolean()

    print("\nselector => columns")

    for s in ["x", "y", "x | y", "x & y", "x - y", "x ^ y", "~x", "x - x"]:
        print(f"{s:8} => {cs.expand_selector(df, eval(s))}")
    return df, x


@app.cell
def _(df, x):
    df.select(x - x)
    return


@app.cell
def _(cs, df):
    print(df.select((_first := cs.by_name('c', 'i')), ~_first))
    print(f'first: {_first}, ~first: {~_first}')
    return


@app.cell
def _(cs, df):
    print(df.select((_first := cs.last()), ~_first))
    print(f'first: {_first}, ~first: {~_first}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating Columns
    """)
    return


@app.cell
def _(pl, rebels):
    rebels.with_columns(bmi=pl.col("mass") / ((pl.col("height") / 100) ** 2))
    return


@app.cell
def _(pl):
    df_1 = pl.DataFrame({'a': [1, 2, 3]})
    df_1.with_columns(pl.col('a') * 2)
    return (df_1,)


@app.cell
def _(df_1, pl):
    df_1.with_columns(a2=pl.col('a') * 2)
    return


@app.cell
def _(pl, rebels):
    rebels.with_columns(
        bmi=pl.col("mass") / ((pl.col("height") / 100) ** 2),
        age_destroy=(
            (pl.date(1983, 5, 25) - pl.col("birth_date")).dt.total_days() / 365
        ).cast(pl.UInt8),
    )
    return


@app.cell
def _():
    # This raises a ColumnNotFoundError:
    # rebels.with_columns(
    #     bmi=pl.col("mass") / ((pl.col("height") / 100) ** 2),
    #     bmi_cat=pl.col("bmi").cut(
    #         [18.5, 25], labels=["Underweight", "Normal", "Overweight"]
    #     ),
    # )
    return


@app.cell
def _(pl, rebels):
    (
        rebels.with_columns(
            bmi=pl.col("mass") / ((pl.col("height") / 100) ** 2)
        ).with_columns(
            bmi_cat=pl.col("bmi").cut(
                [18.5, 25], labels=["Underweight", "Normal", "Overweight"]
            )
        )
    )
    return


@app.cell
def _():
    # This raises a SyntaxError:
    # starwars.select(
    #     "name",
    #     bmi=(pl.col("mass") / ((pl.col("height") / 100) ** 2)),
    #     "species",
    # )
    return


@app.cell
def _(pl, starwars):
    (
        starwars.select(
            "name",
            (pl.col("mass") / ((pl.col("height") / 100) ** 2)).alias("bmi"),  
            "species",
        )
        .drop_nulls()
        .top_k(5, by="bmi")  
    )
    return


@app.cell
def _(df_1, pl):
    df_1.with_columns(pl.lit(1).alias('ones'))
    return


@app.cell
def _(df_1, pl):
    df_1.select(pl.all(), pl.lit(1).alias('ones'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Related Column Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dropping
    """)
    return


@app.cell
def _(rebels):
    rebels.drop("name", "screen_time", strict=False)
    return


@app.cell
def _(cs, rebels):
    rebels.select(~cs.by_name("name", "screen_time"))
    return


@app.cell
def _(cs, rebels):
    rebels.select(cs.exclude("name", "screen_time"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Renaming
    """)
    return


@app.cell
def _(rebels):
    (
        rebels.rename({"homeworld": "planet", "mass": "weight"})
        .rename(lambda s: s.removesuffix("_color"))
        .select("name", "planet", "weight", "hair", "skin", "eye")  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Stacking
    """)
    return


@app.cell
def _(cs, pl, rebels):
    rebel_names = rebels.select("name")
    rebel_colors = rebels.select(cs.ends_with("_color"))
    rebel_quotes = pl.Series(
        "quote",
        [
            "You know, sometimes I amaze myself.",
            "That doesn't sound too hard.",
            "I have a bad feeling about this.",
        ],
    )

    (rebel_names.hstack(rebel_colors).hstack([rebel_quotes]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Adding Row Indices
    """)
    return


@app.cell
def _(rebels):
    rebels.with_row_index(name="rebel_id", offset=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
