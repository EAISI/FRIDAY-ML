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
    # Chapter 8: Continuing Expressions
    """)
    return


@app.cell
def _():
    import polars as pl
    pl.__version__  # The book is built with Polars version 1.20.0
    return (pl,)


@app.cell
def _():
    import math
    import numpy as np

    print(f"{math.pi=}")
    rng = np.random.default_rng(1729)
    print(f"{rng.random()=}")
    return math, np, rng


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Types of Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example A: Element-Wise Operations
    """)
    return


@app.cell
def _(pl):
    penguins = pl.read_csv("data/penguins.csv", null_values="NA").select(
        "species",
        "island",
        "sex",
        "year",
        mass=pl.col("body_mass_g") / 1000,
    )
    penguins.with_columns(
        mass_sqrt=pl.col("mass").sqrt(),  
        mass_exp=pl.col("mass").exp(),
    )
    return (penguins,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example B: Operations That Summarize to One
    """)
    return


@app.cell
def _(penguins, pl):
    penguins.select(pl.col("mass").mean(), pl.col("island").first())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example C: Operations That Summarize to One or More
    """)
    return


@app.cell
def _(penguins, pl):
    penguins.select(pl.col("island").unique())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example D: Operations That Extend
    """)
    return


@app.cell
def _(penguins, pl):
    penguins.select(
        pl.col("species")
        .unique()  
        .repeat_by(3000)  
        .explode()  
        .extend_constant("Saiyan", n=1)  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Element-Wise Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Perform Mathematical Transformations
    """)
    return


