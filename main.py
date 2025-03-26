import streamlit as st
import requests
page_bg = """
<style>
    .stApp {
        background-color: rgba(0, 0, 0, 0.5); /* اضافه کردن شفافیت به پس‌زمینه برای خوانایی */
        padding: 1.5rem;
        border-radius: 10px;
    }
    .responsive-container {
        max-width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-end;
        margin: 0 auto;
        color: white;
    }
    input[type="text"] {
        text-align: right; 
    }
    @media (max-width: 768px) {
        body {
            font-size: 14px;
        }
        .stApp {
            padding: 1rem;
        }
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
def main():
    st.title("📍 پیدا کردن اطلاعات استان با شماره پلاک")
    st.markdown("""
        <div class='responsive-container'>
            لطفاً شماره پلاک دو‌رقمی را وارد کنید تا اطلاعات استان مربوطه نمایش داده شود.
        </div>
    """, unsafe_allow_html=True)


    plate_number = st.text_input("🛂 شماره پلاک:", max_chars=2, placeholder="مثال: 15")

    if plate_number:
        api = f'https://iran-locations-api.ir/api/v1/fa/states?carLicencePlate={plate_number}'
        response = requests.get(api)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
                name = item.get("name", "نام استان یافت نشد.")
                center = item.get("center", "مرکز استان یافت نشد.")
                plates = item.get("carLicencePlates", "پلاک‌ها یافت نشدند.")
                st.markdown(f"""
                    <div class='responsive-container'>
                        ✅ <b>اطلاعات استان دریافت شد:</b><br>
                        🔸 <b>نام استان:</b> {name}<br>
                        🔹 <b>مرکز استان:</b> {center}<br>
                        🚘 <b>پلاک‌های دیگر استان:</b> {", ".join(plates) if isinstance(plates, list) else plates}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class='responsive-container' style='color: orange;'>
                        ⚠️ متأسفانه اطلاعاتی برای این شماره پلاک یافت نشد.
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='responsive-container' style='color: red;'>
                    ❌ خطا در دریافت داده‌ها از سرور. [کد وضعیت: {response.status_code}]
                </div>
            """, unsafe_allow_html=True)
main()
