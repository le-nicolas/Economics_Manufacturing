# Economics Manufacturing Cost Explorer

Small Python project that compares **conventional manufacturing** vs **additive manufacturing** in two ways:

- Cost per unit as production volume increases
- Cost per piece as geometric complexity increases

The script plots both comparisons side-by-side and computes break-even points from the model inputs.

## What This Models

1. `Volume` model:
- Conventional: `(setup_cost / volume) + variable_cost`
- Additive: `constant additive_unit_cost`

2. `Complexity` model:
- Conventional: `coefficient * complexity^exponent`
- Additive: `constant additive_piece_cost`

The break-even values are solved directly from those equations.

## Requirements

- Python 3.9+
- `numpy`
- `matplotlib`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run with defaults:

```bash
python main.py
```

Run headless and save a chart:

```bash
python main.py --no-show --save-path output/cost_comparison.png
```

Customize cost assumptions:

```bash
python main.py --setup-cost 250 --variable-cost 9 --additive-unit-cost 18 --complexity-coefficient 0.08 --complexity-exponent 2.2 --additive-piece-cost 55
```

Useful flags:

- `--max-volume`: max x-axis value for volume graph (default `100`)
- `--max-complexity`: max x-axis value for complexity graph (default `100`)
- `--points`: number of points per curve (default `500`)
- `--save-path`: save figure to file
- `--no-show`: do not open interactive window

## Tests

```bash
python -m unittest discover -s tests
```

## Notes

- This is a simplified educational model, not a full manufacturing quote engine.
- Add extra terms (material waste, machine depreciation, labor tiers, quality/rework costs) if you need production-grade forecasting.
