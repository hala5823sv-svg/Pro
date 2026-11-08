
import streamlit as st
import pandas as pd

# إعدادات صفحة التطبيق
st.set_page_config(
    page_title="المساعد الذكي لترشيد استهلاك المياه",
    page_icon="💧",
    layout="centered"
)

# عنوان التطبيق
st.title("💧 المساعد الذكي لترشيد استهلاك المياه والمصاريف")

st.markdown("""
هذا التطبيق يساعدك على تحليل استهلاكك اليومي والشهري للمياه،
وحساب التكلفة المالية المتوقعة، ومقارنة الفواتير عبر الأشهر
لمتابعة مدى تحسن كفاءة التوفير لديك.
""")

st.markdown("---")

# قسم المدخلات
st.header("📊 أدخل بيانات استهلاك عائلتك")

family_members = st.number_input(
    "عدد أفراد الأسرة:",
    min_value=1,
    max_value=50,
    value=4
)

st.subheader("تفاصيل الاستخدام اليومي:")

shower_time = st.slider(
    "متوسط مدة الاستحمام للشخص الواحد (بالدقائق يومياً):",
    min_value=2,
    max_value=30,
    value=10
)

dish_washing = st.selectbox(
    "طريقة غسيل الأطباق:",
    [
        "غسالة الأطباق (اقتصادية)",
        "غسيل اليدين بالصنبور المفتوح",
        "غسيل اليدين باستخدام حوض مغلق"
    ]
)

car_washing = st.selectbox(
    "غسيل السيارات المنزلية:",
    [
        "خرطوم مياه مستمر",
        "دلو ومنديل (موفر)",
        "لا توجد سيارة"
    ]
)

plants_watering = st.checkbox(
    "هل يوجد سقي للحديقة أو النباتات المنزلية بانتظام؟"
)

# حساب الاستهلاك التقديري باللتر
shower_total = family_members * shower_time * 12

if "غسالة" in dish_washing:
    dish_total = 40
elif "المفتوح" in dish_washing:
    dish_total = 120
else:
    dish_total = 50

if "خرطوم" in car_washing:
    car_total = 300 / 4
elif "دلو" in car_washing:
    car_total = 60 / 4
else:
    car_total = 0

plants_total = 80 if plants_watering else 0

total_daily_consumption = (
    shower_total + dish_total + car_total + plants_total
)

total_monthly_consumption = total_daily_consumption * 30

# حساب الفاتورة التقديرية
estimated_cost = (total_monthly_consumption / 1000) * 4.0

st.markdown("---")

# عرض النتائج
st.header("📈 نتائج التحليل المالي والكمي")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="الاستهلاك اليومي",
        value=f"{int(total_daily_consumption)} لتر"
    )

with col2:
    st.metric(
        label="الاستهلاك الشهري",
        value=f"{int(total_monthly_consumption)} لتر"
    )

with col3:
    st.metric(
        label="التكلفة الشهرية المقدرة",
        value=f"{estimated_cost:.2f} عملة"
    )

# تقييم الاستهلاك
average_per_capita = total_daily_consumption / family_members

if average_per_capita > 150:
    st.error(
        "⚠️ استهلاكك مرتفع جداً مقارنة بالمعدل الطبيعي. "
        "هناك فرصة كبيرة لتوفير المياه وخفض الفاتورة!"
    )

elif average_per_capita > 100:
    st.warning(
        "⚠️ استهلاكك متوسط، ولكن يمكنك تطبيق بعض النصائح لتقليله أكثر."
    )

else:
    st.success(
        "🌟 ممتاز! استهلاكك الاقتصادي للمياه في نطاق مثالي ومستدام."
    )

st.markdown("---")

# قسم حفظ ومقارنة الفواتير الشهرية
st.header("📋 سجل مقارنة الاستهلاك الشهري")

st.markdown(
    "قم بتسجيل استهلاكك لكل شهر لمقارنة الأداء "
    "ومعرفة مدى نجاح خطط الترشيد:"
)

# تهيئة الذاكرة المؤقتة لحفظ البيانات
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=[
            "الشهر",
            "الاستهلاك الشهري (لتر)",
            "التكلفة التقديرية"
        ]
    )

with st.form("save_form"):

    month_name = st.selectbox(
        "اختر الشهر:",
        [
            "يناير", "فبراير", "مارس", "أبريل",
            "مايو", "يونيو", "يوليو", "أغسطس",
            "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]
    )

    submitted = st.form_submit_button(
        "حفظ النتيجة الحالية في السجل"
    )

    if submitted:

        new_data = pd.DataFrame({
            "الشهر": [month_name],
            "الاستهلاك الشهري (لتر)": [
                int(total_monthly_consumption)
            ],
            "التكلفة التقديرية": [
                round(estimated_cost, 2)
            ]
        })

        # دمج البيانات وتجنب التكرار لنفس الشهر
        st.session_state.history = pd.concat(
            [
                st.session_state.history[
                    st.session_state.history["الشهر"] != month_name
                ],
                new_data
            ],
            ignore_index=True
        )

        st.success(
            f"تم حفظ بيانات شهر {month_name} بنجاح!"
        )

# عرض السجل والرسم البياني
if not st.session_state.history.empty:

    st.subheader("سجل الأداء المحفوظ:")

    st.dataframe(
        st.session_state.history,
        use_container_width=True
    )

    st.subheader("📊 رسم بياني لمقارنة الاستهلاك")

    st.bar_chart(
        st.session_state.history.set_index("الشهر")[
            "الاستهلاك الشهري (لتر)"
        ]
    )

st.markdown("---")

# قسم النصائح الذكية المخصصة
st.header("💡 نصائح مخصصة لترشيد الاستهلاك")

recommendations = []

if shower_time > 8:

    recommendations.append(
        f"⏱️ تقليل وقت الاستحمام: تقليل وقت الاستحمام "
        f"بمقدار 3 دقائق لكل فرد سيوفر حوالي "
        f"{family_members * 3 * 12 * 30} لتراً شهرياً."
    )

if "المفتوح" in dish_washing:

    recommendations.append(
        "🍽️ تعديل طريقة غسيل الأطباق: استخدام حوض مغلق "
        "بدلاً من ترك الصنبور مفتوحاً أثناء غسيل الأطباق "
        "يمكن أن يوفر كمية كبيرة من المياه."
    )

if "خرطوم" in car_washing:

    recommendations.append(
        "🚗 غسيل السيارة: استبدال خرطوم المياه المستمر "
        "بالدلو والإسفنجة يوفر مئات اللترات من المياه."
    )

if not recommendations:

    recommendations.append(
        "🌟 أنت تتبع عادات رائعة حقاً! "
        "استمر في المحافظة على هذه الوتيرة."
    )

for rec in recommendations:
    st.markdown(f"- {rec}")

st.markdown("---")

# خاتمة التطبيق
st.caption(
    "تم تطوير هذا التطبيق لمساعدتك في إدارة موارد المياه "
    "والمصاريف بذكاء 🌍."
)
