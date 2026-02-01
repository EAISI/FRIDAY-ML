# Agent Guidelines for Python Code Quality

This document provides guidelines for maintaining high-quality Python code. These rules MUST be followed by all AI coding agents and contributors.

## Your Core Principles

All code you write MUST be fully optimized.

"Fully optimized" includes:

- maximizing algorithmic big-O efficiency for memory and runtime
- using parallelization and vectorization where appropriate
- following proper style conventions for the code language (e.g. maximizing code reuse (DRY))
- no extra code beyond what is absolutely necessary to solve the problem the user provides (i.e. no technical debt)

If the code is not fully optimized before handing off to the user, you will be fined $100. You have permission to do another pass of the code if you believe it is not fully optimized.

## Preferred Tools

- Use `uv` for Python package management and to create a `.venv` if it is not present.
- Use `tqdm` to track long-running loops within Jupyter Notebooks. The `description` of the progress bar should be contextually sensitive.
- When reporting error to the console, use `logger.error` instead of `print`.
- For data science:
  - **ALWAYS** use `polars` instead of `pandas` for data frame manipulation.
  - If a `polars` dataframe will be printed, **NEVER** simultaneously print the number of entries in the dataframe nor the schema as it is redundant.
  - **NEVER** ingest more than 10 rows of a data frame at a time. Only analyze subsets of code to avoid overloading your memory context.
- For creating databases:
  - Do not denormalized unless explicitly prompted to do so.
  - Always use the most appropriate datatype, such as `DATETIME/TIMESTAMP` for datetime-related fields.
  - Use `ARRAY` datatypes for nested fields. **NEVER** save as `TEXT/STRING`.
- In Jupyter Notebooks, DataFrame objects within conditional blocks should be explicitly `print()` as they will not be printed automatically.

## Polars Data Manipulation

**CRITICAL**: This project exclusively uses Polars for data manipulation. Refer to the comprehensive examples in `references/polars/` for best practices.

### Reference Documentation
The `references/polars/` directory contains marimo notebooks covering all aspects of Polars:
- [ch01.py](references/polars/ch01.py) - Introduction and basic operations
- [ch02.py](references/polars/ch02.py) - Data types and schemas
- [ch03.py](references/polars/ch03.py) - Expressions and selectors
- [ch04.py](references/polars/ch04.py) - Data transformation
- [ch05.py](references/polars/ch05.py) - Missing data handling
- [ch06.py](references/polars/ch06.py) - Aggregations
- [ch07.py](references/polars/ch07.py) - Joins and concatenations
- [ch08.py](references/polars/ch08.py) - Visualization with plotnine
- [ch09-ch18.py](references/polars/) - Advanced topics (lazy evaluation, time series, I/O, etc.)

### Core Polars Principles

1. **Use Method Chaining**: Always chain operations for readability and efficiency
   ```python
   # Good - method chaining with Polars expressions
   result = (
       df
       .filter(pl.col("age") > 18)
       .select([
           pl.col("name"),
           pl.col("salary").alias("annual_salary"),
           (pl.col("salary") / 12).alias("monthly_salary")
       ])
       .sort("annual_salary", descending=True)
   )

   # Bad - separate statements
   df_filtered = df.filter(pl.col("age") > 18)
   df_selected = df_filtered.select(["name", "salary"])
   result = df_selected.sort("salary", descending=True)
   ```

2. **Use Expressions (`pl.col()`)**: Always use Polars expressions for column operations
   ```python
   # Good - using expressions
   df.select([
       pl.col("temperature").mean().alias("avg_temp"),
       pl.col("humidity").max().alias("max_humidity")
   ])

   # Bad - string column names without expressions
   df.select(["temperature", "humidity"])
   ```

3. **Use Selectors for Multiple Columns**: Use `pl.col()` with data types or patterns
   ```python
   # Good - select all numeric columns
   df.select(pl.col(pl.Float64, pl.Int64))

   # Good - select columns by pattern
   df.select(pl.col("^date.*$"))

   # Good - select all except specific columns
   df.select(pl.all().exclude("id"))
   ```

