# audio_scraper_module.py
# Module Python pour créer un "GitHub audio scraper repo" à usage web/app

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os


def is_audio_file(url: str) -> bool:
    """Détecte si une URL correspond à un fichier audio."""
    audio_exts = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac']
    parsed_url = urlparse(url)
    return any(parsed_url.path.lower().endswith(ext) for ext in audio_exts)


def is_pdf_file(url: str) -> bool:
    """Vérifie si une URL correspond à un fichier PDF."""
    parsed_url = urlparse(url)
    return parsed_url.path.lower().endswith('.pdf')


def scrape_files(site_url: str, mode: str = "audio"):
    """Explore le site web pour récupérer les fichiers audio ou PDF."""
    try:
        response = requests.get(site_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for tag in soup.find_all(['a', 'audio', 'source']):
            src = tag.get('href') or tag.get('src')
            if not src:
                continue
            full_url = urljoin(site_url, src)
            if mode == "audio" and is_audio_file(full_url):
                links.append(full_url)
            if mode == "pdf" and is_pdf_file(full_url):
                links.append(full_url)

        return list(set(links))
    except Exception as e:
        print(f"Erreur pendant le scraping : {e}")
        return []


def download_files(urls, output_dir="downloads"):
    """Télécharge les fichiers trouvés."""
    os.makedirs(output_dir, exist_ok=True)
    downloaded = []
    for url in urls:
        try:
            filename = os.path.basename(urlparse(url).path)
            filepath = os.path.join(output_dir, filename)
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            downloaded.append(filepath)
        except Exception as e:
            print(f"Erreur téléchargement {url} : {e}")
    return downloaded


if __name__ == "__main__":
    test_url = "https://podcasts.leparisien.fr/le-parisien-code-source/"
    audios = scrape_files(test_url, mode="audio")
    print("Trouvés:", audios)
    files = download_files(audios)
    print("Téléchargés:", files)
