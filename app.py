import streamlit as st
import pandas as pd

st.set_page_config(page_title="Taekwondo Training Dashboard", layout="wide")

st.title("🥋 Taekwondo Training Dashboard")
st.subheader("Select your belt:")

belts_df = pd.read_csv("data/belts.csv")
kicks_df = pd.read_csv("data/kicks.csv")
forms_df = pd.read_csv("data/forms.csv")
one_steps_df = pd.read_csv("data/one_steps.csv")
board_df = pd.read_csv("data/board_techniques.csv")

def filter_data(df, belt_color, belt_value, content_col=None):
    filtered = df[df[belt_color] == belt_value]

    if content_col:
        filtered = filtered[
            (filtered[content_col].notna()) &
            (filtered[content_col].astype(str).str.strip() != "")
        ]

    return filtered

selected_belt = st.selectbox("Select your belt", belts_df["belt"], label_visibility = "collapsed", width = 500)
filtered_forms = filter_data(forms_df, "belt", selected_belt)
form_name = filtered_forms["form"].iloc[0]
tkda_video = filtered_forms["tkda_video"].iloc[0] if not filtered_forms.empty else None
mta_video = filtered_forms["mta_video"].iloc[0] if not filtered_forms.empty else None
filtered_kicks = filter_data(kicks_df,"belt", selected_belt, "kick")
filtered_one_steps = filter_data(one_steps_df, "belt", selected_belt, "strike_kick_block")
filtered_board_techniques = filter_data(board_df, "belt", selected_belt, "technique")

# def display_section(title, df, content_col):
#     if not df.empty:
#         # with st.expander(title, expanded=True):
#             for item in df[content_col]:
#                 st.markdown(f"- {item}")

tab1, tab2, tab3, tab4, tab5 = st.tabs([form_name, f"{form_name} Videos", "One Steps", "Kicks", "Board Tehcniques"])

with tab1:
    st.table(
        filtered_forms[["strike_kick_block", "stance"]]
            .rename(columns={
                "strike_kick_block": "Technique",
                "stance":"Stance"
            })
        .reset_index(drop=True)
    )

with tab2:
    col1, col2 =st.columns(2)
    
    with col1:
        st.subheader("Taekwondo America Tutorial")
        st.video(tkda_video, width=500)

    with col2:
        st.subheader("McClellan's Taekwondo Academy Tutorial")
        st.video(mta_video, format="video/mp4", start_time=0, width=500)

with tab3:
    if not filtered_one_steps.empty:
    # with st.expander("One Steps", expanded=not filtered_one_steps.empty):

        # Get unique one step numbers for this belt
        step_numbers = sorted(filtered_one_steps["one_step_no"].dropna().unique())

        for step_no in step_numbers:
            step_data = filtered_one_steps[filtered_one_steps["one_step_no"] == step_no]

            if step_data.empty:
                continue

            st.markdown(f"#### 🥋 One Step {int(step_no)}")

            for i, row in enumerate(step_data.itertuples(), start=1):
                technique = row.strike_kick_block

                if pd.isna(technique) or technique == "":
                    st.markdown(f"{i}. None")
                else:
                    st.markdown(f"{i}. {technique}")

            st.markdown("---")
    else: st.write("No One Steps")

with tab4: 
    #display_section("Kicks", filtered_kicks, "kick")
    if not filtered_kicks.empty:
        for item in filtered_kicks["kick"]:
                st.markdown(f"- {item}")
    else: 
        st.write("No Kicks")


with tab5:
    #display_section("Board Breaking Techniques", filtered_board_techniques, "technique")
    if not filtered_board_techniques.empty:
        for item in filtered_board_techniques["technique"]:
                st.markdown(f"- {item}")
    else:
         st.write("No Board Techniques")
    
# with st.expander(f"{form_name}", expanded=not filtered_forms.empty):
#     st.table(
#         filtered_forms[["strike_kick_block", "stance"]]
#             .rename(columns={
#                 "strike_kick_block": "Technique",
#                 "stance":"Stance"
#             })
#         .reset_index(drop=True)
#     )
#     with st.expander(f"{form_name} Video Tutorials"):
#         col1, col2 =st.columns(2)
    
#         with col1:
#             st.write("Taekwondo America Tutorial")
#             st.video(tkda_video, width=500)

#         with col2:
#             st.write("McClellan's Taekwondo Academy Tutorial")
#             st.video(mta_video, format="video/mp4", start_time=0, width=500)
           


# display_section("Kicks", filtered_kicks, "kick")
# with st.expander("Kicks"):
#     for kick in filtered_kicks["kick"]:
#         st.markdown(f"- {kick}")


# if not filtered_one_steps.empty:
#     # with st.expander("One Steps", expanded=not filtered_one_steps.empty):

#         # Get unique one step numbers for this belt
#         step_numbers = sorted(filtered_one_steps["one_step_no"].dropna().unique())

#         for step_no in step_numbers:
#             step_data = filtered_one_steps[filtered_one_steps["one_step_no"] == step_no]

#             if step_data.empty:
#                 continue

#             st.markdown(f"#### 🥋 One Step {int(step_no)}")

#             for i, row in enumerate(step_data.itertuples(), start=1):
#                 technique = row.strike_kick_block

#                 if pd.isna(technique) or technique == "":
#                     st.markdown(f"{i}. None")
#                 else:
#                     st.markdown(f"{i}. {technique}")

#             st.markdown("---")
# else: st.write("No One Steps")

# display_section("Board Breaking Techniques", filtered_board_techniques, "technique")

# if not filtered_board_techniques.empty:
#     with st.expander("Board Breaking Techniques", expanded=True):
#         for technique in filtered_board_techniques["technique"]:
#             if pd.isna(technique):
#                 st.markdown("None")
#             else: 
#                 st.markdown(f"- {technique}")

