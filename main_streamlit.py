import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import streamlit as st
from common import set_plt_theme


def _get_l_system(axiom: str, rules: dict[str, str], iterations: int) -> str:
    instructions = axiom
    for _ in range(iterations):
        new_instructions = ""
        for cmd in instructions:
            # Use rule if possible, else keep the character
            new_instructions += rules.get(cmd, cmd)
        instructions = new_instructions
    return instructions


def _rot_mat(angle: float) -> np.ndarray:
    """
    Return a 2D rotational matrix for the given angle.
    """
    return np.array(
        [
            [np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
            [np.sin(np.radians(angle)), np.cos(np.radians(angle))],
        ]
    )


def draw_l_system(
    axiom: str,
    rules: dict,
    iterations: int,
    angle: float,
    length: int,
    color: str = "tab:orange",
    lw: int = 1,
) -> Figure:
    """
    Generate and draw the L-system.
    """
    instructions = _get_l_system(axiom, rules, iterations)
    stack = []
    turtle_pos = np.array([0, 0])  # Initial position
    turtle_heading = np.array([0, 1])  # Initial direction

    # Initialize plot
    fig = plt.figure()
    ax = plt.gca()
    ax.set_aspect("equal")
    ax.set_axis_off()

    # Interpret instructions and draw
    for instruction in instructions:
        if instruction == "F":
            # Move forward
            new_pos = turtle_pos + length * turtle_heading
            ax.plot(
                [turtle_pos[0], new_pos[0]],
                [turtle_pos[1], new_pos[1]],
                color=color,
                lw=lw,
            )
            turtle_pos = new_pos
        elif instruction == "b":
            # Move forward without leaving a trail
            new_pos = turtle_pos + length * turtle_heading
            turtle_pos = new_pos
        elif instruction == "+":
            # Turn right on given rotation angle
            turtle_heading = np.dot(_rot_mat(angle), turtle_heading)
        elif instruction == "-":
            # Turn left on given rotation angle
            turtle_heading = np.dot(_rot_mat(-angle), turtle_heading)
        elif instruction == "[":
            # Save current position and heading
            stack.append((turtle_pos, turtle_heading))
        elif instruction == "]":
            # Restore position and heading
            turtle_pos, turtle_heading = stack.pop()

    return fig


def main():
    st.title("L-Systems")
    set_plt_theme()

    # Inspired by: https://fedimser.github.io/l-systems.html
    default_settings = {
        "Koch's Snowflake": {
            "axiom": "F++F++F",
            "rules": {"F": "F:F-F++F-F"},
            "angle": 60,
        },
        "Levy curve": {
            "axiom": "F++F++F++F",
            "rules": {"F": "F:-F++F-"},
            "angle": 45,
            "iterations": 8,
        },
        "Serpinski Triangle": {
            "axiom": "FXF--FF--FF",
            "rules": {"F": "F:FF", "X": "X:--FXF++FXF++FXF--"},
            "angle": 60,
            "iterations": 5,
        },
        "Sierpinski Carpet": {
            "axiom": "F",
            "rules": {"F": "F:FFF[+FFF+FFF+FFF]"},
            "angle": 90,
            "iterations": 4,
        },
        "Sierpinski Carpet 2": {
            "axiom": "F+F+F+F",
            "rules": {"F": "F:FF+F+F+F+FF"},
            "angle": 90,
        },
        "Koch Curve Generalization": {
            "axiom": "F+F+F+F",
            "rules": {"F": "F:F+F-F-FF+F+F-F"},
            "angle": 90,
        },
        "Mosaic": {
            "axiom": "F+F+F+F",
            "rules": {"F": "F:F-b+FF-F-FF-Fb-FF+b-FF+F+FF+Fb+FFF", "b": "b:bbbbbb"},
            "angle": 90,
            "iterations": 2,
        },
        "Weird Snowflake": {
            "axiom": "F++F++F",
            "rules": {"F": "F:F+F--F+F"},
            "angle": 60,
        },
        "Tree": {
            "axiom": "F",
            "rules": {"F": "F:FF+[+F-F-F]-[-F+F+F]"},
            "angle": np.pi / 8,
            "angle_in_radians": True,
        },
        "Weed": {
            "axiom": "F",
            "rules": {"F": "F:F[+F]F[-F]F"},
            "angle": np.pi / 7,
            "angle_in_radians": True,
        },
    }
    selected_setting = st.selectbox(
        "Choose a pre-made setting", list(default_settings.keys())
    )
    selected_settings = default_settings[selected_setting]

    axiom = st.text_input("Axiom", selected_settings.get("axiom", "F"))
    rules_text = st.text_area(
        label="Rules",
        value=",".join(selected_settings.get("rules", {"F": "F:F-F++F-F"}).values()),
        help="Enter comma-separated rules, e.g., `F:F+F-F,b:bbb`",
    )
    rules = dict(rule.split(":") for rule in rules_text.split(","))
    iterations = st.slider(
        "Iterations",
        min_value=1,
        max_value=8,
        value=selected_settings.get("iterations", 3),
    )
    angle_in_radians = st.checkbox(
        "Use radians for angle",
        value=selected_settings.get("angle_in_radians", False),
    )
    angle_label = "Angle (radians)" if angle_in_radians else "Angle (degrees)"
    angle = st.slider(
        angle_label,
        min_value=0.0,
        max_value=np.pi if angle_in_radians else 180.0,
        value=float(selected_settings.get("angle", np.pi / 2))
        if angle_in_radians
        else float(selected_settings.get("angle", 90.0)),
        step=0.01,
    )
    angle = float(np.degrees(angle)) if angle_in_radians else angle
    length = st.slider("Length", min_value=1, max_value=100, value=10)

    st.pyplot(
        draw_l_system(axiom, rules, iterations, angle, length),
        use_container_width=True,
    )


if __name__ == "__main__":
    # streamlit.cmd run '.\main_streamlit.py'
    main()
