import os
import ipywidgets as widgets
from IPython.display import display
import ipywidgets as widgets

# Meeting notes
notes_box = widgets.Textarea(
    value=sample_notes,
    description="Notes:",
    layout=widgets.Layout(width="95%", height="170px"),
    style={"description_width": "initial"}
)

# Mode selection
mode_box = widgets.ToggleButtons(
    options=[
        ("Offline", "offline"),
        ("Gemini API", "live")
    ],
    value="offline",
    description="Mode:"
)

# Gemini API key input
api_key_box = widgets.Password(
    description="Gemini API Key:",
    placeholder="Enter your Gemini API key",
    layout=widgets.Layout(width="95%"),
    style={"description_width": "initial"}
)

# API key field container
api_key_container = widgets.VBox([api_key_box])
api_key_container.layout.display = "none"

# Show API key field only in live mode
def on_mode_change(change):
    if change["name"] == "value":
        api_key_container.layout.display = (
            "flex" if change["new"] == "live" else "none"
        )

mode_box.observe(on_mode_change, names="value")

# Extract button
button = widgets.Button(
    description="Extract action items",
    button_style="primary",
    icon="check"
)

output = widgets.Output()

# Button click handler
def on_extract_clicked(_):

    with output:
        output.clear_output()

        text = notes_box.value.strip()

        if not text:
            print("Please enter meeting notes first.")
            return

        mode = mode_box.value

        print(
            "Mode:",
            "Offline" if mode == "offline" else "LIVE GEMINI API"
        )

        try:
            if mode == "offline":
                actions = offline_extract(text)

            else:
                api_key = api_key_box.value.strip()

                if not api_key:
                    print("Please enter your Gemini API key.")
                    return

                # Make key available to live_extract()
                os.environ["GEMINI_API_KEY"] = api_key

                actions = live_extract(text)

        except Exception as exc:
            print(
                f"Could not extract items "
                f"({type(exc).__name__}). "
                "Check your API configuration and network."
            )
            return

        if not actions:
            print("No action items found.")
            return

        print("\nExtracted Action Items")
        print("-" * 40)

        for i, action in enumerate(actions, 1):
            print(f"\n{i}. {action['task']}")
            print(f"   Owner: {action['owner']}")
            print(f"   Due: {action['deadline']}")

        print(
            "\nReview every item against the "
            "original notes before using it."
        )

button.on_click(on_extract_clicked)

# Display complete application
display(
    widgets.VBox([
        widgets.HTML("<h3>AI Meeting Action Item Extractor</h3>"),
        notes_box,
        mode_box,
        api_key_container,
        button,
        output
    ])
)