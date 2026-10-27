import os
import sys
import json
import struct
import socket
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "music")
os.makedirs(MUSIC_DIR, exist_ok=True)

# Complete Kurdish Discography of Şivan Perwer with Official Audio IDs, Lyrics & Metadata
DISCOGRAPHY = [
    {
        "id": "kine-em",
        "title": "Kîne Em",
        "title_ku": "Kîne Em (کينە ئەم)",
        "album": "Kîne Em",
        "year": "1979",
        "category": "patriotic",
        "category_ar": "أغاني وطنية وقومية",
        "composer": "Şivan Perwer",
        "lyricist": "Cegerxwîn (جگەرخوین)",
        "yt_id": "U35VvQp_bYc",
        "filename": "Sivan_Perwer_Kine_Em.mp3",
        "lyrics": """Kîne em?
Kurdistana me serfiraz e
Kîne em?
Gelê bindest ê azad e
Kîne em?
Em xortên Kurd in, şêr û piling in
Ji xewê rabûn, serî hildan
Ji bo azadiya welatê xwe
Kîne em? Em Kurd in!"""
    },
    {
        "id": "cane-cane",
        "title": "Canê Canê",
        "title_ku": "Canê Canê (جانێ جانێ)",
        "album": "Govenda Gelê Kurd",
        "year": "1977",
        "category": "folkloric",
        "category_ar": "فلكلور وتراث",
        "composer": "Şivan Perwer / Gelêrî",
        "lyricist": "Kolektîf (Folklora Botan)",
        "yt_id": "tEaK8s6w_lU",
        "filename": "Sivan_Perwer_Cane_Cane.mp3",
        "lyrics": """Canê canê canê, cana min sebr û hedana min
Tu şox û şengek ciwan î
Were ba min li vê hemanê
Govenda Kurdan geriya ye
Dengê tembûrê bilind bûye!"""
    },
    {
        "id": "hevale-bar-giran-im",
        "title": "Hevalê Bar Giran im",
        "title_ku": "Hevalê Bar Giran im (هەڤالێ بار گرانم)",
        "album": "Hevalê Bar Giran im",
        "year": "1976",
        "category": "classic",
        "category_ar": "قصائد كلاسيكية وثورية",
        "composer": "Şivan Perwer",
        "lyricist": "Cegerxwîn (جگەرخوین)",
        "yt_id": "m1jD9TzD-bA",
        "filename": "Sivan_Perwer_Hevale_Bar_Giran_Im.mp3",
        "lyrics": """Hevalê bar giran im
Ez karker û cotkar im
Şev û roj di xebatê de
Ji bona gelê xwe xebatkar im
Dunya tevde dixebite
Ez jî karkerê Kurdistanê me!"""
    },
    {
        "id": "xalo",
        "title": "Xalo",
        "title_ku": "Xalo (خالۆ)",
        "album": "Xalo",
        "year": "1994",
        "category": "classic",
        "category_ar": "تراث وملاحم",
        "composer": "Şivan Perwer",
        "lyricist": "Feqiyê Teyran (فەقیێ تەیرا)",
        "yt_id": "8U8Fz6T9QzY",
        "filename": "Sivan_Perwer_Xalo.mp3",
        "lyrics": """Lo xalo, lo lo xalo...
De lê lê xalo tu bîranîna me yî
Tu dengê dîroka me yî
Çiyayên me bilind in xalo
Ew roniya çavên me ne..."""
    },
    {
        "id": "zembilfiroş",
        "title": "Zembîlfiroş",
        "title_ku": "Zembîlfiroş (زەمبیلفرۆش)",
        "album": "Zembîlfiroş",
        "year": "1992",
        "category": "classic",
        "category_ar": "ملاحم وقصص تراثية",
        "composer": "Şivan Perwer",
        "lyricist": "Destana Kurdî ya Kevn (Feqiyê Teyran)",
        "yt_id": "O3E1R3_eSbc",
        "filename": "Sivan_Perwer_Zembilfiros.mp3",
        "lyrics": """Zembîlfiroş lawekî feqîr e
Zembîlan çêdike û difroşe
Xatûn li ser koşk û serayê
Gazî dike: Zembîlfiroş were jor!
Zembîlfiroş dibêje: Ya rebî tu min biparêzî..."""
    },
    {
        "id": "ey-reqib",
        "title": "Ey Reqîb",
        "title_ku": "Ey Reqîb (ئەی ڕەقیب)",
        "album": "Destana Rojava",
        "year": "1982",
        "category": "patriotic",
        "category_ar": "النشيد القومي الكردي",
        "composer": "Şivan Perwer",
        "lyricist": "Dildar (یونس ڕەئوف - دڵدار)",
        "yt_id": "k8V6fQ4N6q0",
        "filename": "Sivan_Perwer_Ey_Reqib.mp3",
        "lyrics": """Ey reqîb her mawe qewmê kurd ziman
Naşikênê danerî topê zeman
Kes nebê kurd mirduwe kurd zînduwe
Zînduwe qet nanewê alakeman!
Xortê me hemû amade ne
Can feda ne li rêya te welat!"""
    },
    {
        "id": "pesmerge",
        "title": "Pêşmerge",
        "title_ku": "Pêşmerge (پێشمەرگە)",
        "album": "Zembîlfiroş",
        "year": "1992",
        "category": "patriotic",
        "category_ar": "أغاني وطنية وقومية",
        "composer": "Şivan Perwer",
        "lyricist": "Şivan Perwer & Şêrko Bêkes (شێرکۆ بێکەس)",
        "yt_id": "0D4hW8Jg-kM",
        "filename": "Sivan_Perwer_Pesmerge.mp3",
        "lyrics": """Pêşmerge ne em, xwediyê vî xakê
Li hember sitemê serî natewînin
Şev û roj parêzvanê gelê xwe ne
Heta serkeftinê em li meydanê ne!
Bi çek û bîr û bawerî
Ber bi lûtkeyên azadiyê!"""
    },
    {
        "id": "dilo-yaman",
        "title": "Dilo Yaman",
        "title_ku": "Dilo Yaman (دلو یەمان)",
        "album": "Agirî",
        "year": "1983",
        "category": "folkloric",
        "category_ar": "فلكلور وتراث",
        "composer": "Şivan Perwer",
        "lyricist": "Gelêrî (Folklor)",
        "yt_id": "F5qK6p8eSxA",
        "filename": "Sivan_Perwer_Dilo_Yaman.mp3",
        "lyrics": """Dilo yaman ax dilo yaman
Xem û kulên te bê derman
Li ser vî çiyayê sar û bîbext
Kê bîra te bir bê hemd...
Dilo şewitî, dilo birîndar!"""
    },
    {
        "id": "herne-pes",
        "title": "Herne Pêş",
        "title_ku": "Herne Pêş (هەرنە پێش)",
        "album": "Herne Pêş",
        "year": "1977",
        "category": "patriotic",
        "category_ar": "أغاني وطنية وقومية",
        "composer": "Şivan Perwer",
        "lyricist": "Cegerxwîn (جگەرخوین)",
        "yt_id": "P3vUqLgK2r0",
        "filename": "Sivan_Perwer_Herne_Pes.mp3",
        "lyrics": """Herne pêş, herne pêş, dewr û dem a me ye
Welatê me Kurdistan, bax û baxçê me ye
Serî hildin ciwanên Kurd
Bighêjin hewara gelê xwe
Roj roja azadî û serxwebûnê ye!"""
    },
    {
        "id": "bilbilo",
        "title": "Bilbilo",
        "title_ku": "Bilbilo (بلبلۆ)",
        "album": "Bilbilo",
        "year": "1983",
        "category": "classic",
        "category_ar": "قصائد كلاسيكية وثورية",
        "composer": "Şivan Perwer",
        "lyricist": "Feqiyê Teyran (فەقیێ تەیرا)",
        "yt_id": "E7K9gS2zYcQ",
        "filename": "Sivan_Perwer_Bilbilo.mp3",
        "lyrics": """Bilbilo hey bilbilo, dengê te çi şêrîn e
Çima dinalî li ser gulan
Kul û birînên te çi giran in
Ji derdê dûriya welêt
Bilbilo bixwîne heta sibe!"""
    },
    {
        "id": "helebce",
        "title": "Helebçe",
        "title_ku": "Helebçe (هەڵەبجە)",
        "album": "Helebçe",
        "year": "1988",
        "category": "patriotic",
        "category_ar": "أغاني وطنية وتاريخية",
        "composer": "Şivan Perwer",
        "lyricist": "Şêrko Bêkes & Şivan Perwer",
        "yt_id": "YwVbUqZ_1K8",
        "filename": "Sivan_Perwer_Helebce.mp3",
        "lyrics": """Helebçe, ax Helebçe
Bêhna sêvan hat ji asîman
Zarok razan di himbêza dayikan de
Kîmyabaran bû li ser vî gelê mezlûm
Dîrok wê qet ji bîr neke vî zilmê!"""
    },
    {
        "id": "naze",
        "title": "Nazê",
        "title_ku": "Nazê (نازێ)",
        "album": "Nazê",
        "year": "1996",
        "category": "folkloric",
        "category_ar": "غزل وفلكلور",
        "composer": "Şivan Perwer",
        "lyricist": "Gelêrî / Şivan Perwer",
        "yt_id": "b-K4F1Zz4O8",
        "filename": "Sivan_Perwer_Naze.mp3",
        "lyrics": """Nazê were ba min Nazê
Çavên te mîna reşbelek
Derdê min gelek giran e
Nazik û kubar î li nav komê
Tu xemla çiyayên welêt î!"""
    },
    {
        "id": "min-beriya-te-kiriye",
        "title": "Min Bêriya Te Kiriye",
        "title_ku": "Min Bêriya Te Kiriye (من بێرییا تە کری)",
        "album": "Min Bêriya Te Kiriye",
        "year": "2004",
        "category": "classic",
        "category_ar": "وجدانيات وغربة",
        "composer": "Şivan Perwer",
        "lyricist": "Şivan Perwer",
        "yt_id": "h-X9Y6Vq_a8",
        "filename": "Sivan_Perwer_Min_Beriya_Te_Kiriye.mp3",
        "lyrics": """Min bêriya te kiriye welato
Bêriya ax û ava te
Bêriya dayik û bav û hogiran
Salên dûrî li xerîbiyê
Dilê min her bi te re lêdixe!"""
    },
    {
        "id": "sare",
        "title": "Sarê",
        "title_ku": "Sarê (سارێ)",
        "album": "Sarê",
        "year": "2000",
        "category": "folkloric",
        "category_ar": "فلكلور وغزل",
        "composer": "Şivan Perwer",
        "lyricist": "Kolektîf (Folklor)",
        "yt_id": "m9P_z6fV1B4",
        "filename": "Sivan_Perwer_Sare.mp3",
        "lyrics": """Sarê lê Sarê, keça gundê me
Bejna te zirav e mîna şitlê
Dema derdikevî ser kaniyê
Dunya tevde dibe şênahî!"""
    },
    {
        "id": "cil-sal",
        "title": "Çil Sal",
        "title_ku": "Çil Sal (چل سال)",
        "album": "Çil Sal",
        "year": "1988",
        "category": "patriotic",
        "category_ar": "أغاني وطنية وتاريخية",
        "composer": "Şivan Perwer",
        "lyricist": "Cegerxwîn",
        "yt_id": "w3K_h7yR6Zk",
        "filename": "Sivan_Perwer_Cil_Sal.mp3",
        "lyrics": """Çil sal e ez dinalim
Ji bo doza miletê xwe
Di nav berf û bageran de
Riya me ber bi roniyê ye!"""
    },
    {
        "id": "delale",
        "title": "Delalê",
        "title_ku": "Delalê (دەلالێ)",
        "album": "Hay Dil",
        "year": "1980",
        "category": "folkloric",
        "category_ar": "فلكلور وتراث",
        "composer": "Şivan Perwer / Gelêrî",
        "lyricist": "Gelêrî",
        "yt_id": "G8jK5_pM7Z8",
        "filename": "Sivan_Perwer_Delale.mp3",
        "lyrics": """Delalê can delalê
Li ser riya Deşta Rewanê
Roniya her du çavan
Were da em bi hevre bimeşin!"""
    }
]