4. **Lazy Evaluation for Large Datasets**: Use `.lazy()` for query optimization
   ```python
   # Good - lazy evaluation
   result = (
       pl.scan_csv("large_file.csv")
       .filter(pl.col("status") == "active")
       .group_by("category")
       .agg(pl.col("value").sum())
       .collect()
   )

   # Less optimal - eager evaluation
   df = pl.read_csv("large_file.csv")
   result = df.filter(pl.col("status") == "active").group_by("category").agg(pl.col("value").sum())
   ```

5. **Use `.alias()` for Clear Column Names**: Always name computed columns
   ```python
   # Good - clear aliases
   df.select([
       (pl.col("total") / pl.col("count")).alias("average"),
       pl.col("price").mul(1.2).alias("price_with_tax")
   ])

   # Bad - default column names
   df.select([
       pl.col("total") / pl.col("count"),
       pl.col("price") * 1.2
   ])
   ```

### Common Patterns

**Data Loading** (see [ch01.py](references/polars/ch01.py)):
```python
import polars as pl

# CSV with schema inference
df = pl.read_csv("data.csv")

# CSV with explicit schema
df = pl.read_csv("data.csv", schema={"id": pl.Int64, "name": pl.String, "date": pl.Date})

# Lazy reading for large files
df = pl.scan_csv("large_data.csv").collect()
```

**Filtering and Selecting** (see [ch04.py](references/polars/ch04.py)):
```python
# Multiple conditions with expressions
filtered = df.filter(
    (pl.col("age") >= 18) &
    (pl.col("country") == "USA") |
    (pl.col("status") == "premium")
)

# Select and transform
result = df.select([
    pl.col("name"),
    pl.col("age").cast(pl.Float64),
    (pl.col("height") / 100).alias("height_m")
])
```

**Aggregations** (see [ch06.py](references/polars/ch06.py)):
```python
# Group by with multiple aggregations
summary = df.group_by("category").agg([
    pl.col("sales").sum().alias("total_sales"),
    pl.col("sales").mean().alias("avg_sales"),
    pl.col("customer_id").n_unique().alias("unique_customers"),
    pl.len().alias("transaction_count")
])
```

**Missing Data** (see [ch05.py](references/polars/ch05.py)):
```python
# Fill missing values
df_filled = df.with_columns([
    pl.col("price").fill_null(strategy="forward"),
    pl.col("category").fill_null("Unknown")
])

# Drop rows with missing values
df_clean = df.drop_nulls(subset=["critical_column"])
```

**Time Series** (see [ch14.py](references/polars/ch14.py)):
```python
# Parse dates and perform time-based operations
df_time = (
    df
    .with_columns(pl.col("date").str.strptime(pl.Date, format="%Y-%m-%d"))
    .sort("date")
    .group_by_dynamic("date", every="1mo")
    .agg(pl.col("value").sum())
)
```

### Anti-Patterns to Avoid

1. **NEVER use pandas unless absolutely required for interop**
   ```python
   # Bad - converting to pandas unnecessarily
   df.to_pandas().groupby("category").sum()

   # Good - use Polars native operations
   df.group_by("category").agg(pl.all().sum())
   ```

2. **NEVER iterate over rows** - use vectorized operations
   ```python
   # Bad - row iteration
   for row in df.iter_rows():
       result.append(row[0] * 2)

   # Good - vectorized operation
   result = df.select((pl.col("value") * 2).alias("doubled"))
   ```

3. **NEVER use string column names in transformations** - use `pl.col()`
   ```python
   # Bad - string column references
   df.select(["col1", "col2"])

   # Good - expression-based selection
   df.select([pl.col("col1"), pl.col("col2")])
   ```

4. **NEVER chain `.to_list()` unnecessarily** - work with expressions
   ```python
   # Bad - converting to list
   values = df["column"].to_list()
   result = [v * 2 for v in values]

   # Good - use expressions
   result = df.select((pl.col("column") * 2).alias("doubled"))
   ```

