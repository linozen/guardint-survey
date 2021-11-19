import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

from lib.figures import (
    generate_histogram,
    generate_overlaid_histogram,
    generate_stacked_bar_chart,
    generate_ranking_plot,
)

from lib.download import (
    get_csv_download_link,
    get_excel_download_link,
)


###############################################################################
# Helper functions
###############################################################################

colors = [
    "#600b0c",
    "#C01518",
    "#ff1c1f",
    "#ff5557",
    "#ff8e8f",
    "#ffc7c7",
    "#ffe3e3",
    "#ffffff",
]


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
        textinfo="percent+value",
        hovertemplate="""<b>Answer</b> %{label}
<br><br>given by <b>%{value}</b> respondents or <b>%{percent}</b>
<br>of all who answered the question
<br>given the current filter setup.
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
            "orientation": "h",
            "bgcolor": "#efefef",
            "x": -0.2,
            "y": 1.1,
        },
        modebar={"orientation": "v"},
    )
    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/snv-berlin/ioi/master/guardint_logo.png?token=AI3WJCDZHU4NDLOGH2VJFNDBS7SQG",
            xref="paper",
            yref="paper",
            x=1,
            y=1.00,
            sizex=0.20,
            sizey=0.20,
            xanchor="right",
            yanchor="bottom",
        )
    )
    return fig


px_pie_config = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["hoverClosestPie"],
    "toImageButtonOptions": {
        "width": 700,
        "height": 450,
        "scale": (210 / 25.4) / (700 / 300),
    },
}


@st.cache
def gen_px_box(df, x, y, points, color, color_discrete_map):
    fig = px.box(
        df,
        x=x,
        y=y,
        points=points,
        color=color,
        color_discrete_map=color_discrete_map,
    )
    return fig


@st.cache
def render_histogram(df, x, y, nbins, color, color_discrete_map, labels):
    return generate_histogram(df, x, y, nbins, color, color_discrete_map, labels)


@st.cache
def render_overlaid_histogram(traces):
    return generate_overlaid_histogram(traces)


@st.cache
def render_stacked_bar_chart(data):
    return generate_stacked_bar_chart(data)


@st.cache
def render_ranking_plot(input_col):
    return generate_ranking_plot(df[filter], input_col, bodies, scoring)


@st.cache
def read_markdown_file(file):
    return Path(file).read_text()


@st.cache
def get_corr_matrix(df):
    df = pd.read_pickle("./data/merged_corr.pkl")
    fig = px.imshow(df, zmin=0, zmax=1, color_continuous_scale="viridis", height=1300)
    return fig


@st.cache
def get_significance_matrix(df):
    df = pd.read_pickle("./data/merged_sig.pkl")
    fig = px.imshow(df, zmin=-5, zmax=5, color_continuous_scale="viridis", height=1300)
    return fig


# ===========================================================================
# Import data
# ===========================================================================

df = pd.read_pickle("data/merged.pkl")

# ===========================================================================
# General configuration
# ===========================================================================

st.set_page_config(
    page_title="IOI Survey Data Explorer",
)


def callback():
    st.experimental_set_query_params(section=st.session_state.section)


sections = [
    "Overview",
    "Resources",
    "Protection",
    "Constraints",
    "Attitudes",
    "Appendix",
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
    "__"
    + selected_section
    + "__ | Civil Society Organisation and Media representatives"
)

filters = {
    "surveytype": st.sidebar.selectbox(
        "Survey type", ["All", "Civil Society Scrutiny", "Media Scrutiny"]
    ),
    "country": st.sidebar.selectbox(
        "Country", ["All", "United Kingdom", "Germany", "France"]
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

st.markdown(
    """ <style>
    @font-face {
        font-family: 'Roboto Mono';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/robotomono/v13/L0xuDF4xlVMF-BfR8bXMIhJHg45mwgGEFl0_3vq_ROW4.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }

    html, body, [class*="css"]  {
    font-family: 'Roboto Mono';

    }
    .st-bx,input {
        font-family: 'Roboto Mono' !important;
    }

    .css-1rh8hwn {
        font-size: 0.8rem;
    }

    h3 {line-height: 1.3}

    </style> """,
    unsafe_allow_html=True,
)

###############################################################################
# Display dynamic charts
###############################################################################


if selected_section == "Overview":
    st.write("# Overview")

    merged_markdown = read_markdown_file("explorer/markdown/merged.md")
    st.markdown(merged_markdown, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Respondents", len(df[filter].index))
    col2.metric(
        "Cumulative years spent working on SBIA",
        int(df[filter]["expertise1"].sum()),
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Average years spent working on SBIA†",
        "%.1f" % df[filter]["expertise1"].mean(),
    )
    col2.metric(
        "Avg. No. of FOI requests in the past 5 years",
        int(df[filter]["foi2"].mean()),
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Media representatives",
        len(df[filter & (df.surveytype == "Media Scrutiny")].index),
    )
    col2.metric(
        "Civil Society representatives",
        len(df[filter & (df.surveytype == "Civil Society Scrutiny")].index),
    )

    st.caption(
        "†For the calculation of the mean, only valid numerical answers were counted. This is why the number might differ from the number one gets when simply dividing e.g. the cumulative years spent working on SBIA by the overall number of respondents (including those who haven't specified their experience in years)."
    )

    country_counts = df[filter]["country"].value_counts()
    st.write("### Country")
    country_total = country_counts.sum()
    st.write(
        f"_**{country_total}** respondents in total answered the question with the current filter._"
    )
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
        config=px_pie_config,
    )

    st.write("### Field")
    surveytype_counts = df[filter]["surveytype"].value_counts()
    surveytype_total = surveytype_counts.sum()
    st.write(
        f"_**{surveytype_total}** respondents in total answered the question with the current filter._"
    )
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=surveytype_counts,
            names=surveytype_counts.index,
        ),
        use_container_width=True,
        config=px_pie_config,
    )

    st.write("### Gender")
    gender_counts = df[filter]["gender"].value_counts()
    gender_total = gender_counts.sum()
    st.write(
        f"_**{gender_total}** respondents in total answered the question with the current filter._"
    )
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
        config=px_pie_config,
    )

if selected_section == "Resources":
    st.write("# Resources")

    st.write("## Human Resources")

    st.write("### What is your employment status `[hr1]`")
    hr1_counts = df[filter]["hr1"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            hr1_counts,
            values=hr1_counts,
            names=hr1_counts.index,
            color=hr1_counts.index,
            color_discrete_map={
                "Full-time": px.colors.qualitative.Prism[0],
                "Part-time (>50%)": px.colors.qualitative.Prism[1],
                "Part-time (<50%)": px.colors.qualitative.Prism[2],
                "Freelance": px.colors.qualitative.Prism[4],
                "Other": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How many days per month do you work on surveillance by intelligence agencies? `[hr2]`"
    )
    st.plotly_chart(
        render_histogram(
            df=df[filter],
            x="hr2",
            y=None,
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"hr2": "days per month"},
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        gen_px_box(
            df=df[filter],
            points="all",
            x="country",
            y="hr2",
            color="country",
            color_discrete_map={
                "Germany": colors[5],
                "France": colors[1],
                "United Kingdom": colors[7],
            },
        ),
        use_container_width=True,
    )

    df["hr2_more_than_five"] = np.where(df["hr2"] > 5, True, False)
    df["hr2_more_than_five"] = df["hr2_more_than_five"].replace(
        {True: ">5 days", False: "5 days or less"}
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
    )

    st.write("## Expertise")

    st.write(
        "### How many years have you spent working on surveillance by intelligence agencies? `[expertise1]`"
    )
    st.plotly_chart(
        render_histogram(
            df[filter],
            x="expertise1",
            y=None,
            nbins=20,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"expertise1": "years"},
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        gen_px_box(
            df=df[filter],
            points="all",
            x="country",
            y="expertise1",
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How do you assess your level of expertise concerning the **legal** aspects of surveillance by intelligence agencies? For example, knowledge of intelligence law, case law. `[expertise2]`"
    )
    expertise2_counts = df[filter]["expertise2"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=expertise2_counts,
            names=expertise2_counts.index,
            color_discrete_sequence=None,
            color=expertise2_counts.index,
            color_discrete_map={
                "Expert knowledge": px.colors.qualitative.Prism[9],
                "Advanced knowledge": px.colors.qualitative.Prism[8],
                "Some knowledge": px.colors.qualitative.Prism[7],
                "Basic knowledge": px.colors.qualitative.Prism[6],
                "No knowledge": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How do you assess your level of expertise concerning the **political** aspects of surveillance by intelligence agencies?` [expertise3]`"
    )
    expertise3_counts = df[filter]["expertise3"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=expertise3_counts,
            names=expertise3_counts.index,
            color_discrete_sequence=None,
            color=expertise3_counts.index,
            color_discrete_map={
                "Expert knowledge": px.colors.qualitative.Prism[9],
                "Advanced knowledge": px.colors.qualitative.Prism[8],
                "Some knowledge": px.colors.qualitative.Prism[7],
                "Basic knowledge": px.colors.qualitative.Prism[6],
                "No knowledge": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How do you assess your level of expertise concerning the **technical** aspects of surveillance by intelligence agencies?` [expertise4]`"
    )
    expertise4_counts = df[filter]["expertise4"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=expertise4_counts,
            names=expertise4_counts.index,
            color_discrete_sequence=None,
            color=expertise4_counts.index,
            color_discrete_map={
                "Expert knowledge": px.colors.qualitative.Prism[9],
                "Advanced knowledge": px.colors.qualitative.Prism[8],
                "Some knowledge": px.colors.qualitative.Prism[7],
                "Basic knowledge": px.colors.qualitative.Prism[6],
                "No knowledge": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("## Financial Resources")

    st.write(
        "### How do you assess the financial resources that have been available for your work on intelligence over the past 5 years? `[finance1]`"
    )
    finance1_counts = df[filter]["finance1"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=finance1_counts,
            names=finance1_counts.index,
            color_discrete_sequence=None,
            color=finance1_counts.index,
            color_discrete_map={
                "A great deal of funding": px.colors.qualitative.Prism[9],
                "Sufficient funding": px.colors.qualitative.Prism[8],
                "Some funding": px.colors.qualitative.Prism[7],
                "Little funding": px.colors.qualitative.Prism[6],
                "No funding": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        )
    )

    st.write("## Freedom of Information")

    st.write(
        "### Have you requested information under the national FOI law when you worked on intelligence-related issues over the past 5 years? `[foi1]`"
    )
    foi1_counts = df[filter]["foi1"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            foi1_counts,
            values=foi1_counts,
            names=foi1_counts.index,
            color=foi1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("### How often did you request information? `[foi2]`")
    st.plotly_chart(
        render_histogram(
            df[filter],
            x="foi2",
            y=None,
            nbins=10,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
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
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Over the past 5 years, did you receive a response to your FOI request(s) in a timely manner? `[foi3]`"
    )
    foi3_counts = df[filter]["foi3"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            foi3_counts,
            values=foi3_counts,
            names=foi3_counts.index,
            color=foi3_counts.index,
            color_discrete_map={
                "Never": px.colors.qualitative.Prism[9],
                "No, usually longer than 30 days": px.colors.qualitative.Prism[8],
                "Yes, within 30 days": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### How helpful have Freedom of Information requests been for your work on intelligence-related issues? `[foi4]`"
    )
    foi4_counts = df[filter]["foi4"].value_counts()

    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=foi4_counts,
            names=foi4_counts.index,
        ),
        use_container_width=True,
    )

    st.write(
        "### Why haven’t you requested information under the national FOI law when you reported on intelligence-related issues over the past 5 years? `[foi5]`"
    )
    foi5_df = pd.DataFrame(columns=("option", "count", "country"))
    # TODO Map proper labels
    for label in [
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
        foi5_data = df[filter]["country"][df[f"foi5[{label}]"] == 1].tolist()
        for i in foi5_data:
            foi5_df = foi5_df.append(
                {"option": label, "count": foi5_data.count(i), "country": i},
                ignore_index=True,
            )
    foi5_df = foi5_df.drop_duplicates()
    st.plotly_chart(
        render_histogram(
            foi5_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"count": "people who answered 'Yes'"},
        ),
        use_container_width=True,
    )

    st.write("### If you selected ‘other’, please specify `[foi5other]`")
    for i in df[filter]["foi5other"].to_list():
        if type(i) != float:
            st.write("- " + i)

if selected_section == "Protection":
    st.write("# Protection")

    st.write("## Operational Protection")

    st.write(
        "### Have you taken any of the following measures to protect your datas from attacks and surveillance? `[protectops1]`"
    )
    protectops1_options = [
        "Participation in digital security training",
        "Use of E2E encrypted communication channels",
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
        for label in ["sectraining", "e2e"]:
            try:
                count = df[filter][f"protectops1[{label}]"].value_counts()[answer]
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

    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=protectops1_options,
                    y=protectops1_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=protectops1_options,
                    y=protectops1_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=protectops1_options,
                    y=protectops1_dont_know,
                    marker_color=px.colors.qualitative.Prism[10],
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=protectops1_options,
                    y=protectops1_prefer_not_to_say,
                    marker_color=px.colors.qualitative.Prism[10],
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write(
        "### Were any of these measures provided by your employer? `[protectops2]`"
    )
    protectops2_counts = df[filter]["protectops2"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=protectops2_counts,
            names=protectops2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

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
        for label in [
            "encrypted_email",
            "vpn",
            "tor",
            "e2e_chat",
            "encrypted_hardware",
            "2fa",
            "other",
        ]:
            try:
                count = df[filter][f"protectops3[{label}]"].value_counts()[importance]
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

    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Very important",
                    x=protectops3_options,
                    y=protectops3_very_important,
                    marker_color="#581845",
                ),
                go.Bar(
                    name="Somewhat important",
                    x=protectops3_options,
                    y=protectops3_somewhat_important,
                    marker_color="#900C3F",
                ),
                go.Bar(
                    name="Important",
                    x=protectops3_options,
                    y=protectops3_important,
                    marker_color="#C70039",
                ),
                go.Bar(
                    name="Slightly important",
                    x=protectops3_options,
                    y=protectops3_slightly_important,
                    marker_color="#FF5733",
                ),
                go.Bar(
                    name="Not important at all",
                    x=protectops3_options,
                    y=protectops3_not_important,
                    marker_color="#FFC300",
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ‘other’, please specify `[protectops3other]`")
    for i in df[filter]["protectops3other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### Which of the following statements best describes your level of confidence in the protection offered by technological tools? `[protectops4]`"
    )
    protectops4_counts = df[filter]["protectops4"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            protectops4_counts,
            values=protectops4_counts,
            names=protectops4_counts.index,
            color=protectops4_counts.index,
            color_discrete_map={
                "I have full confidence that the right tools <br>will protect my communication from surveillance": px.colors.qualitative.Prism[
                    4
                ],
                "Technological tools help to protect my identity <br>to some extent, but an attacker with sufficient power <br>may eventually be able to bypass my technological <br>safeguards": px.colors.qualitative.Prism[
                    5
                ],
                "Under the current conditions of communications <br>surveillance, technological solutions cannot offer <br>sufficient protection for the data I handle": px.colors.qualitative.Prism[
                    6
                ],
                "I have no confidence in the protection offered by <br>technological tools": px.colors.qualitative.Prism[
                    7
                ],
                "I try to avoid technology-based communication whenever <br>possible when I work on intelligence-related issues": px.colors.qualitative.Prism[
                    8
                ],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("## Legal Protection")

    # TODO Clarify that in MS it's about source protection (also for protectleg2)
    st.write(
        "### When working on intelligence-related issues, do you feel you have reason to be concerned about... surveillance of your activities (_CSO representatives_) | regarding the protection of your sources (_media representatives_) `[protectleg1]`"
    )

    protectleg1_counts = df[filter]["protectleg1"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=protectleg1_counts,
            names=protectleg1_counts.index,
            color=protectleg1_counts.index,
            color_discrete_map={
                "Always": px.colors.qualitative.Prism[9],
                "Often": px.colors.qualitative.Prism[8],
                "Sometimes": px.colors.qualitative.Prism[7],
                "Rarely": px.colors.qualitative.Prism[6],
                "Never": px.colors.qualitative.Prism[5],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### Do you regard the existing legal protections against surveillance of your activities in your country as a sufficient safeguard for your work on intelligence-related issues? `[protectleg2]`"
    )

    protectleg2_counts = df[filter]["protectleg2"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            protectleg2_counts,
            values=protectleg2_counts,
            names=protectleg2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
            color=protectleg2_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write("### If you selected ‘no’, please specify `[protectleg2no]`")
    for i in df[filter]["protectleg2no"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### Are any of the following forms of institutional support readily available to you? `[protectleg3]`"
    )
    protectleg3_options = ["Free legal counsel", "Legal cost insurance", "Other"]
    protectleg3_yes = []
    protectleg3_no = []
    protectleg3_dont_know = []
    protectleg3_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in ["free_counsel", "cost_insurance", "other"]:
            try:
                count = df[filter][f"protectleg3[{label}]"].value_counts()[answer]
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
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=protectleg3_options,
                    y=protectleg3_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=protectleg3_options,
                    y=protectleg3_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=protectleg3_options,
                    y=protectleg3_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=protectleg3_options,
                    y=protectleg3_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ‘other’, please specify `[protectleg3other]`")
    for i in df[filter]["protectleg3other"].to_list():
        if type(i) != float:
            st.write("- " + i)

if selected_section == "Constraints":
    st.write("# Constraints")

    st.write("## Interference by state authorities")

    st.write(
        "### Has your institution or have you yourself been subjected to surveillance by intelligence agencies in the past five years? `[constraintinter1]`"
    )

    constraintinter1_counts = df[filter]["constraintinter1"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=constraintinter1_counts,
            names=constraintinter1_counts.index,
            color=constraintinter1_counts.index,
            color_discrete_map={
                "No": px.colors.qualitative.Prism[8],
                "Yes, I have evidence": px.colors.qualitative.Prism[1],
                "Yes, I suspect": px.colors.qualitative.Prism[2],
                "I don't know": px.colors.qualitative.Prism[10],
                "I prefer not to say": px.colors.qualitative.Prism[10],
            },
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you been threatened with prosecution or have you actually been prosecuted for your work on intelligence-related issues? `[constraintinter2]`"
    )

    constraintinter2_counts = df[filter]["constraintinter2"].value_counts()
    constraintinter2_fig = px.pie(
        df[filter],
        values=constraintinter2_counts,
        names=constraintinter2_counts.index,
        color_discrete_sequence=px.colors.qualitative.Prism,
    )

    st.plotly_chart(constraintinter2_fig)

    st.write("### What was the outcome? `[constraintinter3]`")

    constraintinter3_counts = df[filter]["constraintinter3"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=constraintinter3_counts,
            names=constraintinter3_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you experienced any of the following interferences by public authorities in relation to your work on intelligence related topics? `[constraintinter4]`"
    )
    # TODO Map proper labels
    constraintinter4_yes = []
    constraintinter4_no = []
    constraintinter4_dont_know = []
    constraintinter4_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in constraintinter4_options:
            try:
                count = df[filter][f"constraintinter4[{label}]"].value_counts()[answer]
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
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=constraintinter4_options,
                    y=constraintinter4_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=constraintinter4_options,
                    y=constraintinter4_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=constraintinter4_options,
                    y=constraintinter4_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=constraintinter4_options,
                    y=constraintinter4_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write(
        "### In the past 5 years, have you been approached by intelligence officials and received... `[constraintinter5]`"
    )
    constraintinter5_options = [
        "Unsolicited information",
        "Invitations to off-the-record events or meetings",
        "Other",
    ]
    constraintinter5_yes = []
    constraintinter5_no = []
    constraintinter5_dont_know = []
    constraintinter5_prefer_not_to_say = []
    for answer in ["Yes", "No", "I don't know", "I prefer not to say"]:
        for label in ["unsolicited_information", "invitations", "other"]:
            try:
                count = df[filter][f"constraintinter5[{label}]"].value_counts()[answer]
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
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=constraintinter5_options,
                    y=constraintinter5_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=constraintinter5_options,
                    y=constraintinter5_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=constraintinter5_options,
                    y=constraintinter5_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=constraintinter5_options,
                    y=constraintinter5_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ‘other’, please specify `[constraintinter5other]`")
    for i in df[filter]["constraintinter5other"].to_list():
        if type(i) != float:
            st.write("- " + i)

    st.write(
        "### When working on intelligence-related issues have you ever experienced harassment by security agencies or politicians due to your... `[constraintinter6]`"
    )
    constraintinter6_options = [
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
        for label in [
            "gender",
            "ethnicity",
            "political",
            "sexual",
            "religious",
            "other",
        ]:
            try:
                count = df[filter][f"constraintinter6[{label}]"].value_counts()[answer]
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
    st.plotly_chart(
        render_stacked_bar_chart(
            data=[
                go.Bar(
                    name="Yes",
                    x=constraintinter6_options,
                    y=constraintinter6_yes,
                    marker_color=px.colors.qualitative.Prism[2],
                ),
                go.Bar(
                    name="No",
                    x=constraintinter6_options,
                    y=constraintinter6_no,
                    marker_color=px.colors.qualitative.Prism[8],
                ),
                go.Bar(
                    name="I don't know",
                    x=constraintinter6_options,
                    y=constraintinter6_dont_know,
                    marker_color="#7f7f7f",
                    opacity=0.8,
                ),
                go.Bar(
                    name="I prefer not to say",
                    x=constraintinter6_options,
                    y=constraintinter6_prefer_not_to_say,
                    marker_color="#525252",
                    opacity=0.8,
                ),
            ],
        ),
        use_container_width=True,
    )

    st.write("### If you selected ‘other’, please specify `[constraintinter6other]`")
    for i in df[filter]["constraintinter6other"].to_list():
        if type(i) != float:
            st.write("- " + i)

if selected_section == "Attitudes":
    st.write("# Attitudes")

    st.write(
        "### The following four statements are about **intelligence agencies**. Please select the statement you most agree with, based on your national context. `[attitude1]`"
    )

    attitude1_counts = df[filter]["attitude1"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=attitude1_counts,
            names=attitude1_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

    st.write(
        "### The following four statements are about **intelligence oversight**. Please select the statement you most agree with, based on your national context. `[attitude2]`"
    )

    attitude2_counts = df[filter]["attitude2"].value_counts()
    st.plotly_chart(
        gen_px_pie(
            df[filter],
            values=attitude2_counts,
            names=attitude2_counts.index,
            color_discrete_sequence=px.colors.qualitative.Prism,
        ),
        use_container_width=True,
    )

    st.write(
        "### In your personal view, what are the goals of intelligence oversight? Please select the three goals of oversight you subscribe to the most. `[attitude3]`"
    )

    # TODO Map proper labels
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
    for label in attitude3_options:
        attitude3_data = df[filter]["country"][df[f"attitude3[{label}]"] == 1].tolist()
        for i in attitude3_data:
            attitude3_df = attitude3_df.append(
                {"option": label, "count": attitude3_data.count(i), "country": i},
                ignore_index=True,
            )
    attitude3_df = attitude3_df.drop_duplicates()

    st.plotly_chart(
        render_histogram(
            df=attitude3_df,
            x="option",
            y="count",
            nbins=None,
            color="country",
            color_discrete_map={
                "Germany": px.colors.qualitative.Prism[5],
                "France": px.colors.qualitative.Prism[1],
                "United Kingdom": px.colors.qualitative.Prism[7],
            },
            labels={"count": "people who answered 'Yes'"},
        ),
        use_container_width=True,
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
    st.plotly_chart(render_ranking_plot("attitude4"), use_container_width=True)

    st.write(
        "### Which of the following actors do you trust the most to **contest surveillance** by intelligence agencies? `[attitude5]`"
    )
    st.plotly_chart(render_ranking_plot("attitude5"), use_container_width=True)

    st.write(
        "### Which of the following actors do you trust the most to **enforce compliance** regarding surveillance by intelligence agencies? `[attitude6]`"
    )
    st.plotly_chart(render_ranking_plot("attitude6"), use_container_width=True)


if selected_section == "Appendix":
    st.write("# Appendix")

    st.write("## Raw data")

    st.write(get_csv_download_link(df, "merged"), unsafe_allow_html=True)
    st.write(get_excel_download_link(df, "merged"), unsafe_allow_html=True)

    table = st.checkbox("Show data as table")
    if table:
        st.dataframe(df[filter])

    st.write("## Correlation Matrix (Phik `φK`)")

    st.write(
        "Phik (φk) is a new and practical correlation coefficient that works consistently between categorical, ordinal and interval variables, captures non-linear dependency and reverts to the Pearson correlation coefficient in case of a bivariate normal input distribution. There is extensive documentation available [here](https://phik.readthedocs.io/en/latest/index.html)"
    )

    show_corr = st.checkbox("Show correlation matrix")
    if show_corr:
        fig_corr = get_corr_matrix(df)
        st.plotly_chart(fig_corr, use_container_width=True)

    st.write("## Significance Matrix")

    st.markdown(
        body="When assessing correlations it is good practise to evaluate both the correlation and the significance of the correlation: a large correlation may be statistically insignificant, and vice versa a small correlation may be very significant. For instance, scipy.stats.pearsonr returns both the pearson correlation and the p-value. Similarly, the phik package offers functionality the calculate a significance matrix. Significance is defined as: "
    )
    st.markdown(
        body="$Z=\Phi^{-1}(1-p); \Phi(z)=\\frac{1}{\\sqrt{2\pi}}\int_{-\infty}^{z} e^{-t^{2}/2}\,dt$"
    )

    show_sig = st.checkbox("Show significance matrix")
    if show_sig:
        fig_sig = get_significance_matrix(df)
        st.plotly_chart(fig_sig, use_container_width=True)
