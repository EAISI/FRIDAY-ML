# Reference Documentation

This directory contains comprehensive reference materials and examples for the FRIDAY-ML project. These are educational resources that demonstrate best practices and patterns.

## Directory Structure

### `altair/`

Comprehensive Altair visualization reference documentation containing 8 marimo notebooks covering all aspects of the Altair declarative visualization library:

- **altair_introduction.py** - Getting started with Altair and basic concepts
- **altair_marks_encoding.py** - Understanding marks and encoding channels
- **altair_data_transformation.py** - Data transformations and aggregations
- **altair_scales_axes_legends.py** - Customizing scales, axes, and legends
- **altair_view_composition.py** - Layering, concatenation, and composition
- **altair_interaction.py** - Interactive visualizations and selections
- **altair_cartographic.py** - Geographic visualizations and maps
- **altair_debugging.py** - Debugging and troubleshooting tips

### `polars/`

Comprehensive Polars reference documentation containing 19 marimo notebooks covering all aspects of the Polars data manipulation library:

- **ch01.py** - Introduction and basic operations
- **ch02.py** - Data types and schemas
- **ch03.py** - Expressions and selectors
- **ch04.py** - Data transformation
- **ch05.py** - Missing data handling
- **ch06.py** - Aggregations
- **ch07.py** - Joins and concatenations
- **ch08.py** - Visualization with plotnine
- **ch09.py** - Lazy evaluation
- **ch10.py** - String operations
- **ch11.py** - List operations
- **ch12.py** - Struct operations
- **ch13.py** - Window functions
- **ch14.py** - Time series operations
- **ch15.py** - Categorical data
- **ch16.py** - Visualization with hvplot
- **ch17.py** - I/O operations
- **ch18.py** - Performance optimization
- **appendix1.py** - Advanced techniques and patterns

## Usage

These notebooks serve as:

1. **Learning Resources**: Study examples to understand Polars and Altair patterns
2. **Reference Material**: Look up specific operations and syntax
3. **Templates**: Copy patterns for your own notebooks
4. **Best Practices**: See idiomatic Polars data manipulation and Altair visualization code in action

## Running Reference Notebooks

You can run any reference notebook using marimo:

```bash
# Polars examples
uv run marimo edit references/polars/ch01.py
uv run marimo edit references/polars/ch01.py --watch  # with watch mode

# Altair examples
uv run marimo edit references/altair/altair_introduction.py
uv run marimo edit references/altair/altair_interaction.py --watch  # with watch mode

# Run in Positron with marimo extension for inline viewing
```

## See Also

- [.claude/rules/code-style.md](../.claude/rules/code-style.md) - Comprehensive Polars coding guidelines
- [notebooks/](../notebooks/) - Working ML example notebooks