@app.cell
def _(math, pl):
    (
        pl.DataFrame({"x": [-2.0, 0.0, 0.5, 1.0, math.e, 1000.0]}).with_columns(
            abs=pl.col("x").abs(),
            exp=pl.col("x").exp(),
            log2=pl.col("x").log(2),  
            log10=pl.col("x").log10(),
            log1p=pl.col("x").log1p(),
            sign=pl.col("x").sign(),
            sqrt=pl.col("x").sqrt(),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations Related to Trigonometry
    """)
    return


@app.cell
def _(math, pl):
    (
        pl.DataFrame(
            {"x": [-math.pi, 0.0, 1.0, math.pi, 2 * math.pi, 90.0, 180.0, 360.0]}
        ).with_columns(
            arccos=pl.col("x").arccos(),  
            cos=pl.col("x").cos(),
            degrees=pl.col("x").degrees(),
            radians=pl.col("x").radians(),
            sin=pl.col("x").sin(),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Round and Categorize
    """)
    return


@app.cell
def _(math, pl):
    (
        pl.DataFrame(
            {"x": [-6.0, -0.5, 0.0, 0.5, math.pi, 9.9, 9.99, 9.999]}
        ).with_columns(
            ceil=pl.col("x").ceil(),
            clip=pl.col("x").clip(-1, 1),
            cut=pl.col("x").cut([-1, 1], labels=["bad", "neutral", "good"]),  
            floor=pl.col("x").floor(),
            qcut=pl.col("x").qcut([0.5], labels=["below median", "above median"]),
            round2=pl.col("x").round(2),
            round0=pl.col("x").round(0),  
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations for Missing or Infinite Values
    """)
    return


@app.cell
def _(math, pl):
    x = [42.0, math.nan, None, math.inf, -math.inf]
    (
        pl.DataFrame({"x": x}).with_columns(
            fill_nan=pl.col("x").fill_nan(999),
            fill_null=pl.col("x").fill_null(0),  
            is_finite=pl.col("x").is_finite(),
            is_infinite=pl.col("x").is_infinite(),
            is_nan=pl.col("x").is_nan(),
            is_null=pl.col("x").is_null(),
        )
    )
    return (x,)


@app.cell
def _(pl, x):
    (
        pl.DataFrame({"x": x}).with_columns(
            fill_both=pl.col("x").fill_nan(0).fill_null(0),
            is_either=(pl.col("x").is_nan() | pl.col("x").is_null()),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Operations
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"x": ["here", "there", "their", "they're"]}).with_columns(
            hash=pl.col("x").hash(seed=1337),  
            repeat_by=pl.col("x").repeat_by(3),
            replace=pl.col("x").replace(
                {
                    "here": "there",
                    "they're": "they are",
                }
            ),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Nonreducing Series-Wise Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Accumulate
    """)
    return


@app.cell
def _(np, pl):
    (
        pl.DataFrame(
            {"x": [0.0, 1.0, 2.0, None, 2.0, np.nan, -1.0, 2.0]}
        ).with_columns(
            cum_count=pl.col("x").cum_count(),  
            cum_max=pl.col("x").cum_max(),
            cum_min=pl.col("x").cum_min(),
            cum_prod=pl.col("x").cum_prod(reverse=True),  
            cum_sum=pl.col("x").cum_sum(),
            diff=pl.col("x").diff(),
            pct_change=pl.col("x").pct_change(),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Fill and Shift
    """)
    return


@app.cell
def _(math, pl):
    (
        pl.DataFrame(
            {"x": [-1.0, 0.0, 1.0, None, None, 3.0, 4.0, math.nan, 6.0]}
        ).with_columns(
            backward_fill=pl.col("x").backward_fill(),  
            forward_fill=pl.col("x").forward_fill(limit=1),
            interp1=pl.col("x").interpolate(method="linear"),  
            interp2=pl.col("x").interpolate(method="nearest"),
            shift1=pl.col("x").shift(1),
            shift2=pl.col("x").shift(-2),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations Related to Duplicate Values
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"x": ["A", "C", "D", "C"]}).with_columns(  
            is_duplicated=pl.col("x").is_duplicated(),
            is_first_distinct=pl.col("x").is_first_distinct(),
            is_last_distinct=pl.col("x").is_last_distinct(),
            is_unique=pl.col("x").is_unique(),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Compute Rolling Statistics
    """)
    return


@app.cell
def _(pl):
    stock = (
        pl.read_csv("data/stock/nvda/2023.csv", try_parse_dates=True)
        .select("date", "close")
        .with_columns(
            ewm_mean=pl.col("close").ewm_mean(com=7, ignore_nulls=True),  
            rolling_mean=pl.col("close").rolling_mean(window_size=7),
            rolling_min=pl.col("close").rolling_min(window_size=7),
        )
    )

    stock
    return (stock,)


@app.cell
def _(stock, theme_tufte):
    from plotnine import ggplot, aes, geom_point, geom_line, geom_bar, geom_histogram, facet_wrap, labs, theme_minimal, theme, element_text

    (
        ggplot(stock.unpivot(index="date"), aes("date", "value", color="variable"))
        + geom_line(size=1)
        + labs(x="Date", y="Value", color="Method")
        + theme_tufte(base_size=14)
        + theme(figure_size=(8, 5), dpi=200)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Sort
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame(
            {
                "x": [1, 3, None, 3, 7],
                "y": ["D", "I", "S", "C", "O"],
            }
        ).with_columns(
            arg_sort=pl.col("x").arg_sort(),
            shuffle=pl.col("x").shuffle(seed=7),
            sort=pl.col("x").sort(nulls_last=True),
            sort_by=pl.col("x").sort_by("y"),
            reverse=pl.col("x").reverse(),
            rank=pl.col("x").rank(),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Operations
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"x": [33, 33, 27, 33, 60, 60, 60, 33, 60]}).with_columns(
            rle_id=pl.col("x").rle_id(),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Series-Wise Operations That Summarize to One
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"x": [1, 3, 3, 7]}).with_columns(
            mean=pl.col("x").mean(),
        )
    )
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"cluster": ["a", "a", "b", "b"], "x": [1, 3, 3, 7]})
        .group_by("cluster")
        .agg(
            mean=pl.col("x").mean(),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Are Quantifiers
    """)
    return


@app.cell
def _(pl):
    df = pl.DataFrame(
        {
            "x": [True, False, False],
            "y": [True, True, True],
            "z": [False, False, False],
        }
    )
    print(df)
    print(
        df.select(
            pl.all().all().name.suffix("_all"),
            pl.all().any().name.suffix("_any"),
        ),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Compute Statistics
    """)
    return


