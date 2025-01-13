import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp

# Telegram bot token'ınızı buraya yapıştırın
TOKEN = '7776707741:AAF_ZKRfjt-yGn2fYJVwXfCQZtg95vaAxDA'

# Logging ayarları
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Video ve MP3 indirme fonksiyonu
def download_tiktok_video(url: str, file_format: str = 'mp4'):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    
    if file_format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioquality': 1,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        return file_name

# Start komutu
async def start(update: Update, context) -> None:
    await update.message.reply_text('Salam! Mənim adım TikBotdur. TikTok video faylını yükləmək üçün link daxil edin ☻')

# TikTok video indirme komutu
async def download(update: Update, context) -> None:
    url = update.message.text.strip()

    # URL'nin geçerli bir TikTok bağlantısı olup olmadığını kontrol et
    if 'tiktok.com' not in url:
        await update.message.reply_text("Zəhmət olmasa doğru linki daxil edin!")
        return

    try:
        await update.message.reply_text("Yükləmə başladı... Zəhmət olmasa biraz gözləyin ♥")

        # Video veya MP3 indirme
        file_name = download_tiktok_video(url)

        # İndirilen dosyayı kullanıcıya gönder
        with open(file_name, 'rb') as video:
            await update.message.reply_video(video)
             # Video gönderildikten sonra reply mesajı gönder
        await update.message.reply_text("Videonuz göndərildi, xidmətimizdən istifadə etdiyiniz üçün minnətdaram! 👍")

    except Exception as e:
        await update.message.reply_text(f"Bir xəta baş verdi, narahat olmayın indi həll edirəm: {e}")

# Main fonksiyonu
def main() -> None:
    # Updater ve Dispatcher yerine Application kullanılıyor
    application = Application.builder().token(TOKEN).build()

    # CommandHandler ve MessageHandler ekliyoruz
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    # Botu başlat
    application.run_polling()

if __name__ == '__main__':
    main()
