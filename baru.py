import subprocess
import json
import re
import time
import random
import os

# Konfigurasi Proxy (Diaktifkan jika pengguna memilih)
PROXY_IP = "103.226.139.182"
PROXY_PORT = "8080"
PROXY_USER = "deni"
PROXY_PASS = "fir1234"

def set_proxy():
    """Mengatur proxy jika pengguna memilih mode proxy"""
    os.environ["http_proxy"] = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"
    os.environ["https_proxy"] = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"
    print("🌐 Proxy telah diaktifkan.\n")

def baca_daerah(file_daerah):
    """Membaca daftar daerah dari file"""
    try:
        with open(file_daerah, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"File {file_daerah} tidak ditemukan!")
        return []

def googler_scrape(query):
    """Menjalankan Googler dan mengambil hasil pencarian"""
    try:
        result = subprocess.run(
            ["googler", "-n", "10", query],  # Menggunakan output teks biasa
            capture_output=True, text=True, check=True
        )

        print("\n📌 DEBUG: Output Googler:\n", result.stdout)  # Debugging untuk memastikan output

        # Parsing hasil secara manual tanpa JSON
        domains = set()
        for line in result.stdout.split("\n"):
            match = re.search(r"https?://([\w.-]+)", line)
            if match:
                domain = match.group(1)
                domains.add(domain)

        return list(domains)

    except subprocess.CalledProcessError as e:
        print(f"Error saat menjalankan Googler: {e}")
        return []

def main():
    file_daerah = "daerah.txt"
    hasil_file = "result.txt"

    # Menanyakan pengguna ingin menggunakan proxy atau tidak
    use_proxy = input("Gunakan proxy? (y/n): ").strip().lower()

    if use_proxy == 'y':
        set_proxy()
    else:
        print("🚀 Mode tanpa proxy diaktifkan.\n")

    daerah_list = baca_daerah(file_daerah)

    if not daerah_list:
        print("Daftar daerah kosong atau tidak ditemukan!")
        return

    for daerah in daerah_list:
        print(f"\n🔍 Mencari domain untuk daerah: {daerah}")
        query = f"site:.ac.id stikes '{daerah}' inurl:login.php"
        hasil = googler_scrape(query)

        if hasil:
            print(f"✅ Ditemukan {len(hasil)} domain untuk '{daerah}'")

            # Langsung menyimpan hasil ke file setiap selesai satu daerah
            with open(hasil_file, "a", encoding="utf-8") as f:
                for domain in sorted(hasil):
                    f.write(f"{domain}\n")

            print(f"💾 Hasil untuk '{daerah}' ditambahkan ke {hasil_file}")

        else:
            print(f"❌ Tidak ditemukan domain untuk '{daerah}'")

        # Delay acak antara 15 hingga 120 detik untuk menghindari Google CAPTCHA
        delay = random.uniform(15, 120)
        print(f"⏳ Menunggu {delay:.2f} detik sebelum pencarian berikutnya...")
        time.sleep(delay)

    print(f"\n🎯 Semua hasil tersimpan di '{hasil_file}'")

if __name__ == "__main__":
    main()
