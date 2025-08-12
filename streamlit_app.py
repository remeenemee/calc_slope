import streamlit as st
import math

# Заголовок приложения
st.title("📏 Калькулятор уклонов и отметок")
st.markdown("Вычисления уклонов, отметок и расстояний для инженерных задач.")

# Разделитель
st.divider()


# --- Функции ---
def calculate_slope(point1: float, point2: float, distance: float) -> dict:
    """Вычисляет уклон в %, ‰ и угол в градусах."""
    height_diff = point2 - point1
    slope_percent = (height_diff / distance) * 100
    slope_permille = slope_percent * 10
    slope_angle = math.degrees(math.atan(height_diff / distance))
    return {
        "percent": round(slope_percent, 2),
        "permille": round(slope_permille, 2),
        "angle": round(slope_angle, 2)
    }


def calculate_mark(point1: float, distance: float, slope_permille: float) -> float:
    """Вычисляет вторую отметку по уклону (в ‰)."""
    slope_percent = slope_permille / 10
    height_diff = (slope_percent / 100) * distance
    return round(point1 + height_diff, 2)


def calculate_distance(point1: float, point2: float, slope_permille: float) -> float:
    """Вычисляет расстояние по разнице отметок и уклону (в ‰)."""
    height_diff = abs(point2 - point1)
    slope_percent = slope_permille / 10
    if slope_percent == 0:
        raise ValueError("Уклон не может быть 0‰ — деление на ноль.")
    distance = height_diff / (slope_percent / 100)
    return round(distance, 2)


# --- Вкладки в Streamlit ---
tab1, tab2, tab3 = st.tabs(["🔍 Найти уклон", "🎯 Найти отметку", "📏 Найти расстояние"])

# --- Вкладка 1: Найти уклон ---
with tab1:
    st.header("Расчёт уклона")
    with st.form("slope_form"):
        point1 = st.number_input("Первая отметка (м)", value=0.0, step=0.1, key="slope_p1")
        point2 = st.number_input("Вторая отметка (м)", value=0.0, step=0.1, key="slope_p2")
        distance = st.number_input("Расстояние между точками (м)", value=1.0, min_value=0.1, step=0.1, key="slope_dist")

        submitted1 = st.form_submit_button("Рассчитать уклон")

    if submitted1:
        try:
            result = calculate_slope(point1, point2, distance)
            st.success(
                f"Уклон: **{result['percent']}%** ({result['permille']}‰), "
                f"угол: **{result['angle']}°**"
            )
        except Exception as e:
            st.error("Ошибка расчёта уклона. Проверьте введённые данные.")


# --- Вкладка 2: Найти отметку ---
with tab2:
    st.header("Расчёт второй отметки")
    with st.form("mark_form"):
        point1 = st.number_input("Исходная отметка (м)", value=0.0, step=0.1, key="mark_p1")
        distance = st.number_input("Расстояние (м)", value=10.0, min_value=0.0, step=0.1, key="mark_dist")
        slope_permille = st.number_input("Уклон (в промилле, ‰)", value=10.0, step=1.0, key="mark_slope")

        submitted2 = st.form_submit_button("Рассчитать отметку")

    if submitted2:
        try:
            new_mark = calculate_mark(point1, distance, slope_permille)
            st.success(f"Новая отметка: **{new_mark} м**")
        except Exception as e:
            st.error("Ошибка расчёта отметки.")


# --- Вкладка 3: Найти расстояние ---
with tab3:
    st.header("Расчёт расстояния")
    with st.form("distance_form"):
        point1 = st.number_input("Первая отметка (м)", value=0.0, step=0.1, key="dist_p1")
        point2 = st.number_input("Вторая отметка (м)", value=1.0, step=0.1, key="dist_p2")
        slope_permille = st.number_input("Уклон (в промилле, ‰)", value=10.0, step=1.0, key="dist_slope")

        submitted3 = st.form_submit_button("Рассчитать расстояние")

    if submitted3:
        try:
            dist = calculate_distance(point1, point2, slope_permille)
            st.success(f"Требуемое расстояние: **{dist} м**")
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error("Ошибка расчёта расстояния.")


# --- Подвал ---
st.divider()
st.caption("💡 Приложение для расчёта уклонов, отметок и расстояний. Используется в дорожном/инженерном проектировании.")