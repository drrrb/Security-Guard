import streamlit as st
st.markdown("""
<style>
    /* ضبط اتجاه الموقع ليكون من اليمين لليسار */
    .stApp {
        direction: rtl;
    }
    /* منع تكسير الكلمات العربية وظهورها بشكل عمودي */
    * {
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }
</style>
""", unsafe_allow_html=True)
from supabase import create_client, Client
import urllib.parse

# ==========================================
# 1. الإعدادات الأساسية والتصميم المتكامل (متطلب 1)
# ==========================================
st.set_page_config(page_title="منصة حارس أمن", page_icon="🛡️", layout="wide")

# تصميم CSS حديث لجعل الموقع بالكامل من اليمين لليسار وتحسين مظهر الأزرار
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
        
        /* ضبط الخط والاتجاه */
        html, body, [class*="css"] {
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }
        
        /* ضبط اتجاه النصوص في الحاويات */
        .st-emotion-cache-1y4p8pa, .st-emotion-cache-16idsys p, h1, h2, h3 {
            direction: rtl;
            text-align: right;
        }
        
        /* تصميم زر الواتساب ليظهر بشكل عصري */
        .stLinkButton>a {
            background-color: #25D366 !important; 
            color: white !important; 
            border-radius: 8px !important; 
            border: none !important; 
            font-weight: bold !important;
            width: 100%;
            text-align: center;
            display: block;
            padding: 10px;
            text-decoration: none;
        }
        .stLinkButton>a:hover {
            background-color: #128C7E !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# إعدادات الاتصال بقاعدة البيانات (ضع بياناتك هنا)
# ==========================================
SUPABASE_URL = "https://ypynxxuurxkuwlppdwed.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlweW54eHV1cnhrdXdscHBkd2VkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQzMTMzMTcsImV4cCI6MjA5OTg4OTMxN30.JfJ_kb_J9hUY-YDYk2p5dmFbcnz-DIFThIumn8sdEMY"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_connection()

# ==========================================
# جلب البيانات من القاعدة
# ==========================================
@st.cache_data(ttl=60) # تحديث البيانات كل 60 ثانية
def load_jobs():
    try:
        response = supabase.table("jobs").select("*").execute()
        return response.data
    except Exception as e:
        return []

all_jobs = load_jobs()

# ==========================================
# القائمة الجانبية (الأقسام والدعم الفني) (متطلب 15 و 16)
# ==========================================
st.sidebar.title("🛡️ منصة حارس أمن")
st.sidebar.markdown("---")

# التنقل بين الصفحات
page = st.sidebar.radio(
    "اختر القسم:",
    ["💼 الوظائف العامة", "🕋 وظائف موسم الحج", "🛠️ الدعم الفني"]
)

# ==========================================
# دالة مساعدة لعرض الوظائف في مربعات (متطلب 13 و 14)
# ==========================================
def display_jobs(jobs_list):
    if not jobs_list:
        st.info("لا توجد وظائف تطابق بحثك حالياً.")
        return

    for job in jobs_list:
        # متطلب 13 + 14: كل وظيفة في مربع (Container) خاص بها ينزل للأسفل
        with st.container(border=True):
            title = job.get('title') or 'وظيفة أمنية'
            
            # علامة تمييز إذا كانت التغطية ليوم واحد (متطلب 5)
            is_one_day = job.get('is_one_day')
            if is_one_day:
                st.error("🚨 هذه الوظيفة: تغطية ليوم واحد فقط")
                
            st.subheader(f"🔹 {title}")
            
            # تقسيم المعلومات لعمودين مرتبين
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"*🏢 الشركة:* {job.get('company') or 'غير محدد'}") # متطلب 3
                st.write(f"*📍 المنطقة:* {job.get('location') or 'غير محدد'}")
                st.write(f"*🗺️ موقع العمل:* {job.get('exact_loc') or 'غير محدد'}") # متطلب 10
                st.write(f"*💰 الراتب:* {job.get('salary') or 'غير محدد'}") # متطلب 6
                st.write(f"*🕒 أوقات الدوام:* {job.get('work_hours') or 'غير محدد'}") # متطلب 11
            
            with col2:
                st.write(f"*📅 تاريخ المباشرة:* {job.get('start_date') or 'غير محدد'}") # متطلب 6
                st.write(f"*🏖️ الإجازة:* {job.get('vacation') or 'غير محدد'}") # متطلب 7
                st.write(f"*👨‍💼 العمر المطلوب:* {job.get('age_req') or 'غير محدد'}") # متطلب 8
                st.write(f"*👔 الزي الرسمي:* {job.get('uniform') or 'غير محدد'}") # متطلب 9
                
            st.markdown("---")
            
            # زر التقديم عبر الواتساب (متطلب 12)
            whatsapp_number = job.get('whatsapp_number')
            if whatsapp_number:
                wa_num = str(whatsapp_number).strip().replace(" ", "").replace("+", "")
                if wa_num.startswith("05"):
                    wa_num = "966" + wa_num[1:]
                
                message = f"السلام عليكم، بخصوص إعلان وظيفة ({title}) المعروضة في منصة حارس أمن، هل لا زال التقديم متاحاً؟"
                encoded_message = urllib.parse.quote(message)
                wa_url = f"https://wa.me/{wa_num}?text={encoded_message}"
                
                st.link_button("💬 التقديم الآن عبر الواتساب", wa_url)
            else:
                st.warning("⚠️ رقم التواصل غير متوفر.")

