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
    # Chapter 12: Working with Textual, Temporal, and Nested Data Types
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
    ## String
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### String Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### String methods for conversion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### String methods for describing and querying
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### String methods for manipulation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### String Examples
    """)
    return


@app.cell
def _(pl):
    corpus = pl.DataFrame(
        {
            "raw_text": [
                "  Data Science is amazing ",
                "Data_analysis > Data entry",
                " Python&Polars; Fast",
            ]
        }
    )

    corpus
    return (corpus,)


@app.cell
def _(corpus, pl):
    corpus_1 = corpus.with_columns(processed_text=pl.col('raw_text').str.strip_chars().str.to_lowercase().str.replace_all('_', ' '))
    corpus_1
    return (corpus_1,)


@app.cell
def _(corpus_1, pl):
    corpus_1.with_columns(first_5_chars=pl.col('processed_text').str.slice(0, 5), first_word=pl.col('processed_text').str.split(' ').list.get(0), second_word=pl.col('processed_text').str.split(' ').list.get(1))
    return


@app.cell
def _(corpus_1, pl):
    corpus_1.with_columns(len_chars=pl.col('processed_text').str.len_chars(), len_bytes=pl.col('processed_text').str.len_bytes(), count_a=pl.col('processed_text').str.count_matches('a'))
    return


@app.cell
def _(pl):
    posts = pl.DataFrame(
        {"post": ["Loving #python and #polars!", "A boomer post without a hashtag"]}
    )

    hashtag_regex = r"#(\w+)"  

    posts.with_columns(
        hashtags=pl.col("post").str.extract_all(hashtag_regex)  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Categorical
    """)
    return


@app.cell
def _(pl):
    cats = pl.DataFrame(
        {"name": ["Persian cat", "Siamese Cat", "Lynx", "Lynx"]},
        schema={"name": pl.Categorical},
    )

    cats.with_columns(name_physical=pl.col("name").to_physical())
    return (cats,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Categorical Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Categorical Examples
    """)
    return


@app.cell
def _(pl):
    more_cats = pl.DataFrame(
        {"name": ["Maine Coon Cat", "Lynx", "Lynx", "Siamese Cat"]},
        schema={"name": pl.Categorical},
    )

    more_cats.with_columns(name_physical=pl.col("name").to_physical())
    return (more_cats,)


@app.cell
def _(cats, more_cats):
    cats.join(more_cats, on="name")
    return


@app.cell
def _(pl):
    with pl.StringCache():
        left = pl.DataFrame(
            {
                "categorical_column": ["value3", "value2", "value1"],
                "other": ["a", "b", "c"],
            },
            schema={"categorical_column": pl.Categorical, "other": pl.String},
        )
        right = pl.DataFrame(
            {
                "categorical_column": ["value2", "value3", "value4"],
                "other": ["d", "e", "f"],
            },
            schema={"categorical_column": pl.Categorical, "other": pl.String},
        )
    return left, right


@app.cell
def _(left, right):
    left.join(right, on="categorical_column")
    return


@app.cell
def _(pl):
    pl.enable_string_cache()
    return


@app.cell
def _(pl, right):
    right.select(pl.col("categorical_column").cat.get_categories())
    return


@app.cell
def _(cats, pl):
    sorting_comparison_df = cats.select(cat_lexical=pl.col("name")).with_columns(
        cat_physical=pl.col("cat_lexical").to_physical()
    )

    sorting_comparison_df
    return (sorting_comparison_df,)


@app.cell
def _():
    # sorting_comparison_df.with_columns(
    #     pl.col("cat_lexical").cast(pl.Categorical("physical"))
    # ).sort(by="cat_lexical")

    # A Categorical with physical ordering has been deprecated in the meanwhile. Sorting is now always lexical.
    return


@app.cell
def _(pl, sorting_comparison_df):
    sorting_comparison_df.with_columns(
        pl.col("cat_lexical").cast(pl.Categorical("lexical"))
    ).sort(by="cat_lexical")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Enum
    """)
    return


@app.cell
def _(pl):
    bear_enum_dtype = pl.Enum(["Polar", "Panda", "Brown"])

    bear_enum_series = pl.Series(
        ["Polar", "Panda", "Brown", "Brown", "Polar"], dtype=bear_enum_dtype
    )

    bear_cat_series = pl.Series(
        ["Polar", "Panda", "Brown", "Brown", "Polar"], dtype=pl.Categorical
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Temporal
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Temporal Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Temporal methods for conversion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Temporal methods for describing and querying
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Temporal methods for manipulation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Temporal Examples
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Loading from a CSV file
    """)
    return


@app.cell
def _(pl):
    pl.read_csv("data/all_stocks.csv", try_parse_dates=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Converting to and from a String
    """)
    return


