# app.py
import streamlit as st

# Page config
st.set_page_config(page_title="Angu-Lator", page_icon="📐", layout="centered")

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = {}  # track which questions answered

st.title("📐 Angu-Lator")
st.write("Solve angle-pair problems and circle-secant/tangent angle problems. Includes a short assessment with scoring.")

# ---------- PART 1: ANGLE PAIRS ----------
st.header("Part 1 — Angle Pairs (Two Angles)")
pair_type = st.selectbox("Select angle type:",
                         ["Complementary", "Supplementary", "Linear Pair", "Vertical Angles"])
angle1 = st.number_input("Enter Angle 1 (degrees)", min_value=0.0, max_value=360.0, step=0.1, format="%.2f")

if st.button("Solve Angle Pair"):
    if angle1 == 0 and pair_type != "Vertical Angles":
        st.warning("Please enter a non-zero angle for this case.")
    else:
        if pair_type == "Complementary":
            a2 = 90.0 - angle1
            st.success(f"Result: A₂ = {a2:.2f}°")
            with st.expander("Step-by-step"):
                st.write(r"Formula: A₁ + A₂ = 90°")
                st.write(f"Substitute: A₁ = {angle1}°, so A₂ = 90° − {angle1}° = {a2:.4f}°")
        elif pair_type in ("Supplementary", "Linear Pair"):
            a2 = 180.0 - angle1
            st.success(f"Result: A₂ = {a2:.2f}°")
            with st.expander("Step-by-step"):
                st.write(r"Formula: A₁ + A₂ = 180°")
                st.write(f"Substitute: A₁ = {angle1}°, so A₂ = 180° − {angle1}° = {a2:.4f}°")
        else:  # Vertical
            a2 = angle1
            st.success(f"Result: A₂ = {a2:.2f}° (vertical angles are congruent)")
            with st.expander("Step-by-step"):
                st.write("Vertical angles are equal because they are formed by two intersecting straight lines.")
                st.write(f"Given A₁ = {angle1}°, so A₂ = {a2:.2f}°")

st.markdown("---")

# ---------- PART 2: CIRCLE ANGLES ----------
st.header("Part 2 — Circle Angles (Tangents & Secants)")

circle_case = st.selectbox("Select circle case:",
                           [
                               "Two Tangents Intersect Outside the Circle",
                               "Tangent and Secant Intersect Outside the Circle",
                               "Two Secants Intersect Outside the Circle",
                               "Tangent and Secant at Point of Tangency",
                               "Two Secants Intersect Inside the Circle"
                           ])

st.write("Provide known values (leave blank or zero for unknowns).")
c_angle = st.number_input("Enter angle (if known, degrees)", min_value=0.0, max_value=1000.0, step=0.1, format="%.2f")
arc1 = st.number_input("Enter Arc 1 (far/major arc in degrees)", min_value=0.0, max_value=1000.0, step=0.1, format="%.2f")
arc2 = st.number_input("Enter Arc 2 (near/minor arc in degrees)", min_value=0.0, max_value=1000.0, step=0.1, format="%.2f")

