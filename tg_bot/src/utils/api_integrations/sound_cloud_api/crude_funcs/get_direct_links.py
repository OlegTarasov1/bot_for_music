from yt_dlp import YoutubeDL


def get_direct_music_url(
    url: str
) -> dict:
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio/best',
        "quiet": True,
        'no_warnings': True,
        'skip_download': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download = False)

    return result


def get_mp3_links(
    entrie: dict[dict[str]]
):
    link = None
    
    for i in entrie.get("formats", []):
        if i.get("format_id", "").startswith("http_mp3"):
            link = i.get("url")

    return link