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
    # Chapter 14: Joining and Concatenating
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
    ## Joining
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Join Strategies
    """)
    return


@app.cell
def _(pl):
    df_left = pl.DataFrame({"key": ["A", "B", "C", "D"], "value": [1, 2, 3, 4]})

    df_right = pl.DataFrame({"key": ["B", "C", "D", "E"], "value": [5, 6, 7, 8]})
    return df_left, df_right


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Inner
    """)
    return


@app.cell
def _(df_left, df_right):
    df_left.join(df_right, on="key", how="inner")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Full
    """)
    return


@app.cell
def _(df_left, df_right):
    df_left.join(df_right, on="key", how="full", suffix="_other")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Left
    """)
    return


@app.cell
def _(df_left, df_right):
    df_left.join(df_right, on="key", how="left")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Right
    """)
    return


@app.cell
def _(df_left, df_right):
    df_left.join(df_right, on="key", how="right")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Cross
    """)
    return


@app.cell
def _(df_left, df_right):
    df_left.join(df_right, how="cross")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Semi
    """)
    return


@app.cell
def _(df_left, df_right):
    df_left.join(df_right, on="key", how="semi")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Anti
    """)
    return


@app.cell
def _(df_left, df_right):
    df_left.join(df_right, on="key", how="anti")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Joining on Multiple Columns
    """)
    return


@app.cell
def _(pl):
    residences_left = pl.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "Dave"],
            "city": ["NY", "LA", "NY", "SF"],
            "age": [25, 30, 35, 40],
        }
    )

    departments_right = pl.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "Dave"],
            "city": ["NY", "LA", "NY", "Chicago"],
            "department": ["Finance", "Marketing", "Engineering", "Operations"],
        }
    )

    residences_left.join(departments_right, on=["name", "city"], how="inner")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Validation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Many-to-many
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### One-to-many
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Many-to-one
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### One-to-one
    """)
    return


@app.cell
def _(pl):
    employees = pl.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Charlie", "Dave"],
            "department_id": [10, 10, 30, 10],
        }
    )

    departments = pl.DataFrame(
        {
            "department_id": [10, 20, 30],
            "department_name": [
                "Information Technology",
                "Finance",
                "Human Resources",
            ],
        }
    )

    employees.join(departments, on="department_id", how="left", validate="m:1")
    return


@app.cell
def _():
    # This raises a ComputeError:
    # departments = pl.DataFrame(
    #     {
    #         "department_id": [10, 20, 10],
    #         "department_name": [
    #             "Information Technology",
    #             "Finance",
    #             "Human Resources",
    #         ],
    #     }
    # )

    # employees.join(
    #     departments, on="department_id", how="left", validate="m:1"
    # )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inexact Joining
    """)
    return


@app.cell
def _(pl):
    df_left_1 = pl.DataFrame({'int_id': [10, 5], 'value': ['b', 'a']})
    df_right_1 = pl.DataFrame({'int_id': [4, 7, 12], 'value': [1, 2, 3]})
    return df_left_1, df_right_1


@app.cell
def _():
    # This raises an InvalidOperationError:
    # df_left.join_asof(df_right, on="int_id", tolerance=3)
    return


@app.cell
def _(df_left_1, df_right_1):
    df_left_2 = df_left_1.sort('int_id')
    df_right_2 = df_right_1
    df_left_2.join_asof(df_right_2, on='int_id')
    return df_left_2, df_right_2


@app.cell
def _(df_left_2, df_right_2):
    df_left_2.join_asof(df_right_2, on='int_id', coalesce=False)
    return


@app.cell
def _(df_left_2, df_right_2):
    df_left_2.join_asof(df_right_2.rename({'int_id': 'int_id_right'}), left_on='int_id', right_on='int_id_right')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Inexact Join Strategies
    """)
    return


@app.cell
def _(df_left_2, df_right_2):
    print(df_left_2)
    print(df_right_2)
    return


@app.cell
def _(df_left_2, df_right_2):
    df_left_2.join_asof(df_right_2, on='int_id', tolerance=3, strategy='backward')
    return


@app.cell
def _(df_left_2, df_right_2):
    df_left_2.join_asof(df_right_2, on='int_id', tolerance=3, strategy='forward')
    return


