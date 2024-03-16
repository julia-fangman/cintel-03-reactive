import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import reactive, render, req
import palmerpenguins
import seaborn as sns
import pandas as pd

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Julia's Penguin Data", fillable=True)

with ui.sidebar(position="right", open="open"):
    ui.h2("Sidebar")
    
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 15)
    
    ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 1, 40, 20)
    
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Chinstrap"],
        inline=False,
    )
    ui.hr()
    
    ui.a("Github", href="https://github.com/julia-fangman/cintel-02-data", target="_blank")

# Accordion Layout with DataTable and DataGrid
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return penguins_df

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return penguins_df

# Created a card with tabs for graphs
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):
        @render_plotly
        def plotly_histogram():
            return px.histogram(
                penguins_df,
                x=input.selected_attribute(),
                color="species",
                nbins=input.plotly_bin_count(),
                width=800,
                height=400,
            )

    with ui.nav_panel("Seaborn Histogram"):
        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            histplot = sns.histplot(
                data=penguins_df, x="body_mass_g", bins=input.seaborn_bin_count()
            )
            histplot.set_title("Palmer Penguins")
            histplot.set_xlabel("Mass")
            histplot.set_ylabel("Count")
            return histplot

    with ui.nav_panel("Plotly Scatterplot"):
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                penguins_df,
                x="bill_length_mm",
                y="body_mass_g",
                color="species",
                title="Penguins Plot",
                labels={
                    "bill_length_mm": "Bill Length (mm)",
                    "body_mass_g": "Body Mass (g)",
                },
                size_max=5,
                width=1200,
                height=600,
            )

    with ui.nav_panel("Plotly Box Plot"):
        @render_plotly
        def plotly_box_plot():
            return px.box(
                penguins_df,
                x="species",
                y=input.selected_attribute(),
                color="species",
                title="Penguins Box Plot",
            )

    with ui.nav_menu("Other Links"):
        with ui.nav_panel("Pie Chart"):
            species_distribution = penguins_df["species"].value_counts().reset_index()
            species_distribution.columns = ["species", "count"]
            @render_plotly
            def pie_chart():
                return px.pie(
                    species_distribution,
                    values="count",
                    names="species",
                    title="Species Distribution",
                )
