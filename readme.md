# PDF Dönüştürücü ve Birleştirici

Word dosyalarını (.doc ve .docx) PDF'e dönüştürün ve PDF dosyalarını birleştirin.

## Özellikler

- Word (.doc, .docx) dosyalarını PDF'e dönüştürme
- Birden fazla PDF dosyasını birleştirme
- Dosya sıralama özelliği
- Kolay kullanımlı arayüz
- Türkçe karakter desteği

## Kurulum

1. Gerekli Python kütüphanelerini yükleyin:
```bash
pip install -r requirements.txt
```

2. macOS kullanıcıları için LibreOffice gereklidir (.doc dosyaları için):
```bash
brew install libreoffice
```

## Başlatma

```bash
streamlit run pdf_converter.py
```

## Kullanım

1. "Word -> PDF" sekmesini kullanarak:
   - Word dosyalarınızı yükleyin
   - Sıralarını ayarlayın (isteğe bağlı)
   - "PDF'e Dönüştür" butonuna tıklayın
   - Dönüştürülen dosyaları tek tek veya birleştirilmiş olarak indirin

2. "PDF Birleştirici" sekmesini kullanarak:
   - PDF dosyalarınızı yükleyin
   - Sıralarını ayarlayın
   - "PDF'leri Birleştir" butonuna tıklayın
   - Birleştirilmiş PDF'i indirin

## Notlar

- İşlemler lokal olarak yapılır, dosyalarınız güvende
- Dönüştürme işlemi için internet bağlantısı gerekmez
- .doc dosyaları için LibreOffice gereklidir

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.