@app.cell
def _(df_left_2, df_right_2):
    df_left_2.join_asof(df_right_2, on='int_id', tolerance=3, strategy='nearest')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Additional Fine-Tuning
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Use Case: Marketing Campaign Attribution
    """)
    return


@app.cell
def _(pl):
    campaigns = pl.scan_csv("data/campaigns.csv")
    campaigns.head(1).collect()
    return (campaigns,)


@app.cell
def _(campaigns, pl):
    campaigns.select(pl.col("Product Type").unique()).collect()
    return


@app.cell
def _(pl):
    transactions = pl.scan_csv("data/transactions.csv")
    transactions.head(1).collect()
    return (transactions,)


@app.cell
def _(campaigns, pl, transactions):
    transactions_1 = transactions.with_columns(pl.col('Sale Date').str.to_datetime('%Y-%m-%d %H:%M:%S%.f').cast(pl.Datetime('us')))
    campaigns_1 = campaigns.with_columns(pl.col('Campaign Date').str.to_datetime('%Y-%m-%d %H:%M:%S'))
    sales_with_campaign_df = transactions_1.sort('Sale Date').join_asof(campaigns_1.sort('Campaign Date'), left_on='Sale Date', right_on='Campaign Date', by='Product Type', strategy='backward', tolerance='60d', check_sortedness=False).collect()
    sales_with_campaign_df
    return campaigns_1, sales_with_campaign_df, transactions_1


@app.cell
def _(pl, sales_with_campaign_df):
    (
        sales_with_campaign_df.group_by("Product Type", "Campaign Name")
        .agg(pl.col("Quantity").mean())
        .sort("Product Type", "Campaign Name")
    )
    return


@app.cell
def _(campaigns_1, pl):
    campaigns_1.filter(pl.col('Product Type') == 'Books').collect()
    return


@app.cell
def _(pl, transactions_1):
    transactions_1.filter((pl.col('Product Type') == 'Books') & (pl.col('Sale Date') > pl.lit('2023-12-31 21:00:00').str.to_datetime())).collect()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vertical and Horizontal Concatenation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vertical
    """)
    return


@app.cell
def _(pl):
    df1 = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "value": ["a", "b", "c"],
        }
    )
    df2 = pl.DataFrame(
        {
            "id": [4, 5],
            "value": ["d", "e"],
        }
    )
    pl.concat([df1, df2], how="vertical")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Horizontal
    """)
    return


@app.cell
def _(pl):
    df1_1 = pl.DataFrame({'id': [1, 2, 3], 'value': ['a', 'b', 'c']})
    df2_1 = pl.DataFrame({'value2': ['x', 'y']})
    pl.concat([df1_1, df2_1], how='horizontal')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Diagonal
    """)
    return


@app.cell
def _(pl):
    df1_2 = pl.DataFrame({'id': [1, 2, 3], 'value': ['a', 'b', 'c']})
    df2_2 = pl.DataFrame({'value': ['d', 'e'], 'value2': ['x', 'y']})
    pl.concat([df1_2, df2_2], how='diagonal')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Align
    """)
    return


@app.cell
def _(pl):
    df1_3 = pl.DataFrame({'id': [1, 2, 3], 'value': ['a', 'b', 'c']})
    df2_3 = pl.DataFrame({'value': ['a', 'c', 'd'], 'value2': ['x', 'y', 'z']})
    pl.concat([df1_3, df2_3], how='align')
    return


@app.cell
def _(pl):
    df1_4 = pl.DataFrame({'id': [1, 2, 2], 'value': ['a', 'c', 'b']})
    df2_4 = pl.DataFrame({'id': [2, 2], 'value': ['x', 'y']})
    pl.align_frames(df1_4, df2_4, on='id')
    return df1_4, df2_4


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Relaxed
    """)
    return


@app.cell
def _():
    # This raises a SchemaError:
    # df1 = pl.DataFrame(
    #     {
    #         "id": [1, 2, 3],
    #         "value": ["a", "b", "c"],
    #     }
    # )
    # df2 = pl.DataFrame(
    #     {
    #         "id": [4.0, 5.0],
    #         "value": [1, 2],
    #     }
    # )
    # pl.concat([df1, df2], how="vertical")
    return


@app.cell
def _(df1_4, df2_4, pl):
    pl.concat([df1_4, df2_4], how='vertical_relaxed')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Stacking
    """)
    return


@app.cell
def _(pl):
    df1_5 = pl.DataFrame({'id': [1, 2], 'value': ['a', 'b']})
    df2_5 = pl.DataFrame({'id': [3, 4], 'value': ['c', 'd']})
    df1_5.vstack(df2_5)
    return


@app.cell
def _(pl):
    df1_6 = pl.DataFrame({'id': [1, 2], 'value': ['a', 'b']})
    df2_6 = pl.DataFrame({'value2': ['x', 'y']})
    df1_6.hstack(df2_6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Appending
    """)
    return


@app.cell
def _(pl):
    series_a = pl.Series("a", [1, 2])
    series_b = pl.Series("b", [3, 4])
    series_a.append(series_b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Extending
    """)
    return


@app.cell
def _(pl):
    df1_7 = pl.DataFrame({'id': [1, 2], 'value': ['a', 'b']})
    df2_7 = pl.DataFrame({'id': [3, 4], 'value': ['c', 'd']})
    df1_7.extend(df2_7)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