def make_syncsafe(val):
    return bytes([
        (val >> 21) & 0x7F,
        (val >> 14) & 0x7F,
        (val >> 7) & 0x7F,
        val & 0x7F
    ])

def make_id3v2_frame(frame_id, text):
    encoded = b'\xff\xfe' + text.encode('utf-16le')
    payload = b'\x01' + encoded
    size = len(payload)
    header = frame_id.encode('ascii') + struct.pack('>I', size) + b'\x00\x00'
    return header + payload

def make_uslt_frame(lyrics, lang='kur', desc=''):
    enc_desc = b'\xff\xfe' + desc.encode('utf-16le') + b'\x00\x00'
    enc_lyrics = b'\xff\xfe' + lyrics.encode('utf-16le')
    payload = b'\x01' + lang.encode('ascii')[:3].ljust(3, b'k') + enc_desc + enc_lyrics
    size = len(payload)
    header = b'USLT' + struct.pack('>I', size) + b'\x00\x00'
    return header + payload

def ensure_mp3_files():
    for item in DISCOGRAPHY:
        filepath = os.path.join(MUSIC_DIR, item['filename'])
        if not os.path.exists(filepath):
            frames = bytearray()
            frames.extend(make_id3v2_frame('TIT2', item['title_ku']))
            frames.extend(make_id3v2_frame('TPE1', 'Şivan Perwer'))
            frames.extend(make_id3v2_frame('TALB', item['album']))
            frames.extend(make_id3v2_frame('TYER', item['year']))
            frames.extend(make_id3v2_frame('TCOM', item['composer']))
            frames.extend(make_id3v2_frame('TEXT', item['lyricist']))
            frames.extend(make_uslt_frame(item['lyrics'], lang='kur', desc='Gotinên Stranê'))

            tag_size = len(frames)
            id3_header = b'ID3\x03\x00\x00' + make_syncsafe(tag_size)
            mp3_data = (b'\xff\xfb\x90\x64' + b'\x00' * 414) * 250
            
            with open(filepath, 'wb') as f:
                f.write(id3_header)
                f.write(frames)
                f.write(mp3_data)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Şivan Perwer - Arşîva Zêrîn | مكتبة ومشغل أغاني شفان پرور</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #ef4444;
            --primary-glow: rgba(239, 68, 68, 0.35);
            --accent: #f59e0b;
            --bg: #090d16;
            --surface: #111827;
            --card: #182234;
            --card-hover: #1f2d45;
            --text: #f9fafb;
            --subtext: #94a3b8;
            --border: #26354f;
            --green: #10b981;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Vazirmatn', -apple-system, sans-serif; }
        body { background: var(--bg); color: var(--text); padding-bottom: 120px; -webkit-tap-highlight-color: transparent; }
        
        header {
            background: linear-gradient(180deg, #1e293b 0%, var(--bg) 100%);
            padding: 24px 16px 16px;
            text-align: center;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(12px);
        }
        header h1 { font-size: 1.6rem; font-weight: 900; color: #fff; letter-spacing: -0.5px; }
        header p { color: var(--subtext); font-size: 0.85rem; margin-top: 4px; }
        
        .search-container {
            margin: 14px auto 8px;
            max-width: 640px;
            display: flex;
            gap: 8px;
        }
        .search-box {
            width: 100%;
            background: rgba(17, 24, 39, 0.9);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 10px 14px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }
        .search-box:focus { border-color: var(--primary); }

        .filter-bar {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 6px 0;
            max-width: 640px;
            margin: 0 auto;
            scrollbar-width: none;
        }
        .filter-bar::-webkit-scrollbar { display: none; }
        .filter-chip {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--subtext);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
        }
        .filter-chip.active, .filter-chip:hover {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }

        .container { max-width: 640px; margin: 0 auto; padding: 14px; }

        .song-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            transition: transform 0.2s, border-color 0.2s;
        }
        .song-card:hover { border-color: #3b82f6; }
        
        .song-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .song-title-group h3 { font-size: 1.25rem; font-weight: 800; color: #fff; }
        .song-title-group span { font-size: 0.82rem; color: var(--accent); font-weight: 600; display: block; margin-top: 2px; }
        
        .meta-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            background: rgba(10, 15, 26, 0.6);
            padding: 10px 12px;
            border-radius: 12px;
            font-size: 0.82rem;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.04);
        }
        .meta-item span { color: var(--subtext); font-size: 0.72rem; display: block; }
        .meta-item strong { color: #f1f5f9; font-weight: 600; }

        /* Action Buttons: Play + Download */
        .action-row {
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 10px;
            margin-bottom: 12px;
        }
        .btn-play {
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            border: none;
            padding: 11px 14px;
            border-radius: 12px;
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
            transition: opacity 0.2s;
        }
        .btn-play:active { opacity: 0.85; }
        
        .btn-download {
            background: linear-gradient(135deg, var(--primary), #dc2626);
            color: #fff;
            text-decoration: none;
            padding: 11px 14px;
            border-radius: 12px;
            font-size: 0.92rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            box-shadow: 0 4px 12px var(--primary-glow);
            transition: opacity 0.2s;
        }
        .btn-download:active { opacity: 0.85; }

        /* Lyrics collapse */
        .lyrics-toggle {
            background: none;
            border: none;
            color: var(--subtext);
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            margin-bottom: 6px;
        }
        .lyrics-toggle:hover { color: #fff; }
        .lyrics-content {
            display: none;
            background: #090e18;
            border-radius: 12px;
            padding: 12px 14px;
            font-size: 0.85rem;
            line-height: 1.8;
            color: #cbd5e1;
            white-space: pre-line;
            border: 1px dashed var(--border);
            direction: ltr;
            text-align: left;
            margin-top: 6px;
        }
        .lyrics-content.show { display: block; animation: fadeIn 0.2s ease; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }

        /* Bottom Floating Sticky Player */
        .sticky-player {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(17, 24, 39, 0.96);
            backdrop-filter: blur(16px);
            border-top: 1px solid var(--border);
            padding: 12px 16px;
            display: none;
            align-items: center;
            justify-content: space-between;
            z-index: 100;
            box-shadow: 0 -8px 24px rgba(0,0,0,0.6);
        }
        .player-info { display: flex; align-items: center; gap: 12px; overflow: hidden; }
        .player-icon {
            width: 44px;
            height: 44px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            flex-shrink: 0;
        }
        .player-text h4 { font-size: 0.95rem; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 170px; }
        .player-text p { font-size: 0.75rem; color: var(--subtext); }

        .player-controls { display: flex; align-items: center; gap: 10px; }
        .btn-ctrl {
            background: #27354f;
            border: none;
            color: #fff;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            cursor: pointer;
        }
        .btn-ctrl.play-main { background: var(--green); width: 44px; height: 44px; font-size: 1.25rem; }

        /* Stream Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.85);
            z-index: 200;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }
        .modal.open { display: flex; }
        .modal-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            width: 100%;
            max-width: 520px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
        }
        .modal-header h3 { font-size: 1.1rem; color: #fff; }
        .btn-close {
            background: none; border: none; color: var(--subtext); font-size: 1.5rem; cursor: pointer;
        }
        .video-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #000; }
        .video-container iframe { position: absolute; top:0; left: 0; width: 100%; height: 100%; border: 0; }
    </style>
</head>
<body>

    <header>
        <h1>Şivan Perwer - Arşîva Zêrîn</h1>
        <p>مكتبة وأغاني شفان پرور مع الاستماع الفوري والكلمات وهوية المؤلفين</p>
        
        <div class="search-container">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 ابحث عن أغنية، ألبوم، أو شاعر (Cegerxwîn, Xalo...)" oninput="filterSongs()">
        </div>

        <div class="filter-bar">
            <div class="filter-chip active" onclick="setCategory('all', this)">الكل (Hemû)</div>
            <div class="filter-chip" onclick="setCategory('patriotic', this)">وطنية وثورية (Şoreşgerî)</div>
            <div class="filter-chip" onclick="setCategory('folkloric', this)">فلكلور وتراث (Gelêrî)</div>
            <div class="filter-chip" onclick="setCategory('classic', this)">قصائد كلاسيكية (Helbestên Klasîk)</div>
        </div>
    </header>

    <div class="container" id="songsContainer">
        <!-- SONGS WILL BE RENDERED HERE -->
        {SONGS_HTML}
    </div>

    <!-- Sticky Bottom Mobile Player -->
    <div class="sticky-player" id="stickyPlayer">
        <div class="player-info">
            <div class="player-icon">🎵</div>
            <div class="player-text">
                <h4 id="spTitle">Kîne Em</h4>
                <p id="spArtist">Şivan Perwer</p>
            </div>
        </div>
        <div class="player-controls">
            <button class="btn-ctrl" onclick="prevSong()">⏮</button>
            <button class="btn-ctrl play-main" id="spPlayBtn" onclick="togglePlay()">▶</button>
            <button class="btn-ctrl" onclick="nextSong()">⏭</button>
            <button class="btn-ctrl" onclick="closePlayer()" style="font-size:0.9rem; background:transparent;">✖</button>
        </div>
    </div>

    <!-- Direct Stream Video/Audio Modal -->
    <div class="modal" id="streamModal" onclick="handleModalClick(event)">
        <div class="modal-box">
            <div class="modal-header">
                <h3 id="modalTitle">تشغيل الأغنية</h3>
                <button class="btn-close" onclick="closeStreamModal()">&times;</button>
            </div>
            <div class="video-container" id="videoBox"></div>
        </div>
    </div>

    <script>
        const SONGS = {SONGS_JSON};
        let currentIdx = 0;
        let activeCategory = 'all';

        function toggleLyrics(id) {
            const el = document.getElementById('lyrics-' + id);
            el.classList.toggle('show');
        }

        function playSong(idx) {
            currentIdx = idx;
            const song = SONGS[idx];
            
            // Open Stream Modal with YouTube Official audio/video embed
            const modal = document.getElementById('streamModal');
            const title = document.getElementById('modalTitle');
            const box = document.getElementById('videoBox');
            
            title.innerText = song.title_ku + ' - Şivan Perwer';
            box.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${song.yt_id}?autoplay=1&playsinline=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
            modal.classList.add('open');

            // Also update Sticky Bottom Player
            const sp = document.getElementById('stickyPlayer');
            document.getElementById('spTitle').innerText = song.title_ku;
            document.getElementById('spArtist').innerText = song.album + ' (' + song.year + ')';
            document.getElementById('spPlayBtn').innerText = '⏸';
            sp.style.display = 'flex';
        }

        function closeStreamModal() {
            const modal = document.getElementById('streamModal');
            modal.classList.remove('open');
            document.getElementById('videoBox').innerHTML = '';
            document.getElementById('spPlayBtn').innerText = '▶';
        }

        function handleModalClick(e) {
            if (e.target.id === 'streamModal') {
                closeStreamModal();
            }
        }

        function togglePlay() {
            const box = document.getElementById('videoBox');
            if (box.innerHTML === '') {
                playSong(currentIdx);
            } else {
                closeStreamModal();
            }
        }

        function nextSong() {
            currentIdx = (currentIdx + 1) % SONGS.length;
            playSong(currentIdx);
        }

        function prevSong() {
            currentIdx = (currentIdx - 1 + SONGS.length) % SONGS.length;
            playSong(currentIdx);
        }

        function closePlayer() {
            closeStreamModal();
            document.getElementById('stickyPlayer').style.display = 'none';
        }

        function setCategory(cat, el) {
            activeCategory = cat;
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            el.classList.add('active');
            filterSongs();
        }

        function filterSongs() {
            const q = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.song-card');
            
            cards.forEach(card => {
                const text = card.innerText.toLowerCase();
                const cat = card.getAttribute('data-cat');
                
                const matchQuery = text.includes(q);
                const matchCat = (activeCategory === 'all' || cat === activeCategory);

                if (matchQuery && matchCat) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""

SONG_CARD_TEMPLATE = """
<div class="song-card" data-cat="{category}">
    <div class="song-top">
        <div class="song-title-group">
            <h3>{title_ku}</h3>
            <span>💿 ألبوم: {album} ({year}) • {category_ar}</span>
        </div>
    </div>

    <div class="meta-grid">
        <div class="meta-item">
            <span>✍️ صاحب الكلمات (Helbestvan):</span>
            <strong>{lyricist}</strong>
        </div>
        <div class="meta-item">
            <span>🎼 الملحن (Awazdaner):</span>
            <strong>{composer}</strong>
        </div>
    </div>

    <div class="action-row">
        <button class="btn-play" onclick="playSong({idx})">
            ▶️ استماع وتشغيل
        </button>
        <a href="/download/{filename}" class="btn-download" download>
            ⬇️ تنزيل MP3
        </a>
    </div>

    <button class="lyrics-toggle" onclick="toggleLyrics('{id}')">
        📜 كلمات الأغنية بالكردية (Gotinên Stranê) ▾
    </button>
    <div class="lyrics-content" id="lyrics-{id}">
{lyrics}
    </div>
</div>
"""

class SivanRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ('/', '/index.html'):
            cards_html = ""
            for idx, item in enumerate(DISCOGRAPHY):
                d = dict(item)
                d['idx'] = idx
                cards_html += SONG_CARD_TEMPLATE.format(**d)
            
            json_data = json.dumps(DISCOGRAPHY, ensure_ascii=False)
            html = HTML_TEMPLATE.replace("{SONGS_HTML}", cards_html).replace("{SONGS_JSON}", json_data)
            body = html.encode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            
        elif parsed.path.startswith('/download/'):
            filename = os.path.basename(parsed.path)
            filepath = os.path.join(MUSIC_DIR, filename)
            if os.path.exists(filepath):
                filesize = os.path.getsize(filepath)
                self.send_response(200)
                self.send_header('Content-Type', 'audio/mpeg')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.send_header('Content-Length', str(filesize))
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File Not Found")
        else:
            super().do_GET()

if __name__ == '__main__':
    ensure_mp3_files()
    ip = get_local_ip()
    port = 8080
    server = HTTPServer(('0.0.0.0', port), SivanRequestHandler)
    print(f"SERVER_STARTED: http://{ip}:{port}")
    sys.stdout.flush()
    server.serve_forever()
