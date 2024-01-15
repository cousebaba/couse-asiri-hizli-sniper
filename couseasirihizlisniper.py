import requests
import threading
import time

TOKEN = "örnek_token"
WEBHOOK = "örnek_webhook"
GUILD_ID = "örnek_guild_id"
VANITY_URL = "örnek_vanity_url" # Dostlar Burayı Doldurmanıza Gerek Yok Zaten Sniper'i Çalıştırdığınızda Quest (Soru) Olarak Gelecektir.

headers = {
    "authorization": TOKEN,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36", #örnek user-agent istege gore degisebilirsiniz.
}

def change_vanity():
    payload = {"code": VANITY_URL}
    response = requests.patch(
        f"https://discord.com/api/v10/guilds/{GUILD_ID}/vanity-url",
        headers=headers,
        json=payload,
        timeout=5  # Timeout süresini belirle (örneğin 5 saniye) fakat thread için.
    )
    if response.status_code == 200:
        elapsed_time = time.time() - start_time
        print("\x1b[36mURL değiirildi:", VANITY_URL, "- Süre (Bu Ms Değildir Toplam Geçen Süre Mili Saniye Cinsinden.):", f"{elapsed_time * 1000:.2f} milisaniye\x1b[0m")
        data = {
            "content": f"@everyone discord.gg/{VANITY_URL} omg dostum artık senin!",
            "username": "couse1988",
            "avatar_url": "https://cdn.discordapp.com/attachments/1078000713914921043/1084384416228454460/lol.png",
        }
        requests.post(WEBHOOK, json=data)
        time.sleep(2)
        exit()
    else:
        print("\x1b[36mVanity URL değiştirilemedi, hata kodu:", response.status_code, "\x1b[0m")

def check_vanity():
    start_time = time.time()
    while True:
        if not VANITY_URL:
            print("\x1b[36mVanity URL boşta, yeni bir URL bekleniyor...\x1b[0m")
        else:
            try:
                response = requests.get(
                    f"https://discord.com/api/v9/invites/{VANITY_URL}?with_counts=true&with_expiration=true",
                    headers=headers,
                    timeout=5  # Timeout süresini belirle (örneğin 5 saniye) buda rate limitten kaçınmayı saglar, ve daha kontrollu olur. (arttırılrsa.)
                )
                elapsed_time = time.time() - start_time  

                if response.status_code == 404:
                    print("\x1b[36mVanity URL değiştirliyor:", VANITY_URL, "\x1b[0m")
                    change_vanity()
                else:
                    print("\x1b[36mVanity URL hala aktif (bu hızı değil geçen süre milisaniye cinsinden.):", VANITY_URL, "- Süre:", f"{elapsed_time * 1000:.2f} milisaniye\x1b[0m")

                    # Hız Kontrolü, Rate Limit İçin.
                    if elapsed_time < 0.2:
                        print("\x1b[32mHızlı bir şekilde elde edildi!\x1b[0m")
                        break
            except requests.Timeout:
                print("\x1b[36mistek zaman aşımına uğradı, tekrar deneniyor...\x1b[0m")

        time.sleep(0.01)  

if __name__ == "__main__":
    VANITY_URL = input("\x1b[36mistediğiniz Vanity URL'yi girin:\x1b[0m ") # burda ilk baştakini doldurmak zorunda değilsiniz, zaten sniper çalıştığında soracaktır.
    
    # 35 Thread Kullandım, Ben Hızı Artırmak İsterseniz 20 vb. yapabilirsiniz.
    threads = []
    for _ in range(35):
        vanity_thread = threading.Thread(target=check_vanity)
        threads.append(vanity_thread)
        vanity_thread.start()

    for thread in threads:
        thread.join()
