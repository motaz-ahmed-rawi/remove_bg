import streamlit as st
from PIL import Image
from rembg import remove
import random
import os

# Dil seçenekleri
LANGUAGES = {
    "en": {"title": "Background Remover", "upload": "Upload an image file", "download": "Download the image", "loaded_image": "Uploaded Image", "processed_image": "Image without Background"},
    "tr": {"title": "Arka Plan Kaldırıcı", "upload": "Bir resim dosyası yükleyin", "download": "Resmi İndir", "loaded_image": "Yüklenen Resim", "processed_image": "Arka Plansız Resim"},
    "ar": {"title": "إزالة الخلفية", "upload": "حمّل صورة", "download": "تنزيل الصورة", "loaded_image": "الصورة المرفوعة", "processed_image": "الصورة بدون خلفية"}
}

# Varsayılan dil İngilizce
language = st.sidebar.selectbox("Choose a language / Dil seçin / اختر لغة", ("en", "tr", "ar"))

# Seçilen dile göre metinleri alma
text = LANGUAGES[language]

# Streamlit başlığı ve açıklaması
st.title(text["title"])
st.write(text["upload"])

# Kullanıcıdan resim yüklemesini iste
uploaded_file = st.file_uploader(text["upload"], type=["jpg", "jpeg", "png"])

# Kullanıcıdan bir çıktı klasörü seçmesini sağlayan fonksiyon
def get_random_filename(extension="png"):
    """Rastgele 4 haneli bir dosya adı oluşturur."""
    random_name = f"{random.randint(1000, 9999)}.{extension}"
    return random_name

# Arka plan kaldırma işlemini yapan fonksiyon
def process_image(input_image):
    output_image = remove(input_image)  # Arka plansız resmi oluşturma
    return output_image

# Eğer kullanıcı bir dosya yüklediyse
if uploaded_file is not None:
    # Orijinal resmi göster
    st.image(uploaded_file, caption=text["loaded_image"], use_column_width=True)

    # Arka planı kaldır
    input_image = Image.open(uploaded_file)
    output_image = process_image(input_image)

    # Arka plansız resmi göster
    st.image(output_image, caption=text["processed_image"], use_column_width=True)

    # Kullanıcıya dosyayı indirme seçeneği sun
    output_name = get_random_filename()
    
    # Geçici olarak kaydetmek için bir dosya oluşturup ardından indirme bağlantısı sunma
    output_path = os.path.join(os.getcwd(), output_name)
    output_image.save(output_path)
    
    with open(output_path, "rb") as file:
        btn = st.download_button(
            label=text["download"],
            data=file,
            file_name=output_name,
            mime="image/png"
        )

# Streamlit logolarını ve markalarını gizlemek için tema ayarı
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