@app.cell
def _(pl, rng):
    _samples = rng.normal(loc=5, scale=3, size=1000000)
    pl.DataFrame({'x': _samples}).select(max=pl.col('x').max(), mean=pl.col('x').mean(), quantile=pl.col('x').quantile(quantile=0.95), skew=pl.col('x').skew(), std=pl.col('x').std(), sum=pl.col('x').sum(), var=pl.col('x').var())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Count
    """)
    return


@app.cell
def _(pl, rng):
    _samples = pl.Series(rng.integers(low=0, high=10000, size=1729))
    _samples[403] = None
    df_ints = pl.DataFrame({'x': _samples}).with_row_index()
    df_ints.slice(400, 6)
    return (df_ints,)


@app.cell
def _(df_ints, pl):
    df_ints.select(
        approx_n_unique=pl.col("x").approx_n_unique(),
        count=pl.col("x").count(),
        len=pl.col("x").len(),
        n_unique=pl.col("x").n_unique(),
        null_count=pl.col("x").null_count(),
    )
    return


@app.cell
def _(pl, rng):
    large_df_ints = pl.DataFrame(
        {"x": rng.integers(low=0, high=10_000, size=10_000_000)}
    )
    return (large_df_ints,)


@app.cell
def _(large_df_ints, pl):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    large_df_ints.select(pl.col("x").n_unique())
    return


@app.cell
def _(large_df_ints, pl):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    large_df_ints.select(pl.col("x").approx_n_unique())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Operations
    """)
    return


@app.cell
def _(df_ints, pl):
    df_ints.select(
        arg_min=pl.col("x").arg_min(),
        first=pl.col("x").first(),
        get=pl.col("x").get(403),  
        implode=pl.col("x").implode(),
        last=pl.col("x").last(),
        upper_bound=pl.col("x").upper_bound(),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Series-Wise Operations That Summarize to One or More
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations Related to Unique Values
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame({"x": ["A", "C", "D", "C"]}).select(
            arg_unique=pl.col("x").arg_unique(),
            unique=pl.col("x").unique(maintain_order=True),  
            unique_counts=pl.col("x").unique_counts(),
            value_counts=pl.col("x").value_counts(sort=True),  
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Select
    """)
    return


@app.cell
def _(df_ints, pl):
    df_ints.select(
        bottom_k=pl.col("x").bottom_k(7),  
        head=pl.col("x").head(7),
        sample=pl.col("x").sample(7),
        slice=pl.col("x").slice(400, 7),
        gather=pl.col("x").gather([1, 1, 2, 3, 5, 8, 13]),
        gather_every=pl.col("x").gather_every(247),  
        top_k=pl.col("x").top_k(7),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operations That Drop Missing Values
    """)
    return


@app.cell
def _(np, pl):
    x_1 = [None, 1.0, 2.0, 3.0, np.nan]
    pl.DataFrame({'x': x_1}).select(drop_nans=pl.col('x').drop_nans(), drop_nulls=pl.col('x').drop_nulls())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Operations
    """)
    return


@app.cell
def _(pl):
    numbers = [33, 33, 27, 33, 60, 60, 60, 33, 60]

    (
        pl.DataFrame({"x": numbers}).select(
            arg_true=(pl.col("x") >= 60).arg_true(),  
        )
    )
    return (numbers,)


@app.cell
def _(numbers, pl):
    (
        pl.DataFrame({"x": numbers}).select(
            mode=pl.col("x").mode().sort(),
        )
    )
    return


@app.cell
def _(numbers, pl):
    (
        pl.DataFrame({"x": numbers}).select(
            reshape=pl.col("x").reshape((3, 3)),  
        )
    )
    return


@app.cell
def _(numbers, pl):
    (
        pl.DataFrame({"x": numbers}).select(
            rle=pl.col("x").rle(),  
        )
    )
    return


@app.cell
def _(numbers, pl):
    (
        pl.DataFrame({"x": numbers}).select(
            rle=pl.col("x").sort().search_sorted(42),  
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Series-Wise Operations That Extend
    """)
    return


@app.cell
def _(pl):
    (
        pl.DataFrame(
            {
                "x": [["a", "b"], ["c", "d"]],
            }
        ).select(explode=pl.col("x").explode())
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
