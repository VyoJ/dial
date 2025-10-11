"""Command-line interface for the dial library."""

from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

import dial

app = typer.Typer(
    name="dial",
    help="Generate analog clock faces with customizable styles and times.",
    add_completion=False,
)


@app.command()
def create(
    time: Annotated[str, typer.Argument(help="Time in HH:MM:SS format")],
    output: Annotated[Path, typer.Argument(help="Output file path (PNG, JPG, etc.)")],
    style: Annotated[
        str, typer.Option("--style", "-s", help="Preset style")
    ] = "classic",
    width: Annotated[
        int, typer.Option("--width", "-w", help="Clock width in pixels")
    ] = 400,
    height: Annotated[
        int, typer.Option("--height", "-h", help="Clock height in pixels")
    ] = 400,
    quality: Annotated[
        int, typer.Option("--quality", "-q", help="Quality scale factor (1-4)")
    ] = 2,
    antialias: Annotated[
        bool, typer.Option("--antialias/--no-antialias", help="Enable antialiasing")
    ] = True,
) -> None:
    """Create a clock with the specified time and style."""
    try:
        # Validate style
        available_styles = list(dial.Clock.PRESET_STYLES.keys())
        if style not in available_styles:
            typer.echo(
                f"Error: Unknown style '{style}'. Available styles: {', '.join(available_styles)}",
                err=True,
            )
            raise typer.Exit(1)

        # Create clock
        clock = dial.Clock.create(
            time=time,
            style=style,
            width=width,
            height=height,
            antialias=antialias,
            scale_factor=quality,
        )

        # Save clock
        clock.save(str(output))
        typer.echo(f"Clock saved to {output}")

    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def styles() -> None:
    """List available preset styles."""
    typer.echo("Available preset styles:")
    for style_name, style_config in dial.Clock.PRESET_STYLES.items():
        typer.echo(f"  {style_name}")

        # Show basic info about each style
        if "face" in style_config:
            face_color = style_config["face"].get("color", "default")
            typer.echo(f"    • Face: {face_color}")

        if "numerals" in style_config:
            system = style_config["numerals"].get("system", "arabic")
            visible = style_config["numerals"].get("visible")
            if visible:
                typer.echo(f"    • Numerals: {system} ({', '.join(map(str, visible))})")
            else:
                typer.echo(f"    • Numerals: {system} (all)")


@app.command()
def example(
    output_dir: Annotated[
        Optional[Path], typer.Argument(help="Output directory for examples")
    ] = None,
) -> None:
    """Generate example clocks with different styles and times."""
    if output_dir is None:
        output_dir = Path("examples")

    output_dir.mkdir(exist_ok=True)

    styles = list(dial.Clock.PRESET_STYLES.keys())
    times = ["12:00:00", "3:15:30", "6:30:45", "9:45:15"]

    typer.echo(f"Generating examples in {output_dir}")

    total = len(styles) * len(times)
    with typer.progressbar(range(total), label="Creating clocks") as progress:
        for style in styles:
            for time in times:
                clock = dial.Clock.create(time, style, width=300, height=300)
                filename = f"{style}_{time.replace(':', '')}.png"
                clock.save(output_dir / filename)
                next(progress)

    typer.echo(f"Generated {total} example clocks")


@app.command()
def config(
    config_file: Annotated[Path, typer.Argument(help="JSON configuration file")],
    output: Annotated[Path, typer.Argument(help="Output file path")],
) -> None:
    """Create a clock from a JSON configuration file."""
    try:
        import json

        # Read configuration
        with open(config_file, "r") as f:
            config = json.load(f)

        # Create clock from config
        clock = dial.Clock.from_config(config)

        # Save clock
        clock.save(str(output))
        typer.echo(f"Clock created from {config_file} and saved to {output}")

    except FileNotFoundError:
        typer.echo(f"Error: Configuration file '{config_file}' not found", err=True)
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        typer.echo(f"Error: Invalid JSON in '{config_file}': {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
