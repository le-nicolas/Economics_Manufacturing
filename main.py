from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class VolumeCostModel:
    """Cost assumptions for volume-driven comparison."""

    setup_cost: float = 100.0
    variable_cost: float = 10.0
    additive_unit_cost: float = 20.0

    def conventional_cost(self, volume: np.ndarray) -> np.ndarray:
        safe_volume = np.maximum(volume, 1e-9)
        return (self.setup_cost / safe_volume) + self.variable_cost

    def additive_cost(self, volume: np.ndarray) -> np.ndarray:
        return np.full_like(volume, self.additive_unit_cost, dtype=float)

    def breakeven_volume(self) -> Optional[float]:
        margin = self.additive_unit_cost - self.variable_cost
        if margin <= 0:
            return None
        return self.setup_cost / margin


@dataclass(frozen=True)
class ComplexityCostModel:
    """Cost assumptions for complexity-driven comparison."""

    coefficient: float = 0.1
    exponent: float = 2.0
    additive_piece_cost: float = 50.0

    def conventional_cost(self, complexity: np.ndarray) -> np.ndarray:
        return self.coefficient * np.power(complexity, self.exponent)

    def additive_cost(self, complexity: np.ndarray) -> np.ndarray:
        return np.full_like(complexity, self.additive_piece_cost, dtype=float)

    def breakeven_complexity(self) -> Optional[float]:
        if self.coefficient <= 0 or self.exponent <= 0 or self.additive_piece_cost <= 0:
            return None
        return (self.additive_piece_cost / self.coefficient) ** (1 / self.exponent)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare additive vs conventional manufacturing cost behavior.",
    )

    parser.add_argument("--max-volume", type=float, default=100.0, help="Max units for volume graph.")
    parser.add_argument("--max-complexity", type=float, default=100.0, help="Max complexity for complexity graph.")
    parser.add_argument("--points", type=int, default=500, help="Number of points per curve.")

    parser.add_argument("--setup-cost", type=float, default=100.0, help="Conventional setup/tooling cost.")
    parser.add_argument("--variable-cost", type=float, default=10.0, help="Conventional variable cost per unit.")
    parser.add_argument("--additive-unit-cost", type=float, default=20.0, help="Additive cost per unit.")

    parser.add_argument("--complexity-coefficient", type=float, default=0.1, help="Conventional complexity coefficient.")
    parser.add_argument("--complexity-exponent", type=float, default=2.0, help="Conventional complexity exponent.")
    parser.add_argument("--additive-piece-cost", type=float, default=50.0, help="Additive cost per piece vs complexity.")

    parser.add_argument("--save-path", type=Path, help="Optional output path for figure, e.g. output.png.")
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open an interactive window (useful for CI/headless environments).",
    )
    return parser


def validate_inputs(args: argparse.Namespace) -> None:
    if args.max_volume <= 1:
        raise ValueError("--max-volume must be > 1.")
    if args.max_complexity <= 1:
        raise ValueError("--max-complexity must be > 1.")
    if args.points < 10:
        raise ValueError("--points must be >= 10.")


def add_breakeven_line(ax: plt.Axes, x_value: Optional[float], x_max: float, label: str, color: str) -> None:
    if x_value is None:
        return
    if 1 <= x_value <= x_max:
        ax.axvline(x=x_value, color=color, linestyle=":", label=label)


def create_cost_figure(
    volume_model: VolumeCostModel,
    complexity_model: ComplexityCostModel,
    max_volume: float,
    max_complexity: float,
    points: int,
) -> plt.Figure:
    volume = np.linspace(1, max_volume, points)
    complexity = np.linspace(1, max_complexity, points)

    volume_conventional = volume_model.conventional_cost(volume)
    volume_additive = volume_model.additive_cost(volume)

    complexity_conventional = complexity_model.conventional_cost(complexity)
    complexity_additive = complexity_model.additive_cost(complexity)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].plot(volume, volume_conventional, label="Conventional Manufacturing", color="tab:blue")
    axes[0].plot(volume, volume_additive, label="Additive Manufacturing", color="tab:green", linestyle="--")
    add_breakeven_line(
        axes[0],
        volume_model.breakeven_volume(),
        max_volume,
        label="Volume break-even",
        color="tab:orange",
    )
    axes[0].set_title("Cost per Unit vs Volume")
    axes[0].set_xlabel("Units Manufactured")
    axes[0].set_ylabel("Cost per Unit")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(complexity, complexity_conventional, label="Conventional Manufacturing", color="tab:blue")
    axes[1].plot(complexity, complexity_additive, label="Additive Manufacturing", color="tab:green", linestyle="--")
    add_breakeven_line(
        axes[1],
        complexity_model.breakeven_complexity(),
        max_complexity,
        label="Complexity break-even",
        color="tab:red",
    )
    axes[1].set_title("Cost per Piece vs Geometric Complexity")
    axes[1].set_xlabel("Geometric Complexity")
    axes[1].set_ylabel("Cost per Piece")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


def print_summary(volume_model: VolumeCostModel, complexity_model: ComplexityCostModel) -> None:
    volume_break_even = volume_model.breakeven_volume()
    complexity_break_even = complexity_model.breakeven_complexity()

    if volume_break_even is None:
        print("Volume break-even: not defined with current cost assumptions.")
    else:
        print(f"Volume break-even: {volume_break_even:.2f} units")

    if complexity_break_even is None:
        print("Complexity break-even: not defined with current cost assumptions.")
    else:
        print(f"Complexity break-even: {complexity_break_even:.2f} complexity units")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    validate_inputs(args)

    volume_model = VolumeCostModel(
        setup_cost=args.setup_cost,
        variable_cost=args.variable_cost,
        additive_unit_cost=args.additive_unit_cost,
    )
    complexity_model = ComplexityCostModel(
        coefficient=args.complexity_coefficient,
        exponent=args.complexity_exponent,
        additive_piece_cost=args.additive_piece_cost,
    )

    fig = create_cost_figure(
        volume_model=volume_model,
        complexity_model=complexity_model,
        max_volume=args.max_volume,
        max_complexity=args.max_complexity,
        points=args.points,
    )

    print_summary(volume_model, complexity_model)

    if args.save_path:
        args.save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.save_path, dpi=150)
        print(f"Saved figure: {args.save_path}")

    if not args.no_show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