if st.button("Solve Circle Problem"):
    known = {"angle": c_angle > 0, "arc1": arc1 > 0, "arc2": arc2 > 0}
    result_text = None

    # helper for formatting
    def F(x): return f"{x:.2f}°"

    # OUTSIDE EXTERIOR (two tangents, tangent+secant outside, two secants outside)
    if circle_case in (
        "Two Tangents Intersect Outside the Circle",
        "Tangent and Secant Intersect Outside the Circle",
        "Two Secants Intersect Outside the Circle"
    ):
        label = circle_case
        if known["arc1"] and known["arc2"] and not known["angle"]:
            res = 0.5 * (arc1 - arc2)
            result_text = f"Exterior angle = ½(Arc₁ − Arc₂) = ½({arc1} − {arc2}) = {F(res)}"
        elif known["angle"] and known["arc1"] and not known["arc2"]:
            res = arc1 - 2 * c_angle
            result_text = f"Arc₂ = Arc₁ − 2×∠ = {arc1} − 2×{c_angle} = {F(res)}"
        else:
            result_text = "Not enough data: provide (arc1 & arc2) or (angle & arc1)."

    # TANGENT & SECANT AT POINT OF TANGENCY (angle = 1/2 intercepted arc)
    elif circle_case == "Tangent and Secant at Point of Tangency":
        if known["arc1"] and not known["angle"]:
            res = 0.5 * arc1
            result_text = f"Angle = ½(intercepted arc) = ½×{arc1} = {F(res)}"
        elif known["angle"] and not known["arc1"]:
            res = 2 * c_angle
            result_text = f"Intercepted arc = 2×angle = 2×{c_angle} = {F(res)}"
        else:
            result_text = "Provide either intercepted arc (to get angle) or angle (to get arc)."

    # TWO SECANTS INSIDE (angle = 1/2(arc1 + arc2))
    elif circle_case == "Two Secants Intersect Inside the Circle":
        if known["arc1"] and known["arc2"] and not known["angle"]:
            res = 0.5 * (arc1 + arc2)
            result_text = f"Interior angle = ½({arc1} + {arc2}) = {F(res)}"
        elif known["angle"] and known["arc1"] and not known["arc2"]:
            res = 2 * c_angle - arc1
            result_text = f"Arc₂ = 2×angle − Arc₁ = 2×{c_angle} − {arc1} = {F(res)}"
        else:
            result_text = "Not enough data: provide (arc1 & arc2) or (angle & arc1)."

    if result_text:
        st.success(result_text)
        with st.expander("Show formula & steps"):
            st.write("Formula depends on the selected case. Substitute your known values and compute as shown in the result.")

st.markdown("---")

# ---------- ASSESSMENT (6 Qs) ----------
st.header("🧠 Assessment — 6 questions (score tracked)")

st.write("Your current score:", st.session_state.score, "/ 6")

# Questions: list of dicts with 'q' (text), 'choices' (list), 'answer' (index)
QUESTIONS = [
    {"q": "If two angles are supplementary and one is 110°, what is the other?",
     "choices": ["70°", "90°", "110°", "180°"], "answer": 0},
    {"q": "If two angles are complementary and one is 30°, what is the other?",
     "choices": ["60°", "30°", "120°", "90°"], "answer": 0},
    {"q": "A tangent and a secant intersect outside a circle; far arc = 200°, near arc = 80°. What is the angle?",
     "choices": ["60°", "70°", "40°", "120°"], "answer": 0},  # 1/2(200-80)=60
    {"q": "Two secants intersect inside a circle, arcs are 70° and 50°. Interior angle?",
     "choices": ["60°", "120°", "30°", "20°"], "answer": 0},  # 1/2(70+50)=60
    {"q": "A linear pair with one angle 45°. The other angle is:",
     "choices": ["135°", "45°", "90°", "225°"], "answer": 0},
    {"q": "Vertical angle equal to 85°. Opposite angle equals:",
     "choices": ["85°", "95°", "180°", "0°"], "answer": 0},
]

# Present all questions with independent widgets
for i, item in enumerate(QUESTIONS):
    q_key = f"q_{i}"
    st.write(f"**Q{i+1}.** {item['q']}")
    # if already answered, show selected and whether correct
    if st.session_state.answered.get(q_key):
        sel_index = st.session_state.answered[q_key]["selected"]
        correct = item["answer"]
        if sel_index == correct:
            st.success(f"You answered: {item['choices'][sel_index]} — Correct ✅")
        else:
            st.error(f"You answered: {item['choices'][sel_index]} — Incorrect ❌ (Correct: {item['choices'][correct]})")
        st.write("---")
        continue

    selected = st.radio("Choose an answer:", item["choices"], key=q_key)
    if st.button("Submit Answer", key=f"submit_{i}"):
        sel_index = item["choices"].index(selected)
        correct = item["answer"]
        # mark answered
        st.session_state.answered[q_key] = {"selected": sel_index}
        if sel_index == correct:
            st.session_state.score += 1
            st.success("Correct ✅")
        else:
            st.error(f"Incorrect ❌ — correct is: {item['choices'][correct]}")
        st.experimental_rerun()  # rerun to refresh UI and lock the answered question

st.markdown("---")
if st.button("Reset Assessment (clear score and answers)"):
    st.session_state.score = 0
    st.session_state.answered = {}
    st.experimental_rerun()
