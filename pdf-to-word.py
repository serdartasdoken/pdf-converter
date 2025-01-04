import streamlit as st
from docx2pdf import convert
import os
import zipfile
from io import BytesIO
from PyPDF2 import PdfMerger
import subprocess
from pathlib import Path

def get_working_dir():
    """Çalışma klasörünü oluştur ve yolunu döndür"""
    # Kullanıcının home klasöründe bir çalışma klasörü oluştur
    work_dir = os.path.join(str(Path.home()), "Documents", "pdf_converter_files")
    os.makedirs(work_dir, exist_ok=True)
    return work_dir

def clean_working_dir(work_dir):
    """Çalışma klasörünü temizle"""
    for file in os.listdir(work_dir):
        try:
            file_path = os.path.join(work_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            st.error(f"Dosya silinirken hata: {e}")

def sanitize_filename(filename):
    """Dosya adını güvenli hale getirir"""
    tr_map = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'
    }
    filename = ''.join(tr_map.get(c, c) for c in filename)
    return ''.join(c if c.isalnum() or c in '._- ' else '_' for c in filename)

def convert_to_pdf(file, work_dir):
    """Belgeyi PDF'e dönüştürür"""
    try:
        # Dosya adını düzenle
        safe_filename = sanitize_filename(file.name)
        input_path = os.path.join(work_dir, safe_filename)
        output_path = os.path.splitext(input_path)[0] + '.pdf'
        
        # Dosyayı kaydet
        with open(input_path, 'wb') as f:
            f.write(file.getvalue())
        
        if file.name.endswith('.doc'):
            # LibreOffice ile dönüştür
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', work_dir,
                input_path
            ])
        else:  # .docx
            convert(input_path, output_path)
        
        # PDF'i oku
        with open(output_path, 'rb') as f:
            pdf_data = f.read()
            
        # Kaynak dosyayı temizle
        os.unlink(input_path)
        
        return pdf_data
        
    except Exception as e:
        st.error(f"Dönüştürme hatası: {str(e)}")
        if os.path.exists(input_path):
            os.unlink(input_path)
        return None

def merge_pdfs(pdf_list):
    """PDF dosyalarını birleştirir"""
    try:
        merger = PdfMerger()
        for pdf in pdf_list:
            merger.append(BytesIO(pdf))
            
        output = BytesIO()
        merger.write(output)
        merger.close()
        
        return output.getvalue()
    except Exception as e:
        st.error(f"PDF birleştirme hatası: {str(e)}")
        return None

def main():
    st.title("Belge Dönüştürücü")
    
    # Çalışma klasörünü hazırla
    work_dir = get_working_dir()
    clean_working_dir(work_dir)
    
    tab1, tab2 = st.tabs(["Word -> PDF", "PDF Birleştirici"])
    
    with tab1:
        st.header("Word Dosyalarını PDF'e Dönüştür")
        
        # Çalışma klasörü bilgisi
        st.info(f"Çalışma klasörü: {work_dir}")
        
        # Dosya yükleme
        files = st.file_uploader(
            "Word dosyalarını seçin (.doc, .docx)", 
            type=['doc', 'docx'], 
            accept_multiple_files=True,
            key="word_files"
        )
        
        if files:
            st.write("### Yüklenen Dosyalar")
            file_list = []
            
            for i, file in enumerate(files, 1):
                col1, col2 = st.columns([1, 4])
                with col1:
                    order = st.number_input(
                        "Sıra",
                        min_value=1,
                        max_value=len(files),
                        value=i,
                        key=f"order_{i}"
                    )
                    file_list.append((order, file))
                with col2:
                    st.write(file.name)
                    
            if st.button("PDF'e Dönüştür", key="convert_btn"):
                file_list.sort(key=lambda x: x[0])
                pdfs = []
                zip_buffer = BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w') as zf:
                    for i, (_, file) in enumerate(file_list, 1):
                        with st.spinner(f"Dönüştürülüyor: {file.name}"):
                            pdf_data = convert_to_pdf(file, work_dir)
                            if pdf_data:
                                pdf_name = f"{i:02d}_{os.path.splitext(file.name)[0]}.pdf"
                                zf.writestr(pdf_name, pdf_data)
                                pdfs.append(pdf_data)
                
                if pdfs:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Ayrı PDF'leri İndir (ZIP)",
                            data=zip_buffer.getvalue(),
                            file_name="pdf_dosyalari.zip",
                            mime="application/zip"
                        )
                    
                    with col2:
                        if len(pdfs) > 1:
                            merged_pdf = merge_pdfs(pdfs)
                            if merged_pdf:
                                st.download_button(
                                    "📥 Birleştirilmiş PDF'i İndir",
                                    data=merged_pdf,
                                    file_name="birlestirilmis.pdf",
                                    mime="application/pdf"
                                )
    
    with tab2:
        st.header("PDF Dosyalarını Birleştir")
        pdf_files = st.file_uploader(
            "PDF dosyalarını seçin", 
            type=['pdf'], 
            accept_multiple_files=True,
            key="pdf_files"
        )
        
        if pdf_files:
            st.write("### Yüklenen PDF'ler")
            pdf_list = []
            
            for i, pdf in enumerate(pdf_files, 1):
                col1, col2 = st.columns([1, 4])
                with col1:
                    order = st.number_input(
                        "Sıra",
                        min_value=1,
                        max_value=len(pdf_files),
                        value=i,
                        key=f"pdf_order_{i}"
                    )
                    pdf_list.append((order, pdf))
                with col2:
                    st.write(pdf.name)
            
            if st.button("PDF'leri Birleştir", key="merge_btn"):
                pdf_list.sort(key=lambda x: x[0])
                
                with st.spinner("PDF'ler birleştiriliyor..."):
                    merged_pdf = merge_pdfs([pdf.read() for _, pdf in pdf_list])
                    if merged_pdf:
                        st.download_button(
                            "📥 Birleştirilmiş PDF'i İndir",
                            data=merged_pdf,
                            file_name="birlestirilmis.pdf",
                            mime="application/pdf"
                        )

if __name__ == '__main__':
    st.set_page_config(
        page_title="Belge Dönüştürücü",
        page_icon="📄",
        layout="centered"
    )
    main()
