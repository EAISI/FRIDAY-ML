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
    # Chapter 15: Reshaping
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
    ## Wide Versus Long DataFrames
    """)
    return


@app.cell
def _(pl):
    grades_wide = pl.DataFrame(
        {
            "student": ["Jeroen", "Thijs", "Ritchie"],
            "math": [85, 78, 92],
            "science": [90, 82, 85],
            "history": [88, 80, 87],
        }
    )

    grades_wide
    return


@app.cell
def _(pl):
    grades_long = pl.DataFrame(
        {
            "student": [
                "Jeroen",
                "Jeroen",
                "Jeroen",
                "Thijs",
                "Thijs",
                "Thijs",
                "Ritchie",
                "Ritchie",
                "Ritchie",
            ],
            "subject": [
                "Math",
                "Science",
                "History",
                "Math",
                "Science",
                "History",
                "Math",
                "Science",
                "History",
            ],
            "grade": [85, 90, 88, 78, 82, 80, 92, 85, 87],
        }
    )

    grades_long
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pivot to a Wider DataFrame
    """)
    return


@app.cell
def _(pl):
    grades = pl.DataFrame(
        {
            "student": [
                "Jeroen",
                "Jeroen",
                "Jeroen",
                "Thijs",
                "Thijs",
                "Thijs",
                "Ritchie",
                "Ritchie",
                "Ritchie",
            ],
            "subject": [
                "Math",
                "Science",
                "History",
                "Math",
                "Science",
                "History",
                "Math",
                "Science",
                "History",
            ],
            "grade": [85, 90, 88, 78, 82, 80, 92, 85, 87],
        }
    )

    grades
    return (grades,)


@app.cell
def _(grades):
    grades.pivot(index="student", on="subject", values="grade")
    return


@app.cell
def _(pl):
    multiple_grades = pl.DataFrame(
        {
            "student": [
                "Jeroen",
                "Jeroen",
                "Jeroen",
                "Jeroen",
                "Jeroen",
                "Jeroen",
                "Thijs",
                "Thijs",
                "Thijs",
                "Thijs",
                "Thijs",
                "Thijs",
            ],
            "subject": [
                "Math",
                "Math",
                "Math",
                "Science",
                "Science",
                "Science",
                "Math",
                "Math",
                "Math",
                "Science",
                "Science",
                "Science",
            ],
            "grade": [85, 88, 85, 60, 66, 63, 51, 79, 62, 82, 85, 82],
        }
    )

    multiple_grades
    return (multiple_grades,)


@app.cell
def _(multiple_grades):
    multiple_grades.pivot(
        index="student", on="subject", values="grade", aggregate_function="mean"
    )
    return


@app.cell
def _(multiple_grades, pl):
    multiple_grades.pivot(
        index="student",
        on="subject",
        values="grade",
        aggregate_function=pl.element().max() - pl.element().min(),
    )
    return


@app.cell
def _(pl):
    lf = pl.LazyFrame(
        {
            "col1": ["a", "a", "a", "b", "b", "b"],
            "col2": ["x", "x", "x", "x", "y", "y"],
            "col3": [6, 7, 3, 2, 5, 7],
        }
    )

    index = pl.col("col1")
    on = pl.col("col2")
    values = pl.col("col3")
    unique_column_values = ["x", "y"]
    aggregate_function = lambda col: col.tanh().mean()

    lf.group_by(index).agg(
        aggregate_function(values.filter(on == value)).alias(value)
        for value in unique_column_values
    ).collect()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Unpivot to a Longer DataFrame
    """)
    return


@app.cell
def _(pl):
    grades_wide_1 = pl.DataFrame({'student': ['Jeroen', 'Thijs', 'Ritchie'], 'math': [85, 78, 92], 'science': [90, 82, 85], 'history': [88, 80, 87]})
    grades_wide_1
    return (grades_wide_1,)


@app.cell
def _(grades_wide_1):
    grades_wide_1.unpivot(index=['student'], on=['math', 'science', 'history'], variable_name='subject', value_name='grade')
    return


@app.cell
def _(pl):
    df = pl.DataFrame(
        {
            "student": ["Jeroen", "Thijs", "Ritchie", "Jeroen", "Thijs", "Ritchie"],
            "class": [
                "Math101",
                "Math101",
                "Math101",
                "Math102",
                "Math102",
                "Math102",
            ],
            "age": [20, 21, 22, 20, 21, 22],
            "semester": ["Fall", "Fall", "Fall", "Spring", "Spring", "Spring"],
            "math": [85, 78, 92, 88, 79, 95],
            "science": [90, 82, 85, 92, 81, 87],
            "history": [88, 80, 87, 85, 82, 89],
        }
    )
    df
    return (df,)


@app.cell
def _(df):
    df.unpivot(
        index=["student", "class", "age", "semester"],
        on=["math", "science", "history"],
        variable_name="subject",
        value_name="grade",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Transposing
    """)
    return


