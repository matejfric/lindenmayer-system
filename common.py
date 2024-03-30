import matplotlib.pyplot as plt
from streamlit_theme import (
    st_theme,
)  # https://github.com/streamlit/streamlit/issues/5009


def set_plt_theme() -> None:
    """Set the matplotlib theme based on the Streamlit theme."""
    theme = st_theme()

    if theme is not None:
        theme: dict
        theme: str = theme.get("base")

    if theme == "light":
        plt.style.use("default")
    else:
        plt.style.use("dark_background")