@app.cell
def _(pl):
    dates = pl.DataFrame({"date_str": ["2023-12-31", "2024-02-29"]}).with_columns(
        date=pl.col("date_str").str.to_date("%Y-%m-%d")
    )

    dates
    return (dates,)


@app.cell
def _(dates, pl):
    dates.with_columns(formatted_date=pl.col("date").dt.to_string("%d-%m-%Y"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Generating date ranges
    """)
    return


@app.cell
def _(pl):
    pl.DataFrame(
        {
            "monday": pl.date_range(
                start=pl.date(2024, 10, 28),
                end=pl.date(2024, 12, 1),
                interval="1w",  
                eager=True,  
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Time zones
    """)
    return


@app.cell
def _(pl):
    pl.DataFrame(  
        {
            "utc_mixed_offset": [
                "2021-03-27T00:00:00+0100",
                "2021-03-28T00:00:00+0100",
                "2021-03-29T00:00:00+0200",
                "2021-03-30T00:00:00+0200",
            ]
        }
    ).with_columns(
        parsed=pl.col("utc_mixed_offset").str.to_datetime(
            "%Y-%m-%dT%H:%M:%S%z"
        )  
    ).with_columns(
        converted=pl.col("parsed").dt.convert_time_zone("Europe/Amsterdam")  
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## List
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List Examples
    """)
    return


@app.cell
def _(pl):
    bools = pl.DataFrame({"values": [[True, True], [False, False, True], [False]]})

    bools.with_columns(
        all_true=pl.col("values").list.all(),
        any_true=pl.col("values").list.any(),
    )
    return


@app.cell
def _(pl):
    groups = pl.DataFrame({"ages": [[18, 21], [30, 40, 50], [42, 69]]})

    groups.with_columns(
        over_forty=pl.col("ages").list.eval(
            pl.element() > 40,  
            parallel=True,  
        )
    ).with_columns(  
        all_over_forty=pl.col("over_forty").list.all()  
    )
    return (groups,)


@app.cell
def _(groups, pl):
    groups.with_columns(
        ages_sorted_descending=pl.col("ages").list.sort(descending=True)
    )
    return


@app.cell
def _(groups):
    groups.explode("ages")
    return


@app.cell
def _(groups, pl):
    groups.select(ages=pl.col("ages").list.explode())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Array
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Array Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Array Examples
    """)
    return


@app.cell
def _(pl):
    events = pl.DataFrame(
        [
            pl.Series(
                "location", ["Paris", "Amsterdam", "Barcelona"], dtype=pl.String
            ),
            pl.Series(
                "temperatures",
                [
                    [23, 27, 21, 22, 24, 23, 22],
                    [17, 19, 15, 22, 18, 20, 21],
                    [30, 32, 28, 29, 34, 33, 31],
                ],
                dtype=pl.Array(pl.Int64, shape=7),
            ),
        ]
    )

    events
    return (events,)


@app.cell
def _(events, pl):
    events.with_columns(
        median=pl.col("temperatures").arr.median(),
        max=pl.col("temperatures").arr.max(),
        warmest_dow=pl.col("temperatures").arr.arg_max(),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Struct
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Struct Methods
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Struct Examples
    """)
    return


@app.cell
def _(pl):
    from datetime import date

    orders = pl.DataFrame(
        {
            "customer_id": [2781, 6139, 5392],
            "order_details": [
                {"amount": 250.00, "date": date(2024, 1, 3), "items": 5},
                {"amount": 150.00, "date": date(2024, 1, 5), "items": 1},
                {"amount": 100.00, "date": date(2024, 1, 2), "items": 3},
            ],
        },
    )

    orders
    return (orders,)


@app.cell
def _(orders, pl):
    orders.select(pl.col("order_details").struct.field("amount"))
    return


@app.cell
def _(orders):
    order_details_df = orders.unnest("order_details")

    order_details_df
    return (order_details_df,)


@app.cell
def _(order_details_df, pl):
    order_details_df.select(
        "amount",
        "date",
        "items",
        order_details=pl.struct(pl.col("amount"), pl.col("date"), pl.col("items")),
    )
    return


@app.cell
def _(pl):
    basket = pl.DataFrame(
        {
            "fruit": ["cherry", "apple", "banana", "banana", "apple", "banana"],
        }
    )

    basket
    return (basket,)


@app.cell
def _(basket, pl):
    basket.select(pl.col("fruit").value_counts(sort=True))
    return


@app.cell
def _(basket, pl):
    basket.select(pl.col("fruit").value_counts(sort=True).struct.unnest())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
