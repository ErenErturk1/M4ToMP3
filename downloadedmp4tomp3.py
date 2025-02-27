import os
import yt_dlp
import urllib

def ensure_downloads_folder():
    downloads_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)
    return downloads_path

def convert_to_mp3(file_path, downloads_path):
    try:
        # Windows dosya yolundaki \ işaretlerini / ile değiştir
        file_path = file_path.replace("\\", "/")
        
        # Dosya yolunu URL formatına dönüştür
        file_url = urllib.request.pathname2url(file_path)
        file_url = f"file://{file_url}"
        
        # MP3 formatında dönüştürme işlemi için gerekli ayarlar
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': False,
            'force_generic_extractor': True,
            'enable_file_urls': True  # file:// URL'lerini etkinleştir
        }
        
        # Video dosyasını dönüştürmek için ytdlp kullan
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([file_url])
        
        print(f"Dönüştürme tamamlandı: {file_path}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    downloads_path = ensure_downloads_folder()
    
    num_files = int(input("Kaç video dosyasını dönüştürmek istiyorsunuz? = "))
    
    for i in range(num_files):
        file_path = input(f"{i+1}. Video dosyasının tam yolunu girin (ör. C:/dosya/yol/video.mp4): ")
        
        if os.path.exists(file_path):
            convert_to_mp3(file_path, downloads_path)
        else:
            print(f"Dosya bulunamadı: {file_path}")
    
    print("Tüm işlemler tamamlandı!")
