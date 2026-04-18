# Elveron-FishBot
# 🎣 FishBot

FishBotV1, Elveron adlı Metin2 Private sunucusu için OpenCV ve PyQt6 kullanılarak geliştirilmiş gerçek zamanlı bir otomatik balık yakalama botudur.
Ekrandaki oyun penceresini analiz ederek balık ve hedef bölgeyi tespit eder ve otomatik olarak input (SPACE) gönderir.

---

## 🚀 Özellikler

* 🎯 Gerçek zamanlı görüntü işleme (OpenCV)
* 🧠 Template matching ile balık tespiti
* 🎮 Otomatik input (keyboard simulation)
* 🖥️ PyQt6 GUI arayüz
* ⚡ Düşük gecikmeli thread yapısı
* 🔍 Debug overlay desteği

---

## 📁 Proje Yapısı

```
FishBotV1/
│
├── main.py          # Uygulama giriş noktası
├── gui.py           # Arayüz (PyQt6)
├── worker.py        # Bot thread ve logic
├── vision.py        # Görüntü işleme
├── screen.py        # Ekran capture
├── space_input.py   # Klavye input
├── fish.png         # Template image
└── README.md
```

---

## ⚙️ Kurulum

### 1. Python yükle

Python 3.10+ önerilir

### 2. Bağımlılıkları kur

```bash
pip install opencv-python numpy pyqt6 mss pygetwindow pywin32
```

---

## ▶️ Çalıştırma

```bash
python main.py
```

* Oyunu aç
* Botu başlat (START)
* Bot otomatik çalışır

---

## 🧪 Nasıl Çalışır?

1. Ekran yakalanır (`screen.py`)
2. Balık template ile bulunur (`vision.py`)
3. Hedef bölge analiz edilir
4. Çakışma durumunda SPACE basılır (`space_input.py`)
5. Tüm süreç ayrı thread’de çalışır (`worker.py`)

---

## 🖥️ EXE Haline Getirme

### 1. PyInstaller yükle

```bash
pip install pyinstaller
```

### 2. Build al

```bash
pyinstaller --onefile --noconsole main.py
```

### 3. Çıktı

```
dist/main.exe
```

---

## ⚠️ Notlar

* Oyun penceresi adı: **Elveron** olmalı
* Çözünürlük değişirse detection bozulabilir
* `fish.png` doğru klasörde olmalı

---

## 🧑‍💻 Geliştirici Notu

Bu proje eğitim ve deney amaçlı geliştirilmiştir.
Gerçek zamanlı görüntü işleme ve otomasyon sistemleri üzerine çalışmak için iyi bir örnektir.

---

## 📜 Lisans

MIT License
