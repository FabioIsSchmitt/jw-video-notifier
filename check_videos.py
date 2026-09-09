#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de Novos Vídeos do JW.ORG via CallMeBot (WhatsApp)
Consulta a API da CDN do JW.ORG e envia notificações para novos vídeos.
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone

# Garante saída UTF-8 no terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Configurações padrão
JW_LANG = os.environ.get("JW_LANG", "T")  # 'T' = Português
API_URL = f"https://b.jw-cdn.org/apis/mediator/v1/categories/{JW_LANG}/LatestVideos?detailed=1&clientType=web"
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

CALLMEBOT_PHONE = os.environ.get("CALLMEBOT_PHONE", "").strip()
CALLMEBOT_APIKEY = os.environ.get("CALLMEBOT_APIKEY", "").strip()


def load_history():
    """Carrega o histórico de vídeos já vistos."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Aviso ao carregar histórico: {e}")
    return {"seen_guids": [], "last_updated": None}


def save_history(history):
    """Salva o histórico atualizado em disco."""
    history["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"Histórico salvo com {len(history['seen_guids'])} vídeos registrados.")


def fetch_latest_videos():
    """Busca a lista de vídeos mais recentes da API do JW.ORG."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    req = urllib.request.Request(API_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                return data.get("category", {}).get("media", [])
            else:
                print(f"Erro na API JW: HTTP {response.status}")
                return []
    except Exception as e:
        print(f"Falha ao consultar API do JW.ORG: {e}")
        return []


def format_date(iso_str):
    """Formata string de data ISO para formato legível no Brasil."""
    if not iso_str:
        return "Recentemente"
    try:
        clean_iso = iso_str.split(".")[0].replace("Z", "")
        dt = datetime.fromisoformat(clean_iso)
        return dt.strftime("%d/%m/%Y às %H:%M")
    except Exception:
        return iso_str


def get_video_link(video):
    """Obtém o link direto de download MP4 ou link no site."""
    files = video.get("files", [])
    mp4_url = None
    for f in files:
        if f.get("mimetype") == "video/mp4" and f.get("progressiveDownloadURL"):
            mp4_url = f.get("progressiveDownloadURL")
            if f.get("label") in ["720p", "480p", "360p"]:
                break
    
    web_url = f"https://www.jw.org/finder?lank=pub-jwb_{JW_LANG}&wtlocale={JW_LANG}"
    return mp4_url if mp4_url else web_url


def send_whatsapp_callmebot(message):
    """Envia mensagem usando a API do CallMeBot (WhatsApp)."""
    if not CALLMEBOT_PHONE or not CALLMEBOT_APIKEY:
        print("Aviso: CALLMEBOT_PHONE ou CALLMEBOT_APIKEY não configurados. Mensagem não enviada via WhatsApp.")
        print(f"--- Prévia da mensagem ---\n{message}\n--------------------------")
        return False

    encoded_text = urllib.parse.quote(message)
    clean_phone = CALLMEBOT_PHONE.replace("+", "").replace(" ", "").replace("-", "")
    url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={CALLMEBOT_APIKEY}"

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp_body = resp.read().decode("utf-8", errors="ignore")
            print(f"CallMeBot resposta (HTTP {resp.status}): {resp_body[:150]}")
            return resp.status == 200
    except urllib.error.HTTPError as e:
        print(f"Erro HTTP CallMeBot: {e.code} - {e.read().decode('utf-8', errors='ignore')}")
        return False
    except Exception as e:
        print(f"Erro ao enviar para CallMeBot: {e}")
        return False


def main():
    print("=== Verificador de Novos Vídeos do JW.ORG ===")
    history = load_history()
    seen_guids = set(history.get("seen_guids", []))

    videos = fetch_latest_videos()
    if not videos:
        print("Nenhum vídeo retornado pela API do JW.ORG.")
        return

    print(f"API retornou {len(videos)} vídeos na lista de mais recentes.")

    # Se for a primeira execução (histórico vazio)
    if not seen_guids:
        print("Primeira execução detectada! Gravando estado inicial dos vídeos para evitar disparos em massa.")
        all_guids = [v.get("guid") for v in videos if v.get("guid")]
        history["seen_guids"] = all_guids
        save_history(history)
        print("Histórico inicial criado com sucesso.")
        return

    # Encontra vídeos novos
    new_videos = []
    for video in videos:
        guid = video.get("guid")
        if guid and guid not in seen_guids:
            new_videos.append(video)

    if not new_videos:
        print("Nenhum vídeo novo encontrado nesta checagem.")
        return

    print(f"🎉 Encontrados {len(new_videos)} novo(s) vídeo(s)!")

    # Notifica os novos vídeos (da publicação mais antiga para a mais recente)
    new_videos.reverse()
    for video in new_videos:
        title = video.get("title", "Sem título")
        pub_date = format_date(video.get("firstPublished"))
        duration = video.get("durationFormattedHHMMSS", "")
        link = get_video_link(video)

        msg_lines = [
            "🎥 *Novo Vídeo Publicado no JW.ORG!*",
            "",
            f"📌 *Título:* {title}",
            f"📅 *Publicado em:* {pub_date}",
        ]
        if duration:
            msg_lines.append(f"⏱ *Duração:* {duration}")
        if link:
            msg_lines.append(f"🔗 *Assistir / Baixar:* {link}")

        msg = "\n".join(msg_lines)
        print(f"Notificando: {title}")
        send_whatsapp_callmebot(msg)

        # Adiciona ao conjunto de vistos
        seen_guids.add(video.get("guid"))

    history["seen_guids"] = list(seen_guids)
    save_history(history)
    print("Verificação concluída com sucesso.")


if __name__ == "__main__":
    main()
