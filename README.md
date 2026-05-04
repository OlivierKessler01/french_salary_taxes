# French income tax and housing loan calculator

Works for any couple.

Inputs are yearly **gross** salaries (salaire brut). The script approximates net and taxable income using cadre conversion ratios (gross × 0.78 → net, net × 1.025 → taxable).

## Run

```sh
uv run python -m my_taxes --income_1=<gross> --income_2=<gross> --nb_children=<n>
```

`uv` resolves dependencies from `pyproject.toml` and creates the virtualenv on first run.