# ==========================================
# محتوى الصفحات
# ==========================================

if page == "💼 الوظائف العامة":
    st.title("👋 مرحباً بك في منصة حارس أمن")
    st.markdown("تصفح أحدث الفرص الوظيفية في مجال الحراسات الأمنية وقدم عليها مباشرة.")
    st.markdown("---")
    
    # متطلب 2: فلاتر للمناطق والراتب
    st.sidebar.markdown("### 🔍 تصفية الوظائف")
    
    # استخراج المناطق المتاحة من البيانات
    available_locations = list(set([j.get('location') for j in all_jobs if j.get('location')]))
    selected_location = st.sidebar.selectbox("📍 اختر المنطقة", ["الكل"] + available_locations)
    
    # فلتر نصي للراتب
    search_salary = st.sidebar.text_input("💰 ابحث عن راتب معين (مثال: 4000)")
    
    # تصفية الوظائف (استبعاد وظائف الحج من القسم العام)
    filtered_jobs = [job for job in all_jobs if not job.get('is_hajj')]
    
    if selected_location != "الكل":
        filtered_jobs = [job for job in filtered_jobs if job.get('location') == selected_location]
        
    if search_salary:
        filtered_jobs = [job for job in filtered_jobs if search_salary in str(job.get('salary', ''))]

    # عرض الوظائف بعد الفلترة
    display_jobs(filtered_jobs)

elif page == "🕋 وظائف موسم الحج":
    st.title("🕋 وظائف موسم الحج")
    st.markdown("هذا القسم مخصص حصرياً للفرص الأمنية المؤقتة خلال موسم الحج.") # متطلب 4 و 16
    st.markdown("---")
    
    # تصفية لجلب وظائف الحج فقط (حيث يكون is_hajj = true)
    hajj_jobs = [job for job in all_jobs if job.get('is_hajj')]
    display_jobs(hajj_jobs)

elif page == "🛠️ الدعم الفني":
    st.title("🛠️ قسم الدعم الفني") # متطلب 15
    st.markdown("نحن هنا لمساعدتك! إذا واجهتك أي مشكلة في المنصة أو في تقديم الطلبات، يمكنك التواصل معنا.")
    
    with st.container(border=True):
        st.subheader("📞 تواصل مع إدارة المنصة")
        st.write("أرسل لنا رسالة عبر الواتساب وسنقوم بالرد عليك في أقرب وقت ممكن.")
        
        # ضع رقمك أنت كمدير للمنصة هنا
        admin_number = "966500000000" # غيره لرقمك
        admin_msg = urllib.parse.quote("السلام عليكم، أحتاج مساعدة بخصوص منصة حارس أمن.")
        admin_url = f"https://wa.me/{admin_number}?text={admin_msg}"
        
        st.link_button("💬 محادثة الدعم الفني", admin_url)