@app.cell
def _(pl):
    grades_wide_2 = pl.DataFrame({'student': ['Jeroen', 'Thijs', 'Ritchie'], 'math': [85, 78, 92], 'science': [90, 82, 85], 'history': [88, 80, 87]})
    grades_wide_2
    return (grades_wide_2,)


@app.cell
def _(grades_wide_2):
    report_columns = (f'report_{i + 1}' for i, _ in enumerate(grades_wide_2.columns))
    grades_wide_2.transpose(include_header=True, header_name='original_headers', column_names=report_columns)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exploding
    """)
    return


@app.cell
def _(pl):
    grades_nested = pl.DataFrame(
        {
            "student": ["Jeroen", "Thijs", "Ritchie"],
            "math": [[85, 90, 88], [78, 82, 80], [92, 85, 87]],
        }
    )

    grades_nested
    return (grades_nested,)


@app.cell
def _(grades_nested):
    grades_nested.explode("math")
    return


@app.cell
def _(pl):
    grades_nested_1 = pl.DataFrame({'student': ['Jeroen', 'Thijs', 'Ritchie'], 'math': [[85, 90, 88], [78, 82, 80], [92, 85, 87]], 'science': [[85, 90, 88], [78, 82], [92, 85, 87]], 'history': [[85, 90, 88], [78, 82], [92, 85, 87]]})
    grades_nested_1
    return (grades_nested_1,)


@app.cell
def _():
    # This raises a ShapeError:
    # grades_nested.explode("math", "science", "history")
    return


@app.cell
def _(grades_nested_1):
    grades_nested_long = grades_nested_1.unpivot(index='student', variable_name='subject', value_name='grade')
    grades_nested_long
    return (grades_nested_long,)


@app.cell
def _(grades_nested_long):
    grades_nested_long.explode("grade")
    return


@app.cell
def _(pl):
    nested_lists = pl.DataFrame(
        {
            "id": [1, 2],
            "nested_value": [[["a", "b"]], [["c"], ["d", "e"]]],
        },
        strict=False,
    )
    nested_lists
    return (nested_lists,)


@app.cell
def _(nested_lists):
    nested_lists.explode("nested_value")
    return


@app.cell
def _(nested_lists):
    nested_lists.explode("nested_value").explode("nested_value")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Partition into Multiple DataFrames
    """)
    return


@app.cell
def _(pl):
    sales = pl.DataFrame(
        {
            "OrderID": [1, 2, 3, 4, 5, 6],
            "Product": ["A", "B", "A", "C", "B", "A"],
            "Quantity": [10, 5, 8, 7, 3, 12],
            "Region": ["North", "South", "North", "West", "South", "West"],
        }
    )
    return (sales,)


@app.cell
def _(sales):
    sales.partition_by("Region")
    return


@app.cell
def _(sales):
    sales.partition_by("Region", include_key=False)
    return


@app.cell
def _(sales):
    sales_dict = sales.partition_by(["Region"], as_dict=True)

    sales_dict
    return (sales_dict,)


@app.cell
def _(sales_dict):
    sales_dict[("North",)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()
