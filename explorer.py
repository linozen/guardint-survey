import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# ===========================================================================
# GUARDINT color scheme
# ===========================================================================


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
# Functions to be cached
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
            source="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_logo.png",
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
            source="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_logo.png",
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
            source="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_logo.png",
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
            source="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_logo.png",
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
            source="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_logo.png",
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
            source="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_logo.png",
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


chart_config = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["hoverClosestPie"],
    "toImageButtonOptions": {
        "width": 700,
        "height": 450,
        "scale": (210 / 25.4) / (700 / 300),
    },
}


def print_total(number):
    st.write(f"**{number}** respondents answered the question with the current filter")


def answered_by(group):
    if group == "cso":
        text = "CSO professionals"
    else:
        text = "media professionals"
    st.caption(f"This question was only answered by {text}")


# ===========================================================================
# Import data from stored pickle
# ===========================================================================

df = pd.read_pickle("data/merged.pkl")

# ===========================================================================
# General configuration
# ===========================================================================

st.set_page_config(
    page_title="IOI Survey Data Explorer",
    page_icon="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_favicon.png",
)


def callback():
    st.experimental_set_query_params(section=st.session_state.section)


sections = [
    "Overview",
    "Resources",
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

st.caption(
    "__" + selected_section + "__ | Civil Society Organisation and Media professionals"
)

filters = {
    "country": st.sidebar.selectbox(
        "Country", ["All", "United Kingdom", "Germany", "France"]
    ),
    "field": st.sidebar.selectbox(
        "Field", ["All", "CSO Professionals", "Media Professionals"]
    ),
}

filter = np.full(len(df.index), True)
for column_name, selectbox in filters.items():
    if selectbox == "All":
        continue
    else:
        filter = filter & (df[column_name] == selectbox)

###############################################################################
# Custom JS/CSS
###############################################################################

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
st.markdown(
    """ <style>
    @font-face {
        font-family: 'Roboto Mono';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://raw.githubusercontent.com/snv-berlin/ioi/master/roboto_mono.woff2) format('woff2');
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

    h3 {line-height: 1.3}

    footer {visibility: hidden;}
    .e8zbici2 {visibility: hidden;}

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
    """,
    unsafe_allow_html=True,
)


# ===========================================================================
# Overview
# ===========================================================================


if selected_section == "Overview":
    st.write("# Overview")

    # TODO Add correct links
    st.write(
        """
        This is the _merged_ data containing the responses to the questions
        from both the Civil Society Scrutiny questionnaire and the Media
        Scrutiny questionnaire. Since only some questions were asked in both
        questionnaires, this _merged_ data represents a subset of all the
        questions that were asked in both surveys individually.

        To see all answers given by members of civil society organisations,
        click [here](https://ioi.civsoc.sehn.dev). To see all answers given
        by members of media organisations, click
        [here](https://ioi.media.sehn.dev). Use the sidebar on the left to
        choose the section of the survey that is relevant for you and use
        the drop-down menus to filter by country or survey type.

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
        "Media professionals",
        len(df[filter & (df.field == "Media Professionals")].index),
    )
    col2.metric(
        "Civil Society Organisation professionals",
        len(df[filter & (df.field == "CSO Professionals")].index),
    )

    st.caption(
        """†For the calculation of the mean, only valid numerical answers were
        counted. This is why the number might differ from the number one gets
        when simply dividing e.g. the cumulative years spent working on SBIA
        by the overall number of respondents (including those who haven't
        specified their experience in years).
        """
    )

    st.write("## Open Data")
    st.write(
        """We cleaned and anonymised the data so you can take look at it yourself.
        Using the buttons below, you can download the entire dataset. If you want
        to find out how this page was created, you can take a look at the code on
        [Github](https://github.com/snv-berlin/ioi).
    """
    )
    with open("data/merged.csv", "rb") as file:
        st.download_button(
            label="Download data as CSV",
            data=file,
            file_name="GUARDINT_survey_data_merged.csv",
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
                "United Kingdom": colors[2],
                "France": colors[5],
            },
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write("### Field [`field`]")
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
# Resources
# ===========================================================================


if selected_section == "Resources":
    st.write("# Resources")

    st.write("## Human Resources")

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

    st.write("### Which type of medium do you work for? `[hr3ms]`")
    hr3ms_df = pd.DataFrame(columns=("option", "count", "country"))
    answered_by("media")
    hr3ms_options = [
        "daily_newspaper",
        "weekly_newspaper",
        "magazine",
        "tv",
        "radio",
        "news_agency",
        "online_stand_alone",
        "online_of_offline",
    ]
    hr3ms_options_clean = [
        "Daily newspaper",
        "Weekly newspaper",
        "Magazine",
        "TV",
        "Radio",
        "News agency",
        "Online outlet<br>(standalone)",
        "Online outlet<br>(of an offline publication)",
    ]
    for option, option_clean in zip(hr3ms_options, hr3ms_options_clean):
        hr3ms_data = df[filter]["country"][df[f"hr3ms[{option}]"] == 1].tolist()
        for i in hr3ms_data:
            hr3ms_df = hr3ms_df.append(
                {"option": option_clean, "count": hr3ms_data.count(i), "country": i},
                ignore_index=True,
            )
    hr3ms_df = hr3ms_df.drop_duplicates()

    if filters["field"] == "CSO Professionals":
        print_total(0)
    else:
        # If one respondent chose at least one medium it counts towards the total
        hr3ms_col_list = [col for col in df[filter].columns if col.startswith("hr3ms")]
        hr3ms_df_total = df[filter][hr3ms_col_list]
        hr3ms_df_total["answered"] = [
            "Y" if x > 0 else "N" for x in np.sum(hr3ms_df_total.values == True, 1)
        ]
        print_total(hr3ms_df_total["answered"].value_counts().sort_index()[1])

    st.plotly_chart(
        gen_px_histogram(
            hr3ms_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": colors[0],
                "United Kingdom": colors[2],
                "France": colors[4],
            },
            labels={"count": "people who work<br>for this medium"},
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write(
        "### Within the past year, did you have enough time to cover surveillance by intelligence agencies? `[hr4ms]`"
    )
    answered_by("media")
    hr4ms_counts = df[filter]["hr4ms"].value_counts().sort_index()
    st.plotly_chart(
        gen_go_pie(
            labels=hr4ms_counts.sort_index().index,
            values=hr4ms_counts.sort_index().values,
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write("## Expertise")

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

    st.write("## Financial Resources")

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

    st.write(
        "### If you wanted to conduct investigative research into surveillance by intelligence agencies, could you access extra funding for this research? (For example, a special budget or a stipend) `[finance2ms]`"
    )
    finance2ms_counts = df[filter]["finance2ms"].value_counts()
    answered_by("media")
    print_total(finance2ms_counts.sum())
    st.plotly_chart(
        gen_px_pie(
            finance2ms_counts,
            values=finance2ms_counts,
            names=finance2ms_counts.index,
            color=finance2ms_counts.index,
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

    st.write(
        "### How important are the following funding categories for your organisation's work on intelligence-related issues? `[finance2cs]`"
    )
    finance2cs_options = [
        "private_foundations",
        "donations",
        "national_public_funds",
        "corporate_sponsorship",
        "international_public_funds",
        "other",
    ]
    finance2cs_options_clean = [
        "Private foundations",
        "Donations",
        "National public funds",
        "Corporate sponsorships",
        "International public funds",
        "Other",
    ]
    finance2cs_very_important = []
    finance2cs_somewhat_important = []
    finance2cs_important = []
    finance2cs_slightly_important = []
    finance2cs_not_important = []
    finance2cs_prefer_not_to_say = []
    for importance in [
        "Very important",
        "Somewhat important",
        "Important",
        "Slightly important",
        "Not important at all",
        "I prefer not to say",
    ]:
        for option in finance2cs_options:
            try:
                count = df[filter][f"finance2cs[{option}]"].value_counts()[importance]
            except KeyError:
                count = 0
            if importance == "Very important":
                finance2cs_very_important.append(count)
            elif importance == "Somewhat important":
                finance2cs_somewhat_important.append(count)
            elif importance == "Important":
                finance2cs_important.append(count)
            elif importance == "Slightly important":
                finance2cs_slightly_important.append(count)
            elif importance == "Not important at all":
                finance2cs_not_important.append(count)
            elif importance == "I prefer not to say":
                finance2cs_prefer_not_to_say.append(count)
            else:
                continue
    totals = [
        df[filter][f"finance2cs[{option}]"].value_counts().sum()
        for option in finance2cs_options
    ]
    answered_by("cso")
    print_total(max(totals))
    st.plotly_chart(
        gen_go_bar_stack(
            data=[
                go.Bar(
                    name="Very important",
                    x=finance2cs_options_clean,
                    y=finance2cs_very_important,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="Somewhat important",
                    x=finance2cs_options_clean,
                    y=finance2cs_somewhat_important,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="Important",
                    x=finance2cs_options_clean,
                    y=finance2cs_important,
                    marker_color=colors[2],
                ),
                go.Bar(
                    name="Slightly important",
                    x=finance2cs_options_clean,
                    y=finance2cs_slightly_important,
                    marker_color=colors[3],
                ),
                go.Bar(
                    name="Not important at all",
                    x=finance2cs_options_clean,
                    y=finance2cs_not_important,
                    marker_color=colors[4],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=finance2cs_options_clean,
                    y=finance2cs_prefer_not_to_say,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
    )
    st.write("## Freedom of Information")

    st.write(
        "### Have you requested information under the national FOI law when you worked on intelligence-related issues over the past 5 years?"
    )
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

    st.write("### How often did you request information?")
    foi2_counts = df[filter]["foi3"].value_counts()
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

    st.write(
        "### Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner?"
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

    st.write(
        "### How helpful have Freedom of Information requests been for your work on intelligence-related issues?"
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

    st.write(
        "### Why haven’t you requested information under the national FOI law when you reported on intelligence-related issues over the past 5 years?"
    )
    foi5_df = pd.DataFrame(columns=("option", "count", "country"))
    # TODO Map proper labels
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
        ),
        use_container_width=True,
        config=chart_config,
    )

# ===========================================================================
# Protection
# ===========================================================================

if selected_section == "Protection":
    st.write("# Protection")

    st.write("## Operational Protection")

    st.write(
        "### Have you taken any of the following measures to protect your datas from attacks and surveillance?"
    )
    protectops1_options = [
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
                    x=protectops1_options,
                    y=protectops1_yes,
                    marker_color=colors[1],
                ),
                go.Bar(
                    name="No",
                    x=protectops1_options,
                    y=protectops1_no,
                    marker_color=colors[0],
                ),
                go.Bar(
                    name="I don't know",
                    x=protectops1_options,
                    y=protectops1_dont_know,
                    marker_color=colors[4],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=protectops1_options,
                    y=protectops1_prefer_not_to_say,
                    marker_color=colors[5],
                ),
            ],
        ),
        use_container_width=True,
        config=chart_config,
    )

    st.write("### Were any of these measures provided by your employer?")
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

    st.write(
        "### How important is the use of the following technical tools for you to protect your communications, your online activities and the data you handle?"
    )
    protectops3_options = [
        "Encrypted Email",
        "VPN",
        "Tor",
        "E2E Messengers",
        "Encrpyted hardware",
        "Two-Factor authentication",
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

    st.write(
        "### Which of the following statements best describes your level of confidence in the protection offered by technological tools?"
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

    st.write("## Legal Protection")

    st.write(
        """### When working on intelligence-related issues, do you feel you have reason to be concerned about...

- surveillance of your activities (CSO professionals)
- regarding the protection of your sources (media professionals)"""
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
        "### Are any of the following forms of institutional support readily available to you?"
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

# ===========================================================================
# Constraints
# ===========================================================================

if selected_section == "Constraints":
    st.write("# Constraints")

    st.write("## Interference by state authorities")

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
    print(attitude2_counts)
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
    <div class="custom-footer">Developed with
        <a href="https://streamlit.io" target="_blank">Streamlit</a>
        and ❤ by the
        <a href="https://guardint.org" target="_blank">GUARDINT Project</a>
    </div>
""",
    unsafe_allow_html=True,
)