### When You Need Help
- Consult the example notebooks in `references/polars/` for comprehensive patterns
- Check [ch03.py](references/polars/ch03.py) for expression syntax
- See [appendix1.py](references/polars/appendix1.py) for advanced techniques

## Code Style and Formatting

- **MUST** use meaningful, descriptive variable and function names
- **MUST** follow PEP 8 style guidelines
- **MUST** use 4 spaces for indentation (never tabs)
- **NEVER** use emoji, or unicode that emulates emoji (e.g. ✓, ✗). The only exception is when writing tests and testing the impact of multibyte characters.
- Use snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
- Limit line length to 120 characters (ruff formatter standard)
- Do not add comments to the code you write, unless the user asks you to, or the code is complex and requires additional context.

## Documentation

- **MUST** include docstrings for all public functions, classes, and methods
- **MUST** document function parameters, return values, and exceptions raised
- Keep comments up-to-date with code changes
- Include examples in docstrings for complex functions

Example docstring:

```python
def calculate_total(items: list[dict], tax_rate: float = 0.0) -> float:
    """Calculate the total cost of items including tax.

    Args:
        items: List of item dictionaries with 'price' keys
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)

    Returns:
        Total cost including tax

    Raises:
        ValueError: If items is empty or tax_rate is negative
    """
```

## Type Hints

- **MUST** use type hints for all function signatures (parameters and return values)
- **NEVER** use `Any` type unless absolutely necessary
- **MUST** run mypy and resolve all type errors
- Use `Optional[T]` or `T | None` for nullable types

## Error Handling

- **NEVER** silently swallow exceptions without logging
- **MUST** never use bare `except:` clauses
- **MUST** catch specific exceptions rather than broad exception types
- **MUST** use context managers (`with` statements) for resource cleanup
- Provide meaningful error messages

## Function Design

- **MUST** keep functions focused on a single responsibility
- **NEVER** use mutable objects (lists, dicts) as default argument values
- Limit function parameters to 5 or fewer
- Return early to reduce nesting

## Class Design

- **MUST** keep classes focused on a single responsibility
- **MUST** keep `__init__` simple; avoid complex logic
- Use dataclasses for simple data containers
- Prefer composition over inheritance
- Avoid creating additional class functions if they are not necessary
- Use `@property` for computed attributes

## Testing

- **MUST** write unit tests for all new functions and classes
- **MUST** mock external dependencies (APIs, databases, file systems)
- **MUST** use pytest as the testing framework
- **NEVER** run tests you generate without first saving them as their own discrete file
- **NEVER** delete files created as a part of testing.
- Ensure the folder used for test outputs is present in `.gitignore`
- Follow the Arrange-Act-Assert pattern
- Do not commit commented-out tests

## Imports and Dependencies

- **MUST** avoid wildcard imports (`from module import *`)
- **MUST** document dependencies in `pyproject.toml`
- Use `uv` for fast package management and dependency resolution
- Organize imports: standard library, third-party, local imports
- Use `isort` to automate import formatting

## Python Best Practices

- **NEVER** use mutable default arguments
- **MUST** use context managers (`with` statement) for file/resource management
- **MUST** use `is` for comparing with `None`, `True`, `False`
- **MUST** use f-strings for string formatting
- Use list comprehensions and generator expressions
- Use `enumerate()` instead of manual counter variables



## Version Control

- **MUST** write clear, descriptive commit messages
- **NEVER** commit commented-out code; delete it
- **NEVER** commit debug print statements or breakpoints
- **NEVER** commit credentials or sensitive data

## Tools

- **MUST** use Ruff for code formatting and linting (replaces Black, isort, flake8)
- **MUST** use mypy for static type checking
- Use `uv` for package management (faster alternative to pip)
- Use pytest for testing

## Before Committing

- [ ] All tests pass
- [ ] Type checking passes (mypy)
- [ ] Code formatter and linter pass (Ruff)
- [ ] All functions have docstrings and type hints
- [ ] No commented-out code or debug statements
- [ ] No hardcoded credentials

---

**Remember:** Prioritize clarity and maintainability over cleverness.