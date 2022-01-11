import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from string import Template

# ===========================================================================
# GUARDINT asset URL and color scheme
# ===========================================================================

asset_url = "https://guardint-assets.sehn.dev"
colors = [
    "#600b0c",
    "#C01518",
    "#ff1c1f",
    "#ff5557",
    "#ff8e8f",
    "#ffc7c7",
    "#ffe3e3",
    "#efefef",
]

# ===========================================================================
# Utility Functions to be cached
# ===========================================================================


@st.cache
def gen_px_pie(df, values, names, color_discrete_sequence=colors, **kwargs):
    fig = px.pie(
        df,
        values=values,
        names=names,
        color_discrete_sequence=color_discrete_sequence,
        color=kwargs.get("color", None),
        color_discrete_map=kwargs.get("color_discrete_map", None),
        custom_data=kwargs.get("custom_data", None),
    )
    # Update what is shown on the slices (on hover)
    fig.update_traces(
        texttemplate="<b>%{value}</b><br>%{percent}",
        hovertemplate="""<b>Answer</b> %{label}
<br><br>given by <b>%{value}</b> respondents or <b>%{percent}</b>
<br>of all who answered the question
<br>given the current filter.
        """,
    )
    # Update layout
    fig.update_layout(
        autosize=False,
        width=700,
        height=450,
        margin=dict(l=0, r=0, b=100, t=30),
        font={"size": 18, "family": "Roboto Mono, monospace"},
        legend={
            "font": {"size": kwargs.get("legend_font_size", 12)},
            "orientation": kwargs.get("legend_orientation", "h"),
            "bgcolor": "#efefef",
            "x": -0.2,
            "y": 1.1,
        },
        modebar={"orientation": "v"},
    )
    # Add logo
    fig.add_layout_image(
        dict(
            source=f"{asset_url}/guardint_logo.png",
            xref="paper",
            yref="paper",
            x=1.00,
            y=0.00,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


@st.cache
def gen_go_pie(labels, values, marker_colors=colors, **kwargs):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels, values=values, marker_colors=marker_colors, sort=False
            )
        ]
    )
    # Update what is shown on the slices (on hover)
    fig.update_traces(
        texttemplate="<b>%{value}</b><br>%{percent}",
        hovertemplate="""<b>Answer</b> %{label}
<br><br>given by <b>%{value}</b> respondents or <b>%{percent}</b>
<br>of all who answered the question
<br>given the current filter.<extra></extra>
        """,
    )
    # Update layout
    fig.update_layout(
        autosize=False,
        width=700,
        height=kwargs.get("height", 450),
        margin=dict(l=0, r=0, b=50, t=30),
        font={"size": kwargs.get("font_size", 18), "family": "Roboto Mono, monospace"},
        legend={
            "font": {"size": kwargs.get("legend_font_size", 12)},
            "orientation": "v",
            "bgcolor": "#efefef",
            "x": kwargs.get("legend_x", -0.2),
            "y": kwargs.get("legend_y", 1.1),
        },
        modebar={"orientation": "v"},
    )
    # Add logo
    fig.add_layout_image(
        dict(
            source=f"{asset_url}/guardint_logo.png",
            xref="paper",
            yref="paper",
            x=1.00,
            y=0.00,
            sizex=kwargs.get("image_sizex", 0.15),
            sizey=kwargs.get("image_sizey", 0.15),
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


@st.cache
def gen_px_histogram(
    df, x, y, nbins, color, labels, color_discrete_map=colors, **kwargs
):
    fig = px.histogram(
        df,
        x=x,
        y=y,
        nbins=nbins,
        color=color,
        color_discrete_map=color_discrete_map,
        labels=labels,
        marginal=kwargs.get("marginal", "rug"),
    )
    # Update layout
    fig.update_layout(
        autosize=False,
        width=700,
        height=450,
        margin=dict(l=0, r=0, b=100, t=30),
        font={"size": kwargs.get("font_size", 13), "family": "Roboto Mono, monospace"},
        legend={
            "font": {"size": kwargs.get("legend_font_size", 10)},
        },
        modebar={"orientation": "h"},
    )
    # Add logo
    fig.add_layout_image(
        dict(
            source="{asset_url}/guardint_logo.png",
            xref="paper",
            yref="paper",
            x=1.18,
            y=-0.005,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


@st.cache
def gen_go_histogram_overlaid(traces, names, colors, **kwargs):
    fig = go.Figure()
    for trace, name, color in zip(traces, names, colors):
        fig.add_trace(
            go.Histogram(
                x=trace,
                name=name,
                marker_color=color,
                xbins={"size": 2},
                cumulative_enabled=True,
            )
        )
    fig.update_layout(barmode="overlay")
    fig.update_traces(opacity=0.75)
    # Update layout
    fig.update_layout(
        autosize=False,
        width=700,
        height=450,
        margin=dict(l=0, r=0, b=100, t=30),
        font={"size": kwargs.get("font_size", 13), "family": "Roboto Mono, monospace"},
        legend={
            "font": {"size": kwargs.get("legend_font_size", 10)},
        },
        modebar={"orientation": "h"},
    )
    # Add logo
    fig.add_layout_image(
        dict(
            source="{asset_url}/guardint_logo.png",
            xref="paper",
            yref="paper",
            x=1.18,
            y=-0.005,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


@st.cache
def gen_px_box(df, x, y, points, color, labels, color_discrete_map=colors, **kwargs):
    fig = px.box(
        df,
        x=x,
        y=y,
        points=points,
        color=color,
        labels=labels,
        color_discrete_map=color_discrete_map,
    )
    # Update layout
    fig.update_layout(
        autosize=False,
        width=700,
        height=450,
        margin=dict(l=0, r=0, b=100, t=30),
        font={"size": 13, "family": "Roboto Mono, monospace"},
        legend={
            "font": {"size": kwargs.get("legend_font_size", 10)},
        },
        modebar={"orientation": "h"},
    )
    # Add logo
    fig.add_layout_image(
        dict(
            source="{asset_url}/guardint_logo.png",
            xref="paper",
            yref="paper",
            x=1.18,
            y=-0.005,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


@st.cache
def gen_go_bar_stack(data, **kwargs):
    fig = go.Figure(data=data)
    # Update layout
    fig.update_layout(
        barmode="stack",
        autosize=False,
        width=700,
        height=700,
        margin=dict(l=0, r=0, b=100, t=30),
        font={"size": 13, "family": "Roboto Mono, monospace"},
        legend={
            "font": {"size": kwargs.get("legend_font_size", 10)},
        },
        modebar={"orientation": "h"},
    )
    # Add logo
    fig.add_layout_image(
        dict(
            source="{asset_url}/guardint_logo.png",
            xref="paper",
            yref="paper",
            x=1.18,
            y=-0.005,
            sizex=0.15,
            sizey=0.15,
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


@st.cache
def gen_rank_plt(input_col, options, **kwargs):
    input_col_score = pd.Series(index=options)
    for i in range(1, 7):
        input_col_counts = df[f"{input_col}[{i}]"].value_counts()
        scores = input_col_counts.multiply(scoring[i])
        input_col_score = input_col_score.add(scores, fill_value=0)
        input_col_score = input_col_score.sort_values(ascending=False)
        if i == 1:
            ranked_first = df[f"{input_col}[1]"].value_counts()
            ranked_first_clean = pd.DataFrame(
                {
                    "institution": ranked_first.index,
                    "No of times<br>ranked first": ranked_first.values,
                }
            )
    input_col_df = pd.DataFrame(
        {
            "institution": input_col_score.index,
            "score": input_col_score.values,
        }
    )
    input_col_df = input_col_df.merge(
        ranked_first_clean, on="institution", how="left"
    ).fillna(0)
    input_col_df = input_col_df.sort_values(["score", "No of times<br>ranked first"])
    fig = px.bar(
        input_col_df.sort_values(by="score"),
        y="institution",
        x="score",
        color="No of times<br>ranked first",
        color_continuous_scale=[colors[5], colors[2]],
        orientation="h",
    )
    # Update layout
    fig.update_layout(
        autosize=False,
        width=700,
        height=450,
        margin=dict(l=0, r=0, b=100, t=30),
        font={"size": 13, "family": "Roboto Mono, monospace"},
        legend={
            "font": {"size": kwargs.get("legend_font_size", 10)},
        },
        modebar={"orientation": "h"},
    )
    # Add logo
    fig.add_layout_image(
        dict(
            source="{asset_url}/guardint_logo.png",
            xref="paper",
            yref="paper",
            x=1.0,
            y=0.0,
            sizex=0.25,
            sizey=0.25,
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


def print_total(number):
    st.write(f"**{number}** respondents answered the question with the current filter")


def answered_by(group):
    if group == "cso":
        text = "CSO professionals"
    else:
        text = "journalists"
    st.caption(f"This question was only answered by {text}")


chart_config = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["hoverClosestPie"],
    "toImageButtonOptions": {
        "width": 700,
        "height": 450,
        "scale": (210 / 25.4) / (700 / 300),
    },
}

# ===========================================================================
# Import data from stored pickle
# ===========================================================================

df = pd.read_pickle("data/guardint_survey.pkl")

# ===========================================================================
# General configuration
# ===========================================================================

st.set_page_config(
    page_title="GUARDINT Survey Data Explorer",
    page_icon=f"{asset_url}/guardint_favicon.png",
)


def callback():
    st.experimental_set_query_params(section=st.session_state.section)


sections = [
    "Overview",
    "Resources > HR",
    "Resources > Expertise",
    "Resources > Finance",
    "Resources > FOI",
    "Resources > Appreciation",
    "Media Reporting",
    "Public Campaigning",
    "Policy Advocacy",
    "Strategic Litigation",
    "Protection",
    "Constraints",
    "Attitudes",
]

try:
    query_params = st.experimental_get_query_params()
    query_section = query_params["section"][0]
    if "section" not in st.session_state:
        st.session_state.section = query_section

except KeyError:
    st.experimental_set_query_params(section=sections[0])
    query_params = st.experimental_get_query_params()
    query_section = query_params["section"][0]
    if "section" not in st.session_state:
        st.session_state.section = query_section

selected_section = st.sidebar.radio(
    "Choose section",
    sections,
    index=sections.index(query_section),
    key="section",
    on_change=callback,
)

st.caption("GUARD//INT Survey > " + selected_section)

filters = {
    "country": st.sidebar.selectbox(
        "Country", ["All", "United Kingdom", "Germany", "France"]
    ),
    "field": st.sidebar.selectbox("Field", ["All", "CSO Professionals", "Journalists"]),
}

filter = np.full(len(df.index), True)
for column_name, selectbox in filters.items():
    if selectbox == "All":
        continue
    else:
        filter = filter & (df[column_name] == selectbox)

# ===========================================================================
# Custom JS/CSS
# ===========================================================================

# This causes the page to scroll to top when section is changed
components.html(
    f"""
        <!--{st.session_state.section}-->
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    """,
    height=0,
)

# Here, a custom font is loaded from the GitHub repo
css = Template(
    """ <style>
    @font-face {
        font-family: 'Roboto Mono';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url($asset_url/roboto_mono.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    html, body, [class*="css"]  {
        font-family: 'Roboto Mono';
    }
    .st-bx {
        font-family: 'Roboto Mono' !important;
    }
    .st-ae {
        font-family: 'Roboto Mono' !important;
    }
    .css-1rh8hwn {
        font-size: 0.8rem;
    }
    button {
        border-width: 3px 3px 3px 3px !important;
        border-radius: 0 !important;
    }
    h1 {
        margin-top: -1em;
    }
    h3 {line-height: 1.3}
    footer {
        visibility: hidden;
    }
    .e8zbici2 {
        visibility: hidden;
    }
    .custom-footer {
        display: block;
        padding-top: 150px;
        margin-bottom: -400px;
        color: rgba(38, 39, 48, 0.4);
        flex: 0 1 0%;
        font-size: 0.8rem !important;
        max-width: 730px;
        width: 100%;
    }
    strong {
        font-style: bold;
        font-weight: 700;
        color: #000;
    }
    code {
        color: #ff1c1f;
    }
    a {
        color: #ff1c1f !important;
    }
    a:hover {
        color: #ff5557 !important;
    }
    a:visited {
        color: #600b0c !important;
    }
    </style>
    """
)

css = css.substitute({"asset_url": asset_url})
st.markdown(css, unsafe_allow_html=True)

# ===========================================================================
# Overview
# ===========================================================================


if selected_section == "Overview":
    st.write("# Civic Intelligence Oversight Survey Data Explorer")

    st.write(
        """
        A better understanding of the democratic governance of intelligence
        requires more detailed information about an increasingly important group
        of actors outside the traditional corridors of power: Civic intelligence
        oversight practitioners. As part of the GUARD//INT research project, we
        conducted online surveys with representatives of civil society
        organisations (CSOs) and journalists in France, Germany and the United
        Kingdom.

        This site provides open access to the anonymized data we gathered. It visualises
        the first empirical investigation of the perceptions of media and CSO
        professionals specialised in intelligence and surveillance. The data enables us
        to better understand the potential and limitations of civic intelligence
        oversight as an increasingly important part of how democratic societies respond
        to and oversee digital surveillance.
        """
    )

    col1, col2 = st.columns(2)
    col1.metric("Respondents", len(df[filter].index))
    col2.metric(
        "Cumulative years spent working on SBIA",
        int(df[filter]["expertise1"].sum()),
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Avg. years spent working on SBIA†",
        "%.1f" % df[filter]["expertise1"].mean(),
    )
    col2.metric(
        "Avg. No. of FOI requests in the past 5 years",
        int(df[filter]["foi2"].mean()),
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Journalists",
        len(df[filter & (df.field == "Journalists")].index),
    )
    col2.metric(
        "Civil Society Organisation professionals",
        len(df[filter & (df.field == "CSO Professionals")].index),
    )

    st.caption(
        """† For the calculation of the mean only valid numerical answers were
        counted, excluding those who haven't specified their experience in years.
        """
    )

    st.write("## Understanding the data")
    st.write(
        """The individuals we surveyed mostly engage in civic oversight
        practices in their professional capacity and were invited to complete
        the survey based on their experience in working on surveillance by
        intelligence agencies. We designed two different but overlapping
        surveys: One for journalists and one for CSO professionals. When we
        posed a question only to journalists, the question code is prepended
        with `MS` (media scrutiny). When we put the question only to CSO
        professionals, the code is prepended with `CS` (civil society scrutiny).
        If the question was put to both groups, the prefix was removed.
    """
    )
    st.write(
        """The questions and response options are structured in different
        sections ranging from different kinds of resources (human resources,
        expertise, use of freedom of information rights, financial resources,
        journalistic appreciation) to different civic oversight activities
        (media reporting, public campaigning, policy advocacy, strategic
        litigation) as well as protections, constraints and attitudes. A
        comprehensive overview of all questions and answer options can be found
        in our two codebooks:
    """
    )
    with open("codebooks/guardint_survey_codebook_media.pdf", "rb") as file:
        st.download_button(
            label="Codebook Media Scrutiny (PDF)",
            data=file,
            file_name="guardint_survey_codebook_media.pdf",
        )
    with open("codebooks/guardint_survey_codebook_civil_society.pdf", "rb") as file:
        st.download_button(
            label="Codebook Civil Society Scrutiny (PDF)",
            data=file,
            file_name="guardint_survey_codebook_civil_society.pdf",
        )
    st.write(
        """If you want to have a look at the data yourself, you can also
        download the entire dataset that this website is built on
        below:
        """
    )
    with open("data/guardint_survey.csv", "rb") as file:
        st.download_button(
            label="Survey data (CSV)", data=file, file_name="guardint_survey_data.csv"
        )
    with open("data/guardint_survey.xlsx", "rb") as file:
        st.download_button(
            label="Survey data (Excel)",
            data=file,
            file_name="guardint_survey_data.xlsx",
        )

    st.write("## About this website")
    st.write(
        """We initially built this website to give ourselves an easy way to
        peruse and analyse the data. Since we found it helpful, we thought you
        might find it helpful, too. Using the controls located in the sidebar on
        the left you can filter by country  (United Kingdom, France or Germany)
        and by field (Journalists, CSO Professionals). For every question, the
        data explorer indicates the total number of responses according to the
        currently applied filter. By hoovering over the charts, further details
        on the respective answer option appear. All charts can be downloaded as
        .png files.
        """
    )
    st.write(
        """This website would not be remotely possible without the great
        open-source software it's built with. We extend a big thank you to the
        creators of the Streamlit library and all the other software libraries
        that enable the functionality of this website. The code for this website
        is freely available under a permissive license. If you find any errors
        or room for improvement, don't hesitate to let us know.
        """
    )

    st.write("## Get in touch")

    st.write(
        """If you have questions or comments about our research or the data
        provided, you can contact the research team at the [Berlin Social Science
        Center
        (WZB)](https://www.wzb.eu/en/research/digitalization-and-societal-transformation/politics-of-digitalization/projects/oversight-and-intelligence-networks-who-guards-the-guardians-guardint)
        and [Stiftung Neue Verantwortung (SNV)](https://www.stiftung-nv.de/en/project/digital-rights-surveillance-and-democracy) via email to
        [contact@guardint.org](mailto:contact@guardint.org). You can also reach
        out on Twitter [@guard_int](https://twitter.com/guard_int).
        """
    )

    st.write("## Summary statistics")
    st.write(
        """Below you find some summary statistics, such as which countries the
        respondents are primarily working in. You can always jump to a section
        that interests you by using the outline in the left sidebar.
    """
    )
    country_counts = df[filter]["country"].value_counts()
    st.write("### Country `[country]`")
    print_total(country_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=country_counts,
            names=country_counts.index,
            color=country_counts.index,
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write("### Field `[field]`")
    field_counts = df[filter]["field"].value_counts()
    print_total(field_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=field_counts,
            names=field_counts.index,
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write("### Predominant activity of CSO professionals `[CSpreselection]`")
    CSpreselection_counts = df[filter]["CSpreselection"].value_counts()
    print_total(CSpreselection_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=CSpreselection_counts,
            names=CSpreselection_counts.index,
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write("### Gender `[gender]`")
    gender_counts = df[filter]["gender"].value_counts()
    print_total(gender_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=gender_counts,
            names=gender_counts.index,
            color=gender_counts.index,
            color_discrete_map={
                "Not specified": colors[0],
                "Male": colors[1],
                "Female": colors[2],
                "Other": colors[3],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # TODO Privacy notice

# ===========================================================================
# Resources > HR
# ===========================================================================

if selected_section == "Resources > HR":
    st.write("# Resources > HR")

    st.write("### What is your employment status? `[hr1]`")
    hr1_counts = df[filter]["hr1"].value_counts()
    print_total(hr1_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            hr1_counts,
            values=hr1_counts,
            names=hr1_counts.index,
            color=hr1_counts.index,
            color_discrete_map={
                "Full-time": colors[0],
                "Part-time (>50%)": colors[1],
                "Part-time (<50%)": colors[2],
                "Freelance": colors[3],
                "Other": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How many days per month do you work on surveillance by intelligence agencies? `[hr2]`"
    )
    hr2_counts = df[filter]["hr2"].value_counts()
    print_total(hr2_counts.sum())
    st.plotly_chart(
        gen_px_histogram(
            df=df[filter],
            x="hr2",
            y=None,
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"hr2": "days per month"},
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.plotly_chart(
        gen_px_box(
            df=df[filter],
            points="all",
            x="country",
            y="hr2",
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"hr2": "days per month"},
        ),
        use_container_width=True,
        config=chart_config,
    )

    df["hr2_more_than_five"] = np.where(df["hr2"] > 5, True, False)
    df["hr2_more_than_five"] = df["hr2_more_than_five"].replace(
        {True: "more than 5 days", False: "5 days or less"}
    )
    hr2_more_than_five_counts = df[filter]["hr2_more_than_five"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            hr2_more_than_five_counts,
            values=hr2_more_than_five_counts,
            names=hr2_more_than_five_counts.index,
            color=hr2_more_than_five_counts.index,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("### Which type of medium do you work for? `[MShr3]`")
    MShr3_df = pd.DataFrame(columns=("option", "count", "country"))
    answered_by("media")
    MShr3_options = [
        "daily_newspaper",
        "weekly_newspaper",
        "magazine",
        "tv",
        "radio",
        "news_agency",
        "online_stand_alone",
        "online_of_offline",
    ]
    MShr3_options_clean = [
        "Daily newspaper",
        "Weekly newspaper",
        "Magazine",
        "TV",
        "Radio",
        "News agency",
        "Online outlet<br>(standalone)",
        "Online outlet<br>(of an offline publication)",
    ]
    for option, option_clean in zip(MShr3_options, MShr3_options_clean):
        MShr3_data = df[filter]["country"][df[f"MShr3[{option}]"] == 1].tolist()
        for i in MShr3_data:
            MShr3_df = MShr3_df.append(
                {"option": option_clean, "count": MShr3_data.count(i), "country": i},
                ignore_index=True,
            )
    MShr3_df = MShr3_df.drop_duplicates()

    if filters["field"] == "CSO Professionals":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        MShr3_col_list = [col for col in df[filter].columns if col.startswith("MShr3")]
        MShr3_df_total = df[filter][MShr3_col_list]
        MShr3_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(MShr3_df_total.values == True, 1)
        ]
        print_total(MShr3_df_total["answered"].value_counts().sort_index()[1])

    st.plotly_chart(
        gen_px_histogram(
            MShr3_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "United Kingdom": colors[2],
                "France": colors[5],
            },
            labels={"count": "people who work<br>for this medium"},
            marginal=None,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Within the past year, did you have enough time to cover surveillance by intelligence agencies? `[MShr4]`"
    )
    answered_by("media")
    MShr4_counts = df[filter]["MShr4"].value_counts().sort_index()
    print_total(MShr4_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=MShr4_counts.sort_index().index,
            values=MShr4_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Resources > Expertise
# ===========================================================================

if selected_section == "Resources > Expertise":
    st.write("# Resources > Expertise")

    st.write(
        "### How many years have you spent working on surveillance by intelligence agencies? `[expertise1]`"
    )
    expertise1_counts = df[filter]["expertise1"].value_counts()
    print_total(expertise1_counts.sum())
    st.plotly_chart(
        gen_px_histogram(
            df[filter],
            x="expertise1",
            y=None,
            nbins=20,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"expertise1": "years"},
        ),
        use_container_width=True,
        config=chart_config,
    )
    st.plotly_chart(
        gen_px_box(
            df=df[filter],
            points="all",
            x="country",
            y="expertise1",
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"expertise1": "years"},
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How do you assess your level of expertise concerning the **legal** aspects of surveillance by intelligence agencies? `[expertise2]`"
    )
    expertise2_counts = df[filter]["expertise2"].value_counts().sort_index()
    print_total(expertise2_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=expertise2_counts.sort_index().index,
            values=expertise2_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How do you assess your level of expertise concerning the **political** aspects of surveillance by intelligence agencies `[expertise3]`?"
    )
    expertise3_counts = df[filter]["expertise3"].value_counts().sort_index()
    print_total(expertise3_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=expertise3_counts.sort_index().index,
            values=expertise3_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How do you assess your level of expertise concerning the **technical** aspects of surveillance by intelligence agencies? `[expertise4]`"
    )
    expertise4_counts = df[filter]["expertise4"].value_counts().sort_index()
    print_total(expertise4_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=expertise4_counts.sort_index().index,
            values=expertise4_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Resources > Finance
# ===========================================================================

if selected_section == "Resources > Finance":
    st.write("# Resources > Finance")

    st.write(
        "### How do you assess the financial resources that have been available for your work on intelligence over the past 5 years? `[finance1]`"
    )
    finance1_counts = df[filter]["finance1"].value_counts().sort_index()
    print_total(finance1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=finance1_counts.sort_index().index,
            values=finance1_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### If you wanted to conduct investigative research into surveillance by intelligence agencies, could you access extra funding for this research? (For example, a special budget or a stipend) `[MSfinance2]`"
    )
    MSfinance2_counts = df[filter]["MSfinance2"].value_counts()
    answered_by("media")
    print_total(MSfinance2_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSfinance2_counts,
            values=MSfinance2_counts,
            names=MSfinance2_counts.index,
            color=MSfinance2_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[4],
                "I prefer not to say": colors[5],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How important are the following funding categories for your organisation's work on intelligence-related issues? `[CSfinance2]`"
    )
    CSfinance2_options = [
        "private_foundations",
        "donations",
        "national_public_funds",
        "corporate_sponsorship",
        "international_public_funds",
        "other",
    ]
    CSfinance2_options_clean = [
        "Private foundations",
        "Donations",
        "National public funds",
        "Corporate sponsorships",
        "International public funds",
        "Other",
    ]
    CSfinance2_very_important = []
    CSfinance2_somewhat_important = []
    CSfinance2_important = []
    CSfinance2_slightly_important = []
    CSfinance2_not_important = []
    CSfinance2_prefer_not_to_say = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
        "I prefer not to say",
    ]:
        for option in CSfinance2_options:
            try:
                count = df[filter][f"CSfinance2[{option}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                CSfinance2_very_important.append(count)
            elif importance == "Somewhat important":
                CSfinance2_somewhat_important.append(count)
            elif importance == "Important":
                CSfinance2_important.append(count)
            elif importance == "Slightly important":
                CSfinance2_slightly_important.append(count)
            elif importance == "Not important at all":
                CSfinance2_not_important.append(count)
            elif importance == "I prefer not to say":
                CSfinance2_prefer_not_to_say.append(count)
            else:
                continue
    totals = [
        df[filter][f"CSfinance2[{option}]"].value_counts().sum()
        for option in CSfinance2_options
    ]
    answered_by("cso")
    print_total(max(totals))
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Very important",
                    x=CSfinance2_options_clean,
                    y=CSfinance2_very_important,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Somewhat important",
                    x=CSfinance2_options_clean,
                    y=CSfinance2_somewhat_important,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Important",
                    x=CSfinance2_options_clean,
                    y=CSfinance2_important,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Slightly important",
                    x=CSfinance2_options_clean,
                    y=CSfinance2_slightly_important,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not important at all",
                    x=CSfinance2_options_clean,
                    y=CSfinance2_not_important,
                    marker_color=colors[4],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=CSfinance2_options_clean,
                    y=CSfinance2_prefer_not_to_say,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
    )

if selected_section == "Resources > FOI":
    st.write("# Resources > FOI")

    st.write(
        "### Have you requested information under the national FOI† law when you worked on intelligence-related issues over the past 5 years? `[foi1]`"
    )
    st.caption("†Freedom of Information")
    foi1_counts = df[filter]["foi1"].value_counts()
    print_total(foi1_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            foi1_counts,
            values=foi1_counts,
            names=foi1_counts.index,
            color=foi1_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[3],
                "I don't know": colors[4],
                "I prefer not to say": colors[5],
            },
        ),
        use_container_width=True,
    )

    # =======================================================================
    st.write("### How often did you request information? `[foi2]`")
    foi2_counts = df[filter]["foi2"].value_counts()
    print_total(foi2_counts.sum())
    st.plotly_chart(
        gen_px_histogram(
            df[filter],
            x="foi2",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"foi2": "Number of requests"},
        ),
        use_container_width=True,
    )
    st.plotly_chart(
        gen_px_box(
            df=df[filter],
            points="all",
            x="country",
            y="foi2",
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"foi2": "Number of requests"},
        ),
        use_container_width=True,
    )

    # =======================================================================
    st.write(
        "### Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner? `[foi3]`"
    )
    foi3_counts = df[filter]["foi3"].value_counts()
    print_total(foi3_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=foi3_counts.sort_index().index,
            values=foi3_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How helpful have Freedom of Information requests been for your work on intelligence-related issues? `[foi4]`"
    )
    foi4_counts = df[filter]["foi4"].value_counts()
    print_total(foi4_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=foi4_counts.sort_index().index,
            values=foi4_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Why haven’t you requested information under the national FOI law when you reported on intelligence-related issues over the past 5 years? `[foi5]`"
    )
    foi5_df = pd.DataFrame(columns=("option", "count", "country"))
    for option in [
        "not_aware",
        "not_covered",
        "too_expensive",
        "too_time_consuming",
        "afraid_of_data_destruction",
        "afraid_of_discrimination",
        "other",
        "dont_know",
        "prefer_not_to_say",
    ]:
        foi5_data = df[filter]["country"][df[f"foi5[{option}]"] == 1].tolist()
        for i in foi5_data:
            foi5_df = foi5_df.append(
                {"option": option, "count": foi5_data.count(i), "country": i},
                ignore_index=True,
            )
    foi5_df = foi5_df.drop_duplicates()
    foi5_df = foi5_df.replace(
        {
            "not_aware": "I was not aware",
            "not_covered": "The authority was not covered<br>by FOI law",
            "too_expensive": "It seemed to expensive",
            "too_time_consuming": "It seemed to time-consuming",
            "afraid_of_data_destruction": "I was afraid the request<br>could lead to data destruction",
            "other": "Other",
            "prefer_not_to_say": "I prefer not to say",
            "dont_know": "I don't know ",
        }
    )
    print_total(foi5_df["count"].sum())
    st.plotly_chart(
        gen_px_histogram(
            foi5_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            font_size=11,
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"count": "people who answered 'Yes'"},
            marginal=None,
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Resources > Appreciation
# ===========================================================================

if selected_section == "Resources > Appreciation":
    st.write("# Resources > Appreciation")

    st.write(
        "### In the past 5 years, have stories on surveillance by intelligence agencies been nominated for a journalistic award in the country you primarily work in? `[MSapp1]`"
    )
    answered_by("media")
    MSapp1_counts = df[filter]["MSapp1"].value_counts()
    print_total(MSapp1_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSapp1_counts,
            values=MSapp1_counts,
            names=MSapp1_counts.index,
            color=MSapp1_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[4],
                "I prefer not to say": colors[5],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Are there specific awards in the country you primarily work in for reporting on intelligence-related topics? `[MSapp2]`"
    )
    answered_by("media")
    MSapp2_counts = df[filter]["MSapp2"].value_counts()
    print_total(MSapp2_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSapp2_counts,
            values=MSapp2_counts,
            names=MSapp2_counts.index,
            color=MSapp2_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[4],
                "I prefer not to say": colors[5],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Media Reporting
# ===========================================================================

if selected_section == "Media Reporting":
    st.caption(
        "__NB__: All questions in this section have only been presented to Journalists."
    )

    st.write("# Scope of Coverage")

    # =======================================================================
    st.write(
        """### Please estimate: how many journalistic pieces have you produced on intelligence-related topics in the past year? `[MSsoc1]`"""
    )
    answered_by("media")
    MSsoc1_df = df[filter][["country", "MSsoc1"]]
    MSsoc1_df = MSsoc1_df.dropna(subset=["MSsoc1"])
    print_total(MSsoc1_df["MSsoc1"].value_counts().sum())
    st.plotly_chart(
        gen_px_histogram(
            df=MSsoc1_df,
            x="MSsoc1",
            y=None,
            nbins=20,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"MSsoc1": "pieces produced lasy year"},
        ),
        use_container_width=True,
        config=chart_config,
    )
    st.plotly_chart(
        gen_px_box(
            df=df[filter],
            points="all",
            x="country",
            y="MSsoc1",
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"MSsoc1": "pieces produced lasy year"},
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Please estimate: how many of these pieces focused on surveillance by intelligence agencies? `[MSsoc2]`"
    )
    answered_by("media")
    MSsoc2_df = df[filter][["country", "MSsoc2"]]
    MSsoc2_df = MSsoc2_df.dropna(subset=["MSsoc2"])
    print_total(MSsoc2_df["MSsoc2"].value_counts().sum())
    st.plotly_chart(
        gen_px_histogram(
            df=MSsoc2_df,
            x="MSsoc2",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={
                "MSsoc2": "pieces focused on surveillance by intelligence agencies"
            },
        ),
        use_container_width=True,
        config=chart_config,
    )
    st.plotly_chart(
        gen_px_box(
            df=df[filter],
            points="all",
            x="country",
            y="MSsoc2",
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={
                "MSsoc2": "pieces focused on<br>surveillance by intelligence agencies"
            },
        ),
        use_container_width=True,
        config=chart_config,
    )
    MSsoc1_list = df[filter]["MSsoc1"].to_list()
    MSsoc2_list = df[filter]["MSsoc2"].to_list()
    MSsoc1_sum = int(df[filter]["MSsoc1"].sum())
    MSsoc2_sum = int(df[filter]["MSsoc2"].sum())
    try:
        MSsoc12_ratio = MSsoc2_sum / MSsoc1_sum
    except ZeroDivisionError:
        MSsoc12_ratio = 0
    st.write("### Comparison between `[MSsoc1]` and `[MSsoc2]`")

    st.write(
        f"""
Out of a total of __{MSsoc1_sum}__ pieces written on intelligence,
__{MSsoc2_sum}__ or __{MSsoc12_ratio:.1%}__ have foused on surveillance
by intelligence agencies given the current filter.
        """
    )
    df_comp = df[filter][["MSsoc1", "country"]].dropna()
    df_comp["subject"] = "all pieces on <br>intelligence"
    df_comp = df_comp.append(df[filter][["MSsoc2", "country"]].dropna())
    df_comp["subject"] = np.where(
        df_comp["MSsoc2"].notnull(),
        "pieces focused <br>on surveillance <br>by intelligence",
        "all pieces on <br>intelligence",
    )
    df_comp["pieces"] = df_comp.loc[:, ["MSsoc1", "MSsoc2"]].sum(axis=1)

    st.plotly_chart(
        gen_px_box(
            df=df_comp,
            points="all",
            x="subject",
            y="pieces",
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"pieces": "journalistic pieces"},
        ),
        config=chart_config,
        use_container_width=True,
    )

    # =======================================================================
    st.write(
        "### How regularly do you report on surveillance by intelligence agencies? `[MSsoc3]`"
    )
    answered_by("media")
    MSsoc3_counts = df[filter]["MSsoc3"].value_counts()
    print_total(MSsoc3_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=MSsoc3_counts.sort_index().index,
            values=MSsoc3_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### When covering surveillance by intelligence agencies, which topics usually prompt you to write an article? `[MSsoc4]`"
    )
    MSsoc4_df = pd.DataFrame(columns=("option", "count", "country"))
    MSsoc4_options = [
        "follow_up_on_other_media",
        "statements_government",
        "oversight_reports",
        "leaks",
        "own_investigations",
        "dont_know",
        "prefer_not_to_say",
        "other",
    ]
    MSsoc4_options_clean = [
        "Follow-up on other media",
        "Statements by Government",
        "Oversight reports",
        "Leaked material",
        "Own investigations",
        "I don't know",
        "I prefer not to say",
        "Other",
    ]
    answered_by("media")
    if filters["field"] == "CSO Professionals":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        MSsoc4_col_list = [
            col for col in df[filter].columns if col.startswith("MSsoc4")
        ]
        MSsoc4_df_total = df[filter][MSsoc4_col_list]
        MSsoc4_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(MSsoc4_df_total.values == True, 1)
        ]
        print_total(MSsoc4_df_total["answered"].value_counts().sort_index()[1])
    for option, option_clean in zip(MSsoc4_options, MSsoc4_options_clean):
        MSsoc4_data = df[filter]["country"][df[f"MSsoc4[{option}]"] == 1].tolist()
        for i in MSsoc4_data:
            MSsoc4_df = MSsoc4_df.append(
                {"option": option_clean, "count": MSsoc4_data.count(i), "country": i},
                ignore_index=True,
            )
    MSsoc4_df = MSsoc4_df.drop_duplicates()
    st.plotly_chart(
        gen_px_histogram(
            MSsoc4_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"count": "people who answered 'Yes'"},
            marginal=None,
        ),
        use_container_width=True,
    )

    # =======================================================================
    st.write(
        "### When covering surveillance by intelligence agencies, which of the following topics to you report on frequently? `[MSsoc5]`"
    )
    answered_by("media")
    MSsoc5_df = pd.DataFrame(columns=("option", "count", "country"))
    MSsoc5_options = [
        "national_security_risks",
        "intelligence_success",
        "intelligence_misconduct",
        "oversight_interventions",
        "oversight_failures",
        "policy_debates_leg_reforms",
        "other",
    ]
    MSsoc5_options_clean = [
        "National security risks",
        "Successful intelligence<br>operations",
        "Misconduct by intelligence",
        "Oversight interventions",
        "Oversight failures",
        "Policy debates and/or<br>legilsative reform",
        "Other",
    ]
    for option, option_clean in zip(MSsoc5_options, MSsoc5_options_clean):
        MSsoc5_data = df[filter]["country"][df[f"MSsoc5[{option}]"] == 1].tolist()
        for i in MSsoc5_data:
            MSsoc5_df = MSsoc5_df.append(
                {"option": option_clean, "count": MSsoc5_data.count(i), "country": i},
                ignore_index=True,
            )
    if filters["field"] == "CSO Professionals":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        MSsoc5_col_list = [
            col for col in df[filter].columns if col.startswith("MSsoc5")
        ]
        MSsoc5_df_total = df[filter][MSsoc5_col_list]
        MSsoc5_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(MSsoc5_df_total.values == True, 1)
        ]
        print_total(MSsoc5_df_total["answered"].value_counts().sort_index()[1])
    MSsoc5_df = MSsoc5_df.drop_duplicates()
    st.plotly_chart(
        gen_px_histogram(
            MSsoc5_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"count": "people who answered 'Yes'"},
            marginal=None,
        ),
        use_container_width=True,
    )

    # =======================================================================
    st.write("# Transnational Scope")

    st.write(
        "### How often does your work on surveillance by intelligence agencies cover a transnational angle? `[MStrans1]`"
    )

    MStrans1_counts = df[filter]["MStrans1"].value_counts().sort_index()
    answered_by("media")
    print_total(MStrans1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=MStrans1_counts.sort_index().index,
            values=MStrans1_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How often do you collaborate with colleagues covering other countries when working on surveillance by intelligence agencies? `[MStrans2]`"
    )
    MStrans2_counts = df[filter]["MStrans2"].value_counts().sort_index()
    answered_by("media")
    print_total(MStrans2_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=MStrans2_counts.sort_index().index,
            values=MStrans2_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Have those collaborations included an investigative research project with colleagues from abroad? `[MStrans3]`"
    )
    MStrans3_counts = df[filter]["MStrans3"].value_counts()
    answered_by("media")
    print_total(MStrans3_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MStrans3_counts,
            values=MStrans3_counts,
            names=MStrans3_counts.index,
            color=MStrans3_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[4],
                "I prefer not to say": colors[5],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Perceived Impact")

    st.write(
        "### When you think about public responses to your articles on intelligence agencies by readers and colleagues, did you receive any of the following forms of public feedback or engagement? `[MSimpact1]`"
    )

    MSimpact1_df = pd.DataFrame(columns=("option", "count", "country"))
    options = [
        "above_avg_comments",
        "above_avg_shares",
        "above_avg_readers",
        "letters_to_the_editor",
        "follow_up_by_other_media",
        "other",
        "none_of_the_above",
        "dont_know",
        "prefer_not_to_say",
    ]
    options_clean = [
        "An above average number of comments",
        "An above average number of shares",
        "An above average number of readers",
        "Letters to the editor",
        "Follow-up reporting by other media",
        "Other",
        "None of the above",
        "I don't know",
        "I prefer not to say",
    ]
    for option, option_clean in zip(options, options_clean):
        MSimpact1_data = df[filter]["country"][df[f"MSimpact1[{option}]"] == 1].tolist()
        for i in MSimpact1_data:
            MSimpact1_df = MSimpact1_df.append(
                {
                    "option": option_clean,
                    "count": MSimpact1_data.count(i),
                    "country": i,
                },
                ignore_index=True,
            )
    answered_by("media")
    if filters["field"] == "CSO Professionals":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        MSimpact1_col_list = [
            col for col in df[filter].columns if col.startswith("MSimpact1")
        ]
        MSimpact1_df_total = df[filter][MSimpact1_col_list]
        MSimpact1_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(MSimpact1_df_total.values == True, 1)
        ]
        print_total(MSimpact1_df_total["answered"].value_counts().sort_index()[1])
    MSimpact1_df = MSimpact1_df.drop_duplicates()
    st.plotly_chart(
        gen_px_histogram(
            MSimpact1_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"count": "people who answered 'Yes'"},
            marginal=None,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### When you think of responses to your articles on intelligence agencies by administrations or policy makers, did your reporting contribute to any of the following forms of political action? `[MSimpact2]`"
    )

    MSimpact2_df = pd.DataFrame(columns=("option", "count", "country"))
    options = [
        "diplomatic_pressure",
        "civic_action",
        "conversations_with_government",
        "official_inquiries",
        "government_statements",
        "conversations_with_intelligence",
        "dont_know",
        "prefer_not_to_say",
        "other",
    ]
    options_clean = [
        "My reporting led to<br>diplomatic pressure being exercised",
        "My reporting spurred<br>civic action",
        "My reporting led to<br>a conversation with policy makers",
        "My reporting spurred<br>official inquiries",
        "My reporting prompted<br>the government to issue a public statement",
        "My reporting led to<br>a conversation with intelligence practitioners",
        "I don't know",
        "I prefer not to say",
        "Other",
    ]
    for option, option_clean in zip(options, options_clean):
        MSimpact2_data = df[filter]["country"][df[f"MSimpact2[{option}]"] == 1].tolist()
        for i in MSimpact2_data:
            MSimpact2_df = MSimpact2_df.append(
                {
                    "option": option_clean,
                    "count": MSimpact2_data.count(i),
                    "country": i,
                },
                ignore_index=True,
            )
    answered_by("media")
    if filters["field"] == "CSO Professionals":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        MSimpact1_col_list = [
            col for col in df[filter].columns if col.startswith("MSimpact1")
        ]
        MSimpact1_df_total = df[filter][MSimpact1_col_list]
        MSimpact1_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(MSimpact1_df_total.values == True, 1)
        ]
        print_total(MSimpact1_df_total["answered"].value_counts().sort_index()[1])
    MSimpact2_df = MSimpact2_df.drop_duplicates()
    st.plotly_chart(
        gen_px_histogram(
            MSimpact2_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"count": "people who answered 'Yes'"},
            marginal=None,
            font_size=11,
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Public Campaigning
# ===========================================================================

if selected_section == "Public Campaigning":
    st.caption(
        "__NB__: All questions in this section have only been presented to civil society professionals."
    )

    st.write("# Activity")

    st.write(
        "### How important are the following campaigning tools for your work concerning intelligence-related issues? `[CScampact2]`"
    )
    answered_by("cso")
    options = [
        "media_contributions",
        "own_publications",
        "petitions_open_letters",
        "public_events",
        "collaborations",
        "demonstrations",
        "social_media",
        "advertising",
        "volunteer_activities",
        "providing_technical_tools",
        "support_for_eu_campaigns",
        "other",
    ]
    options_clean = [
        "Media contributions",
        "Own publications",
        "Petitions and open letters",
        "Public events",
        "Collaborations with celebrities and influencers",
        "Demonstrations and rallies",
        "Social media communications",
        "Advertising",
        "Volunteer activities",
        "Providing technical tools",
        "Support for campaign activities in other countries",
        "Other",
    ]
    CScampact2_very_important = []
    CScampact2_somewhat_important = []
    CScampact2_important = []
    CScampact2_slightly_important = []
    CScampact2_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for option in options:
            try:
                count = df[filter][f"CScampact2[{option}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                CScampact2_very_important.append(count)
            elif importance == "Somewhat important":
                CScampact2_somewhat_important.append(count)
            elif importance == "Important":
                CScampact2_important.append(count)
            elif importance == "Slightly important":
                CScampact2_slightly_important.append(count)
            elif importance == "Not important at all":
                CScampact2_not_important.append(count)
            else:
                continue

    if filters["field"] == "Journalists":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        CScampact2_col_list = [
            col for col in df[filter].columns if col.startswith("CScampact2")
        ]
        CScampact2_df_total = df[filter][CScampact2_col_list]
        # Make all NaNs numeric zeroes
        CScampact2_df_total = CScampact2_df_total.fillna(0)
        # Now replace everything that is not a number with "Y"
        for col in CScampact2_df_total.columns:
            CScampact2_df_total[col] = (
                pd.to_numeric(CScampact2_df_total[col], errors="coerce")
                .fillna("Y")
                .astype("string")
            )
        # Make a column to count "Y"
        CScampact2_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(CScampact2_df_total.values == "Y", 1)
        ]
        print_total(CScampact2_df_total["answered"].value_counts().sort_index()[1])

    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Very important",
                    x=options_clean,
                    y=CScampact2_very_important,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Somewhat important",
                    x=options_clean,
                    y=CScampact2_somewhat_important,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Important",
                    x=options_clean,
                    y=CScampact2_important,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Slightly important",
                    x=options_clean,
                    y=CScampact2_slightly_important,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not important at all",
                    x=options_clean,
                    y=CScampact2_not_important,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Transnational Scope")

    st.write(
        "### How frequently do your public campaigns address transnational issues of surveillance by intelligence agencies? `[CScamptrans1]`"
    )
    answered_by("cso")
    CScamptrans1_counts = df[filter]["CScamptrans1"].value_counts()
    print_total(CScamptrans1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CScamptrans1_counts.sort_index().index,
            values=CScamptrans1_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### When conducting public campaigns on surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? `[CScamptrans2]`"
    )
    answered_by("cso")
    CScamptrans2_counts = df[filter]["CScamptrans2"].value_counts()
    print_total(CScamptrans2_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CScamptrans2_counts.sort_index().index,
            values=CScamptrans2_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Perceived Impact")

    st.write(
        "### How much do you agree with the following statements concerning the effectiveness of your campaigning activities regarding intelligence-related issues over the past 5 years? `[CScampimpact1]`"
    )
    answered_by("cso")
    options = [
        "increased_awareness",
        "policies_reflect_demands",
        "created_media_attention",
        "achieved_goals",
    ]
    options_clean = [
        "Helped increase public awareness",
        "Our demands have been reflected in politics",
        "Created media attention",
        "Achieved defined goals",
    ]
    CScampimpact1_agree_completely = []
    CScampimpact1_agree_to_great_extent = []
    CScampimpact1_agree_somewhat = []
    CScampimpact1_agree_slightly = []
    CScampimpact1_not_agree_at_all = []
    for agreement in [
        "Agree completely",
        "Agree to a great extent",
        "Agree somewhat",
        "Agree slightly",
        "Not agree at all",
    ]:
        for option in options:
            try:
                count = df[filter][f"CScampimpact1[{option}]"].value_counts()[agreement]
            except KeyError:
                count = 0
            if agreement == "Agree completely":
                CScampimpact1_agree_completely.append(count)
            elif agreement == "Agree to a great extent":
                CScampimpact1_agree_to_great_extent.append(count)
            elif agreement == "Agree somewhat":
                CScampimpact1_agree_somewhat.append(count)
            elif agreement == "Agree slightly":
                CScampimpact1_agree_slightly.append(count)
            elif agreement == "Not agree at all":
                CScampimpact1_not_agree_at_all.append(count)
            else:
                continue
    if filters["field"] == "Journalists":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        CScampimpact1_col_list = [
            col for col in df[filter].columns if col.startswith("CScampimpact1")
        ]
        CScampimpact1_df_total = df[filter][CScampimpact1_col_list]
        # Make all NaNs numeric zeroes
        CScampimpact1_df_total = CScampimpact1_df_total.fillna(0)
        # Now replace everything that is not a number with "Y"
        for col in CScampimpact1_df_total.columns:
            CScampimpact1_df_total[col] = (
                pd.to_numeric(CScampimpact1_df_total[col], errors="coerce")
                .fillna("Y")
                .astype("string")
            )
        # Make a column to count "Y"
        CScampimpact1_df_total["answered"] = [
            "Y" if x > 0 else "N"
            for x in np.sum(CScampimpact1_df_total.values == "Y", 1)
        ]
        print_total(CScampimpact1_df_total["answered"].value_counts().sort_index()[1])
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Agree completely",
                    x=options_clean,
                    y=CScampimpact1_agree_completely,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Agree to a great extent",
                    x=options_clean,
                    y=CScampimpact1_agree_to_great_extent,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Agree somewhat",
                    x=options_clean,
                    y=CScampimpact1_agree_somewhat,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Agree slightly",
                    x=options_clean,
                    y=CScampimpact1_agree_slightly,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not agree at all",
                    x=options_clean,
                    y=CScampimpact1_not_agree_at_all,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Policy Advocacy
# ===========================================================================

if selected_section == "Policy Advocacy":
    st.caption(
        "__NB__: All questions in this section have only been presented to civil society organisation professionals."
    )
    st.write("# Activity")

    st.write(
        "### How important are the following policy advocacy tools for your work on intelligence-related issues? `[CSadvocact2]`"
    )
    answered_by("cso")
    options = [
        "research",
        "consultations",
        "briefings",
        "expert_events",
        "participation_in_fora",
        "legal_opinions",
        "informal_encounters",
        "other",
    ]
    options_clean = [
        "Research & analysis",
        "Contributing to consultations",
        "Briefing of policy makers",
        "Expert events",
        "Participation in fora or bodies",
        "Legal opinions",
        "Informal encounters",
        "Other",
    ]
    CSadvocact2_very_important = []
    CSadvocact2_somewhat_important = []
    CSadvocact2_important = []
    CSadvocact2_slightly_important = []
    CSadvocact2_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for option in options:
            try:
                count = df[filter][f"CSadvocact2[{option}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                CSadvocact2_very_important.append(count)
            elif importance == "Somewhat important":
                CSadvocact2_somewhat_important.append(count)
            elif importance == "Important":
                CSadvocact2_important.append(count)
            elif importance == "Slightly important":
                CSadvocact2_slightly_important.append(count)
            elif importance == "Not important at all":
                CSadvocact2_not_important.append(count)
            else:
                continue
    try:
        # If one respondent chose at least one medium it counts towards the total
        CSadvocact2_col_list = [
            col for col in df[filter].columns if col.startswith("CSadvocact2")
        ]
        CSadvocact2_df_total = df[filter][CSadvocact2_col_list]
        # Make all NaNs numeric zeroes
        CSadvocact2_df_total = CSadvocact2_df_total.fillna(0)
        # Now replace everything that is not a number with "Y"
        for col in CSadvocact2_df_total.columns:
            CSadvocact2_df_total[col] = (
                pd.to_numeric(CSadvocact2_df_total[col], errors="coerce")
                .fillna("Y")
                .astype("string")
            )
        # Make a column to count "Y"
        CSadvocact2_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(CSadvocact2_df_total.values == "Y", 1)
        ]
        print_total(CSadvocact2_df_total["answered"].value_counts().sort_index()[1])
    except IndexError:
        print_total(0)
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Very important",
                    x=options_clean,
                    y=CSadvocact2_very_important,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Somewhat important",
                    x=options_clean,
                    y=CSadvocact2_somewhat_important,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Important",
                    x=options_clean,
                    y=CSadvocact2_important,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Slightly important",
                    x=options_clean,
                    y=CSadvocact2_slightly_important,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not important at all",
                    x=options_clean,
                    y=CSadvocact2_not_important,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Transnational Scope")

    st.write(
        "### How frequently does your policy advocacy address transnational issues of surveillance by intelligence agencies? `[CSadvoctrans1]`"
    )
    answered_by("cso")
    CSadvoctrans1_counts = df[filter]["CSadvoctrans1"].value_counts()
    print_total(CSadvoctrans1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CSadvoctrans1_counts.sort_index().index,
            values=CSadvoctrans1_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### When performing policy advocacy concerning surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? `[CSadvoctrans2]`"
    )
    answered_by("cso")
    CSadvoctrans2_counts = df[filter]["CSadvoctrans2"].value_counts()
    print_total(CSadvoctrans2_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CSadvoctrans2_counts.sort_index().index,
            values=CSadvoctrans2_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Perceived Impact")

    st.write(
        "### How much do you agree with the following statements concerning the effectiveness of your advocacy activities regarding intelligence-related issues over the past 5 years? `[CSadvocimpact1]`"
    )
    options = [
        "increased_awareness",
        "policies_reflect_recommendations",
        "more_informed_debates",
        "achieved_goals",
    ]
    options_clean = [
        "Helped increase public awareness",
        "Our policy recommendations have been reflected in politics",
        "Contributed to more informed debate",
        "Achieved defined goals",
    ]
    CSadvocimpact1_agree_completely = []
    CSadvocimpact1_agree_to_great_extent = []
    CSadvocimpact1_agree_somewhat = []
    CSadvocimpact1_agree_slightly = []
    CSadvocimpact1_not_agree_at_all = []
    for agreement in [
        "Agree completely",
        "Agree to a great extent",
        "Agree somewhat",
        "Agree slightly",
        "Not agree at all",
    ]:
        for option in options:
            try:
                count = df[filter][f"CSadvocimpact1[{option}]"].value_counts()[
                    agreement
                ]
            except KeyError:
                count = 0
            if agreement == "Agree completely":
                CSadvocimpact1_agree_completely.append(count)
            elif agreement == "Agree to a great extent":
                CSadvocimpact1_agree_to_great_extent.append(count)
            elif agreement == "Agree somewhat":
                CSadvocimpact1_agree_somewhat.append(count)
            elif agreement == "Agree slightly":
                CSadvocimpact1_agree_slightly.append(count)
            elif agreement == "Not agree at all":
                CSadvocimpact1_not_agree_at_all.append(count)
            else:
                continue
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Agree completely",
                    x=options_clean,
                    y=CSadvocimpact1_agree_completely,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Agree to a great extent",
                    x=options_clean,
                    y=CSadvocimpact1_agree_to_great_extent,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Agree somewhat",
                    x=options_clean,
                    y=CSadvocimpact1_agree_somewhat,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Agree slightly",
                    x=options_clean,
                    y=CSadvocimpact1_agree_slightly,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not agree at all",
                    x=options_clean,
                    y=CSadvocimpact1_not_agree_at_all,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Strategic Litigation
# ===========================================================================

if selected_section == "Strategic Litigation":
    st.caption(
        "__NB__: All questions in this section have only been presented to civil society organisation professionals."
    )
    st.write("# Activity")

    st.write(
        "### How important are the following policy litigateacy tools for your work on intelligence-related issues? `[CSlitigateact2]`"
    )
    answered_by("cso")
    options = [
        "initiating_lawsuit",
        "initiating_complaint",
        "supporting_existing_legislation",
        "other",
    ]
    options_clean = [
        "Initiating and/or coordinating a lawsuit",
        "Initiating a legal complaint",
        "Supporting existing legislation",
        "Other",
    ]
    CSlitigateact2_very_important = []
    CSlitigateact2_somewhat_important = []
    CSlitigateact2_important = []
    CSlitigateact2_slightly_important = []
    CSlitigateact2_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for option in options:
            try:
                count = df[filter][f"CSlitigateact2[{option}]"].value_counts()[
                    importance
                ]
            except KeyError:
                count = 0
            if importance == "Very important":
                CSlitigateact2_very_important.append(count)
            elif importance == "Somewhat important":
                CSlitigateact2_somewhat_important.append(count)
            elif importance == "Important":
                CSlitigateact2_important.append(count)
            elif importance == "Slightly important":
                CSlitigateact2_slightly_important.append(count)
            elif importance == "Not important at all":
                CSlitigateact2_not_important.append(count)
            else:
                continue
    try:
        # If one respondent chose at least one medium it counts towards the total
        CSlitigateact2_col_list = [
            col for col in df[filter].columns if col.startswith("CSlitigateact2")
        ]
        CSlitigateact2_df_total = df[filter][CSlitigateact2_col_list]
        # Make all NaNs numeric zeroes
        CSlitigateact2_df_total = CSlitigateact2_df_total.fillna(0)
        # Now replace everything that is not a number with "Y"
        for col in CSlitigateact2_df_total.columns:
            CSlitigateact2_df_total[col] = (
                pd.to_numeric(CSlitigateact2_df_total[col], errors="coerce")
                .fillna("Y")
                .astype("string")
            )
        # Make a column to count "Y"
        CSlitigateact2_df_total["answered"] = [
            "Y" if x > 0 else "N"
            for x in np.sum(CSlitigateact2_df_total.values == "Y", 1)
        ]
        print_total(CSlitigateact2_df_total["answered"].value_counts().sort_index()[1])
    except IndexError:
        print_total(0)

    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Very important",
                    x=options_clean,
                    y=CSlitigateact2_very_important,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Somewhat important",
                    x=options_clean,
                    y=CSlitigateact2_somewhat_important,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Important",
                    x=options_clean,
                    y=CSlitigateact2_important,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Slightly important",
                    x=options_clean,
                    y=CSlitigateact2_slightly_important,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not important at all",
                    x=options_clean,
                    y=CSlitigateact2_not_important,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Costs")

    st.write(
        "### How frequently did the costs (e.g. court fees, loser pays principles, lawyers fees) prevent your organisation from starting a strategic litigation process? `[CSlitigatecost1]`"
    )
    answered_by("cso")
    CSlitigatecost1_counts = df[filter]["CSlitigatecost1"].value_counts().sort_index()
    print_total(CSlitigatecost1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CSlitigatecost1_counts.sort_index().index,
            values=CSlitigatecost1_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How frequently did your organisation benefit from pro bono support? `[CSlitigatecost2]`"
    )
    answered_by("cso")
    CSlitigatecost2_counts = df[filter]["CSlitigatecost2"].value_counts()
    print_total(CSlitigatecost2_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CSlitigatecost2_counts.sort_index().index,
            values=CSlitigatecost2_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Imagine your organisation lost a strategic litigation case concerning surveillance by intelligence agencies. How financially risky would it be for the organisation to be defeated in court? `[CSlitigatecost3]`"
    )
    answered_by("cso")
    CSlitigatecost3_counts = df[filter]["CSlitigatecost3"].value_counts()
    print_total(CSlitigatecost3_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CSlitigatecost3_counts.sort_index().index,
            values=CSlitigatecost3_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Transnational Scope")

    st.write(
        "### How frequently do your strategic litigation cases address transnational issues of surveillance by intelligence agencies? `[CSlitigatetrans1]`"
    )
    answered_by("cso")
    CSlitigatetrans1_counts = df[filter]["CSlitigatetrans1"].value_counts()
    print_total(CSlitigatetrans1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CSlitigatetrans1_counts.sort_index().index,
            values=CSlitigatetrans1_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### When performing strategic litigation concerning surveillance by intelligence agencies, how often do you collaborate with civil society actors in other countries? `[CSlitigatetrans2]`"
    )
    answered_by("cso")
    CSlitigatetrans2_counts = df[filter]["CSlitigatetrans2"].value_counts()
    print_total(CSlitigatetrans2_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=CSlitigatetrans2_counts.sort_index().index,
            values=CSlitigatetrans2_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Perceived Impact")

    st.write(
        "### How much do you agree with the following statements concerning the effectiveness of your strategic litigation activities regarding surveillance by intelligence agencies over the past 5 years? `[CSlitigateimpact1]`"
    )
    answered_by("cso")
    options = [
        "increased_awareness",
        "changed_the_law",
        "amendments_of_the_law",
        "revealed_new_information",
        "achieved_goals",
    ]
    options_clean = [
        "Helped increase public awareness",
        "Changed the prevalent case law",
        "Led to amendments in legislation",
        "Revealed new information",
        "Achieved defined goals",
    ]
    CSlitigateimpact1_agree_completely = []
    CSlitigateimpact1_agree_to_great_extent = []
    CSlitigateimpact1_agree_somewhat = []
    CSlitigateimpact1_agree_slightly = []
    CSlitigateimpact1_not_agree_at_all = []
    for agreement in [
        "Agree completely",
        "Agree to a great extent",
        "Agree somewhat",
        "Agree slightly",
        "Not agree at all",
    ]:
        for option in options:
            try:
                count = df[filter][f"CSlitigateimpact1[{option}]"].value_counts()[
                    agreement
                ]
            except KeyError:
                count = 0
            if agreement == "Agree completely":
                CSlitigateimpact1_agree_completely.append(count)
            elif agreement == "Agree to a great extent":
                CSlitigateimpact1_agree_to_great_extent.append(count)
            elif agreement == "Agree somewhat":
                CSlitigateimpact1_agree_somewhat.append(count)
            elif agreement == "Agree slightly":
                CSlitigateimpact1_agree_slightly.append(count)
            elif agreement == "Not agree at all":
                CSlitigateimpact1_not_agree_at_all.append(count)
            else:
                continue
    try:
        # If one respondent chose at least one medium it counts towards the total
        CSlitigateimpact1_col_list = [
            col for col in df[filter].columns if col.startswith("CSlitigateimpact1")
        ]
        CSlitigateimpact1_df_total = df[filter][CSlitigateimpact1_col_list]
        # Make all NaNs numeric zeroes
        CSlitigateimpact1_df_total = CSlitigateimpact1_df_total.fillna(0)
        # Now replace everything that is not a number with "Y"
        for col in CSlitigateimpact1_df_total.columns:
            CSlitigateimpact1_df_total[col] = (
                pd.to_numeric(CSlitigateimpact1_df_total[col], errors="coerce")
                .fillna("Y")
                .astype("string")
            )
        # Make a column to count "Y"
        CSlitigateimpact1_df_total["answered"] = [
            "Y" if x > 0 else "N"
            for x in np.sum(CSlitigateimpact1_df_total.values == "Y", 1)
        ]
        print_total(
            CSlitigateimpact1_df_total["answered"].value_counts().sort_index()[1]
        )
    except IndexError:
        print_total(0)

    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Agree completely",
                    x=options_clean,
                    y=CSlitigateimpact1_agree_completely,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Agree to a great extent",
                    x=options_clean,
                    y=CSlitigateimpact1_agree_to_great_extent,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Agree somewhat",
                    x=options_clean,
                    y=CSlitigateimpact1_agree_somewhat,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Agree slightly",
                    x=options_clean,
                    y=CSlitigateimpact1_agree_slightly,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not agree at all",
                    x=options_clean,
                    y=CSlitigateimpact1_not_agree_at_all,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Protection
# ===========================================================================

if selected_section == "Protection":
    st.write("## Operational Protection")

    st.write(
        "### Have you taken any of the following measures to protect your datas from attacks and surveillance? `[protectops1]`"
    )
    options_clean = [
        "Participation in<br>digital security training",
        "Use of E2E encrypted<br>communication channels",
    ]

    protectops1_yes = []
    protectops1_no = []
    protectops1_dont_know = []
    protectops1_prefer_not_to_say = []
    for answer in [
        "Yes",
        "No",
        "I don't know",
        "I prefer not to say",
    ]:
        for option in ["sectraining", "e2e"]:
            try:
                count = df[filter][f"protectops1[{option}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                protectops1_yes.append(count)
            elif answer == "No":
                protectops1_no.append(count)
            elif answer == "I don't know":
                protectops1_dont_know.append(count)
            elif answer == "I prefer not to say":
                protectops1_prefer_not_to_say.append(count)
            else:
                continue
    totals = [
        df[filter]["protectops1[sectraining]"].value_counts().sum(),
        df[filter]["protectops1[e2e]"].value_counts().sum(),
    ]
    print_total(max(totals))
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Yes",
                    x=options_clean,
                    y=protectops1_yes,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="No",
                    x=options_clean,
                    y=protectops1_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=options_clean,
                    y=protectops1_dont_know,
                    marker_color=colors[4],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=options_clean,
                    y=protectops1_prefer_not_to_say,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Were any of these measures provided by your employer? `[protectops2]`"
    )
    protectops2_counts = df[filter]["protectops2"].value_counts()
    print_total(protectops2_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=protectops2_counts,
            names=protectops2_counts.index,
            color=protectops2_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I prefer not to say": colors[5],
                "I don't know": colors[4],
            },
            legend_orientation="v",
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### How important is the use of the following technical tools for you to protect your communications, your online activities and the data you handle? `[protectops3]`"
    )
    protectops3_options = [
        "Encrypted Email",
        "VPN",
        "Tor",
        "E2E Messengers",
        "Encrpyted hardware",
        "Two-Factor authentication",
        "Secure Drop †",
        "Other",
    ]

    protectops3_very_important = []
    protectops3_somewhat_important = []
    protectops3_important = []
    protectops3_slightly_important = []
    protectops3_not_important = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
    ]:
        for option in [
            "encrypted_email",
            "vpn",
            "tor",
            "e2e_chat",
            "encrypted_hardware",
            "2fa",
            "secure_drop",
            "other",
        ]:
            try:
                count = df[filter][f"protectops3[{option}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                protectops3_very_important.append(count)
            elif importance == "Somewhat important":
                protectops3_somewhat_important.append(count)
            elif importance == "Important":
                protectops3_important.append(count)
            elif importance == "Slightly important":
                protectops3_slightly_important.append(count)
            elif importance == "Not important at all":
                protectops3_not_important.append(count)
            else:
                continue
    totals = [
        df[filter]["protectops3[encrypted_email]"].value_counts().sum(),
        df[filter]["protectops3[vpn]"].value_counts().sum(),
        df[filter]["protectops3[tor]"].value_counts().sum(),
        df[filter]["protectops3[e2e_chat]"].value_counts().sum(),
        df[filter]["protectops3[encrypted_hardware]"].value_counts().sum(),
        df[filter]["protectops3[2fa]"].value_counts().sum(),
        df[filter]["protectops3[other]"].value_counts().sum(),
    ]
    print_total(max(totals))
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Very important",
                    x=protectops3_options,
                    y=protectops3_very_important,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Somewhat important",
                    x=protectops3_options,
                    y=protectops3_somewhat_important,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Important",
                    x=protectops3_options,
                    y=protectops3_important,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Slightly important",
                    x=protectops3_options,
                    y=protectops3_slightly_important,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not important at all",
                    x=protectops3_options,
                    y=protectops3_not_important,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
    )
    st.caption("† The option'Secure Drop' was only available to Journalists")

    # =======================================================================
    st.write(
        "### Which of the following statements best describes your level of confidence in the protection offered by technological tools? `[protectops4]`"
    )
    protectops4_counts = df[filter]["protectops4"].value_counts()
    print_total(protectops4_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=protectops4_counts.sort_index().index,
            values=protectops4_counts.sort_index().values,
            height=600,
            font_size=13,
            legend_font_size=11,
            legend_x=-1.0,
            legend_y=2.0,
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Legal Protection")

    st.write(
        """### When working on intelligence-related issues, do you feel you have reason to be concerned about... `[protectleg1]`

- surveillance of your activities (CSO professionals)
- regarding the protection of your sources (Journalists)"""
    )

    protectleg1_counts = df[filter]["protectleg1"].value_counts()
    print_total(protectleg1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=protectleg1_counts.sort_index().index,
            values=protectleg1_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write(
        "### Do you regard the existing legal protections against surveillance of your activities in your country as a sufficient safeguard for your work on intelligence-related issues? `[protectleg2]`"
    )

    protectleg2_counts = df[filter]["protectleg2"].value_counts()
    print_total(protectleg2_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            protectleg2_counts,
            values=protectleg2_counts,
            names=protectleg2_counts.index,
            color_discrete_sequence=colors,
            color=protectleg2_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Are any of the following forms of institutional support readily available to you? `[protectleg3]`"
    )
    protectleg3_options = ["Free legal counsel", "Legal cost insurance", "Other"]
    protectleg3_yes = []
    protectleg3_no = []
    protectleg3_dont_know = []
    protectleg3_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for option in ["free_counsel", "cost_insurance", "other"]:
            try:
                count = df[filter][f"protectleg3[{option}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                protectleg3_yes.append(count)
            elif answer == "No":
                protectleg3_no.append(count)
            elif answer == "I don't know":
                protectleg3_dont_know.append(count)
            elif answer == "I prefer not to say":
                protectleg3_prefer_not_to_say.append(count)
            else:
                continue
    try:
        # If one respondent chose at least one medium it counts towards the total
        protectleg3_col_list = [
            col for col in df[filter].columns if col.startswith("protectleg3")
        ]
        protectleg3_df_total = df[filter][protectleg3_col_list]
        # Make all NaNs numeric zeroes
        protectleg3_df_total = protectleg3_df_total.fillna(0)
        # Now replace everything that is not a number with "Y"
        for col in protectleg3_df_total.columns:
            protectleg3_df_total[col] = (
                pd.to_numeric(protectleg3_df_total[col], errors="coerce")
                .fillna("Y")
                .astype("string")
            )
        # Make a column to count "Y"
        protectleg3_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(protectleg3_df_total.values == "Y", 1)
        ]
        print_total(protectleg3_df_total["answered"].value_counts().sort_index()[1])
    except IndexError:
        print_total(0)
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Yes",
                    x=protectleg3_options,
                    y=protectleg3_yes,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="No",
                    x=protectleg3_options,
                    y=protectleg3_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=protectleg3_options,
                    y=protectleg3_dont_know,
                    marker_color=colors[5],
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=protectleg3_options,
                    y=protectleg3_prefer_not_to_say,
                    marker_color=colors[4],
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    # =======================================================================
    st.write("# Rights to Access")

    st.write(
        "### As a journalist in the country you primarily work in, do you have a special right to know if you have been subjected to surveillance in the past? `[MSprotectrta1]`"
    )
    answered_by("media")
    MSprotectrta1_counts = df[filter]["MSprotectrta1"].value_counts()
    print_total(MSprotectrta1_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSprotectrta1_counts,
            values=MSprotectrta1_counts,
            names=MSprotectrta1_counts.index,
            color=MSprotectrta1_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("### Have you ever made use of this right? `[MSprotectrta2]`")
    answered_by("media")
    MSprotectrta2_counts = df[filter]["MSprotectrta2"].value_counts()
    print_total(MSprotectrta2_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSprotectrta2_counts,
            values=MSprotectrta2_counts,
            names=MSprotectrta2_counts.index,
            color=MSprotectrta2_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Is this right available to all journalists, even non-citizens? `[MSprotectrta3]`"
    )
    answered_by("media")
    MSprotectrta3_counts = df[filter]["MSprotectrta3"].value_counts()
    print_total(MSprotectrta3_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSprotectrta3_counts,
            values=MSprotectrta3_counts,
            names=MSprotectrta3_counts.index,
            color=MSprotectrta3_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Have you ever submitted a data subject access request (based on your right to access as defined in the GDPR) related to surveillance by intelligence agencies? `[MSprotectrta4]`"
    )
    answered_by("media")
    MSprotectrta4_counts = df[filter]["MSprotectrta4"].value_counts()
    print_total(MSprotectrta4_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSprotectrta4_counts,
            values=MSprotectrta4_counts,
            names=MSprotectrta4_counts.index,
            color=MSprotectrta4_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Over the past 5 years, have you received responses to your data subject access request(s) in a timely manner? `[MSprotectrta5]`"
    )
    answered_by("media")
    MSprotectrta5_counts = df[filter]["MSprotectrta5"].value_counts()
    print_total(MSprotectrta5_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSprotectrta5_counts,
            values=MSprotectrta5_counts,
            names=MSprotectrta5_counts.index,
            color=MSprotectrta5_counts.index,
            color_discrete_map={
                "Never": colors[0],
                "No, usually longer than 30 days": colors[1],
                "Yes, within 30 days": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### If you received a response to a data subject access request, was the information provided helpful? `[MSprotectrta6]`"
    )
    answered_by("media")
    MSprotectrta6_counts = df[filter]["MSprotectrta6"].value_counts()
    print_total(MSprotectrta6_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSprotectrta6_counts,
            values=MSprotectrta6_counts,
            names=MSprotectrta6_counts.index,
            color=MSprotectrta6_counts.index,
            color_discrete_map={
                "Yes, the information provided was helpful": colors[2],
                "Partly, the information provided was somewhat <br>helpful but contained omissions": colors[
                    1
                ],
                "No, the information provided was not at all helpful": colors[0],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Constraints
# ===========================================================================

if selected_section == "Constraints":

    st.write("# Censorship")

    st.write(
        "### When covering intelligence related issues, have you consulted state bodies or officials prior to the publication of the story due to the sensitivity of information? `[MSconstraintcen1]`"
    )
    answered_by("media")
    MSconstraintcen1_counts = df[filter]["MSconstraintcen1"].value_counts()
    print_total(MSconstraintcen1_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSconstraintcen1_counts,
            values=MSconstraintcen1_counts,
            names=MSconstraintcen1_counts.index,
            color=MSconstraintcen1_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Is there an institutional setting that advises journalists to engage in a consultation process prior to the publication of sensitive information (i.e. a code of conduct or a committee)? `[MSconstraintcen2]`"
    )
    answered_by("media")
    MSconstraintcen2_counts = df[filter]["MSconstraintcen2"].value_counts()
    print_total(MSconstraintcen2_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSconstraintcen2_counts,
            values=MSconstraintcen2_counts,
            names=MSconstraintcen2_counts.index,
            color=MSconstraintcen2_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Please estimate: How often have you consulted state bodies or officials prior to publishing  intelligence-related stories in the past 5 years? `[MSconstraintcen3]`"
    )
    answered_by("media")
    MSconstraintcen3_df = df[filter][["country", "MSconstraintcen3"]]
    MSconstraintcen3_df = MSconstraintcen3_df.dropna(subset=["MSconstraintcen3"])
    print_total(MSconstraintcen3_df["MSconstraintcen3"].value_counts().sum())
    st.plotly_chart(
        gen_px_histogram(
            df=df[filter],
            x="MSconstraintcen3",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "France": colors[2],
                "United Kingdom": colors[5],
            },
            labels={"MSconstraintcen3": "times"},
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Has this consultation process prevented a publication of yours from appearing? `[MSconstraintcen4]`"
    )
    answered_by("media")
    MSconstraintcen4_counts = df[filter]["MSconstraintcen4"].value_counts()
    print_total(MSconstraintcen4_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSconstraintcen4_counts,
            values=MSconstraintcen4_counts,
            names=MSconstraintcen4_counts.index,
            color=MSconstraintcen4_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write(
        "### Have you been required to make edits as part of this consultation process? `[MSconstraintcen5]`"
    )
    answered_by("media")
    MSconstraintcen5_counts = df[filter]["MSconstraintcen5"].value_counts()
    print_total(MSconstraintcen5_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            MSconstraintcen5_counts,
            values=MSconstraintcen5_counts,
            names=MSconstraintcen5_counts.index,
            color=MSconstraintcen5_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
                "I don't know": colors[5],
                "I prefer not to say": colors[4],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Interference")

    st.write(
        "### Has your institution or have you yourself been subjected to surveillance by intelligence agencies in the past five years? `[constraintinter1]`"
    )

    constraintinter1_counts = df[filter]["constraintinter1"].value_counts()
    print_total(constraintinter1_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=constraintinter1_counts,
            names=constraintinter1_counts.index,
            color=constraintinter1_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes, I have evidence": colors[2],
                "Yes, I suspect": colors[3],
                "I don't know": colors[4],
                "I prefer not to say": colors[5],
            },
            legend_orientation="v",
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you been threatened with prosecution or have you actually been prosecuted for your work on intelligence-related issues?"
    )

    constraintinter2_counts = df[filter]["constraintinter2"].value_counts().sort_index()
    print_total(constraintinter2_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=constraintinter2_counts,
            names=constraintinter2_counts.index,
            color=constraintinter2_counts.index,
            color_discrete_map={
                "No": colors[0],
                "Yes": colors[2],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write("### What was the outcome?")

    constraintinter3_counts = df[filter]["constraintinter3"].value_counts()
    print_total(constraintinter3_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=constraintinter3_counts,
            names=constraintinter3_counts.index,
            color_discrete_sequence=colors,
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you experienced any of the following interferences by public authorities in relation to your work on intelligence related topics?"
    )
    constraintinter4_yes = []
    constraintinter4_no = []
    constraintinter4_dont_know = []
    constraintinter4_prefer_not_to_say = []
    constraintinter4_options = [
        "police_search",
        "seizure",
        "extortion",
        "violent_threat",
        "inspection_during_travel",
        "detention",
        "surveillance_signalling",
        "online_harassment",
        "entry_on_deny_lists",
        "exclusion_from_events",
        "public_defamation",
    ]
    constraintinter4_options_clean = [
        "Police searches",
        "Seizure of material",
        "Extortion",
        "Violent threats",
        "Special inspections during travels",
        "Detention",
        "Surveillance signalling",
        "Online harassment",
        "Entry on deny lists",
        "Exclusion from events",
        "Public defamation",
    ]
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for option in constraintinter4_options:
            try:
                count = df[filter][f"constraintinter4[{option}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                constraintinter4_yes.append(count)
            elif answer == "No":
                constraintinter4_no.append(count)
            elif answer == "I don't know":
                constraintinter4_dont_know.append(count)
            elif answer == "I prefer not to say":
                constraintinter4_prefer_not_to_say.append(count)
            else:
                continue
    totals = [
        df[filter][f"constraintinter4[{option}]"].value_counts().sum()
        for option in constraintinter4_options
    ]
    print_total(max(totals))
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Yes",
                    x=constraintinter4_options_clean,
                    y=constraintinter4_yes,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="No",
                    x=constraintinter4_options_clean,
                    y=constraintinter4_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=constraintinter4_options_clean,
                    y=constraintinter4_dont_know,
                    marker_color=colors[4],
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=constraintinter4_options_clean,
                    y=constraintinter4_prefer_not_to_say,
                    marker_color=colors[5],
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write(
        "### In the past 5 years, have you been approached by intelligence officials and received..."
    )
    constraintinter5_options = ["unsolicited_information", "invitations", "other"]
    constraintinter5_options_clean = [
        "Unsolicited information",
        "Invitations to off-the-record<br>events or meetings",
        "Other",
    ]
    constraintinter5_yes = []
    constraintinter5_no = []
    constraintinter5_dont_know = []
    constraintinter5_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for option in constraintinter5_options:
            try:
                count = df[filter][f"constraintinter5[{option}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                constraintinter5_yes.append(count)
            elif answer == "No":
                constraintinter5_no.append(count)
            elif answer == "I don't know":
                constraintinter5_dont_know.append(count)
            elif answer == "I prefer not to say":
                constraintinter5_prefer_not_to_say.append(count)
            else:
                continue
    totals = [
        df[filter][f"constraintinter5[{option}]"].value_counts().sum()
        for option in constraintinter5_options
    ]
    print_total(max(totals))
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Yes",
                    x=constraintinter5_options_clean,
                    y=constraintinter5_yes,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="No",
                    x=constraintinter5_options_clean,
                    y=constraintinter5_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=constraintinter5_options_clean,
                    y=constraintinter5_dont_know,
                    marker_color=colors[4],
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=constraintinter5_options_clean,
                    y=constraintinter5_prefer_not_to_say,
                    marker_color=colors[5],
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write(
        "### When working on intelligence-related issues have you ever experienced harassment by security agencies or politicians due to your..."
    )
    constraintinter6_options = [
        "gender",
        "ethnicity",
        "political",
        "sexual",
        "religious",
        "other",
    ]
    constraintinter6_options_clean = [
        "Gender",
        "Ethnicity",
        "Political orientation",
        "Sexual orientation",
        "Religious affiliation",
        "Other",
    ]
    constraintinter6_yes = []
    constraintinter6_no = []
    constraintinter6_dont_know = []
    constraintinter6_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for option in constraintinter6_options:
            try:
                count = df[filter][f"constraintinter6[{option}]"].value_counts()[answer]
            except KeyError:
                count = 0
            if answer == "Yes":
                constraintinter6_yes.append(count)
            elif answer == "No":
                constraintinter6_no.append(count)
            elif answer == "I don't know":
                constraintinter6_dont_know.append(count)
            elif answer == "I prefer not to say":
                constraintinter6_prefer_not_to_say.append(count)
            else:
                continue
    totals = [
        df[filter][f"constraintinter6[{option}]"].value_counts().sum()
        for option in constraintinter6_options
    ]
    print_total(max(totals))
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Yes",
                    x=constraintinter6_options_clean,
                    y=constraintinter6_yes,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="No",
                    x=constraintinter6_options_clean,
                    y=constraintinter6_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=constraintinter6_options_clean,
                    y=constraintinter6_dont_know,
                    marker_color=colors[4],
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=constraintinter6_options_clean,
                    y=constraintinter6_prefer_not_to_say,
                    marker_color=colors[5],
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

    # =======================================================================
    st.write("# Self Censorship")
    st.write(
        "### Which of the following behaviours have you experienced or observed in your professional environment related to covering intelligence-related topics? `[MSconstraintself1]`"
    )
    answered_by("media")
    options = [
        "avoid",
        "change_focus",
        "change_timeline",
        "abandon",
        "leave_profession",
        "other",
    ]
    options_clean = [
        "Avoided sensitive issues in<br>a story related to intelligence",
        "Changed the focus of a story<br>related to intelligence",
        "Changed the timeline for publication",
        "Abandoned a story related to<br>intelligence",
        "Considered leaving the profession<br>altogether",
        "Other",
    ]
    MSconstraintself1_yes = []
    MSconstraintself1_no = []
    MSconstraintself1_dont_know = []
    MSconstraintself1_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for option in options:
            try:
                count = df[filter][f"MSconstraintself1[{option}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                MSconstraintself1_yes.append(count)
            elif answer == "No":
                MSconstraintself1_no.append(count)
            elif answer == "I don't know":
                MSconstraintself1_dont_know.append(count)
            elif answer == "I prefer not to say":
                MSconstraintself1_prefer_not_to_say.append(count)
            else:
                continue
    try:
        # If one respondent chose at least one medium it counts towards the total
        MSconstraintself1_col_list = [
            col for col in df[filter].columns if col.startswith("MSconstraintself1")
        ]
        MSconstraintself1_df_total = df[filter][MSconstraintself1_col_list]
        # Make all NaNs numeric zeroes
        MSconstraintself1_df_total = MSconstraintself1_df_total.fillna(0)
        # Now replace everything that is not a number with "Y"
        for col in MSconstraintself1_df_total.columns:
            MSconstraintself1_df_total[col] = (
                pd.to_numeric(MSconstraintself1_df_total[col], errors="coerce")
                .fillna("Y")
                .astype("string")
            )
        # Make a column to count "Y"
        MSconstraintself1_df_total["answered"] = [
            "Y" if x > 0 else "N"
            for x in np.sum(MSconstraintself1_df_total.values == "Y", 1)
        ]
        print_total(
            MSconstraintself1_df_total["answered"].value_counts().sort_index()[1]
        )
    except IndexError:
        print_total(0)
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Yes",
                    x=options_clean,
                    y=MSconstraintself1_yes,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="No",
                    x=options_clean,
                    y=MSconstraintself1_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=options_clean,
                    y=MSconstraintself1_dont_know,
                    marker_color=colors[5],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=options_clean,
                    y=MSconstraintself1_prefer_not_to_say,
                    marker_color=colors[4],
                ),
            ],
        ),
        use_container_width=True,
        confif=chart_config,
    )

    # =======================================================================
    st.write(
        "### Which of the following behaviours have you experienced or observed in your professional environment related to your work on intelligence-related topics? `[CSconstraintself1]`"
    )
    options = [
        "avoid",
        "cancelled_campaign",
        "withdrew_litigation",
        "leave_profession",
        "other",
    ]
    options_clean = [
        "Avoided advocating for<br>contentious policy changes",
        "Canceled a public campaign",
        "Withdrew litigation case",
        "Quit working on<br>intelligence-related issues",
        "Other",
    ]
    CSconstraintself1_yes = []
    CSconstraintself1_no = []
    CSconstraintself1_dont_know = []
    CSconstraintself1_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for option in options:
            try:
                count = df[filter][f"CSconstraintself1[{option}]"].value_counts()[
                    answer
                ]
            except KeyError:
                count = 0
            if answer == "Yes":
                CSconstraintself1_yes.append(count)
            elif answer == "No":
                CSconstraintself1_no.append(count)
            elif answer == "I don't know":
                CSconstraintself1_dont_know.append(count)
            elif answer == "I prefer not to say":
                CSconstraintself1_prefer_not_to_say.append(count)
            else:
                continue
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Yes",
                    x=options_clean,
                    y=CSconstraintself1_yes,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="No",
                    x=options_clean,
                    y=CSconstraintself1_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=options_clean,
                    y=CSconstraintself1_dont_know,
                    marker_color=colors[5],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=options_clean,
                    y=CSconstraintself1_prefer_not_to_say,
                    marker_color=colors[4],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Attitudes
# ===========================================================================

if selected_section == "Attitudes":
    st.write("# Attitudes")

    st.write(
        "### The following four statements are about **intelligence agencies**. Please select the statement you most agree with, based on your national context."
    )
    attitude1_counts = df[filter]["attitude1"].value_counts().sort_index()
    print_total(attitude1_counts.sum())
    st.plotly_chart(
        gen_go_pie(
            labels=attitude1_counts.sort_index().index,
            values=attitude1_counts.sort_index().values,
            height=600,
            font_size=13,
            legend_font_size=11,
            legend_x=-0.75,
            legend_y=1.5,
            image_sizex=0.25,
            image_sizey=0.25,
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write(
        "### The following four statements are about **intelligence oversight**. Please select the statement you most agree with, based on your national context."
    )
    attitude2_counts = df[filter]["attitude2"].value_counts().sort_index()
    attitude2_counts[
        "A1: Intelligence oversight generally succeeds<br>in uncovering past misconduct and preventing<br>future misconduct"
    ] = 0
    st.plotly_chart(
        gen_go_pie(
            labels=attitude2_counts.sort_index().index,
            values=attitude2_counts.sort_index().values,
            height=600,
            font_size=13,
            legend_font_size=11,
            legend_x=-0.75,
            legend_y=1.5,
            image_sizex=0.25,
            image_sizey=0.25,
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write(
        "### In your personal view, what are the goals of intelligence oversight? Please select the three goals of oversight you subscribe to the most. `[attitude3]`"
    )
    attitude3_options = [
        "rule_of_law",
        "civil_liberties",
        "effectiveness_of_intel",
        "legitimacy_of_intel",
        "trust_in_intel",
        "critique_of_intel",
        "prefer_not_to_say",
    ]
    attitude3_df = pd.DataFrame(columns=("option", "count", "country"))
    for option in attitude3_options:
        attitude3_data = df[filter]["country"][df[f"attitude3[{option}]"] == 1].tolist()
        for i in attitude3_data:
            attitude3_df = attitude3_df.append(
                {"option": option, "count": attitude3_data.count(i), "country": i},
                ignore_index=True,
            )
    attitude3_df = attitude3_df.drop_duplicates()
    attitude3_df = attitude3_df.replace(
        {
            "rule_of_law": "Rule of law",
            "civil_liberties": "Civil liberties",
            "effectiveness_of_intel": "Effectiveness of intelligence agencies",
            "legitimacy_of_intel": "Legitimacy of intelligence agencies",
            "trust_in_intel": "Trust in intelligence agencies",
            "critique_of_intel": "Critique of intelligence agencies",
            "prefer_not_to_say": "I prefer not to say",
        }
    )
    st.plotly_chart(
        gen_px_histogram(
            df=attitude3_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "United Kingdom": colors[2],
                "France": colors[5],
            },
            labels={"count": "people who answered 'Yes'"},
        ),
        use_container_width=True,
        config=chart_config,
    )

    scoring = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
    bodies = [
        "Parliamentary oversight bodies",
        "Judicial oversight bodies",
        "Independent expert bodies",
        "Data protection authorities",
        "Audit courts",
        "CSOs | The media",
    ]

    st.write(
        "### Which of the following actors do you trust the most to **enable public debate** on surveillance by intelligence agencies? `[attitude4]`"
    )
    st.plotly_chart(
        gen_rank_plt("attitude4", bodies), use_container_width=True, config=chart_config
    )

    st.write(
        "### Which of the following actors do you trust the most to **contest surveillance** by intelligence agencies?"
    )
    st.plotly_chart(
        gen_rank_plt("attitude5", bodies), use_container_width=True, config=chart_config
    )

    st.write(
        "### Which of the following actors do you trust the most to **enforce compliance** regarding surveillance by intelligence agencies?"
    )
    st.plotly_chart(
        gen_rank_plt("attitude6", bodies), use_container_width=True, config=chart_config
    )

# ===========================================================================
# Footer
# ===========================================================================

st.markdown(
    """
    <div class="custom-footer">Developed by the
        <a href="https://guardint.org" target="_blank">GUARDINT Project</a>
    with funding by the Deutsche Forschungsgesellschaft (DFG, German Research Foundation) <a href="https://gepris.dfg.de/gepris/projekt/396819157?contrast=0&findButton=historyCall&hitsPerPage=25&index=95005&language=en&nurProjekteMitAB=false&orderBy=name&teilprojekte=true" target="_blank">
    Project Number 396819157</a>
    </div>
""",
    unsafe_allow_html=True,
)
