from yt_dlp import YoutubeDL
import logging
import json


def search_for_music(
    search_data: str,
    max_results: int | None = 50
) -> list[dict] | None:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True
    }
    search_query = f"scsearch{max_results if max_results else ''}:{search_data}"

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_query, download = False)
        if "entries" in result:
            return result["entries"]
        else:
            return None


# print(*search_for_music("sophie powers", 10), sep="\n\n")

# print(get_soundcloud_genres())


# def get_direct_music_url(
#     url: str
# ) -> dict:
#     ydl_opts = {
#         'format': 'bestaudio[ext=mp3]/bestaudio/best',
#         "quiet": True,
#         'no_warnings': True,
#         # 'get-url': True,
#         'skip_download': True
#     }

#     with YoutubeDL(ydl_opts) as ydl:
#         result = ydl.extract_info(url, download = False)

#     return result


# def get_all_links(
#     query: str
# ) -> list[str]:
#     # print(query)
#     data = search_for_music(query)
#     raw_links = []
#     if data:
#         for i in data:
#             try:
#                 url = i['webpage_url']
#                 # print(f"\n{url}\n")
#                 raw_links.append(url)
#                 break
#             except Exception as e:
#                 # print(e)
#                 continue
#     else:
#         return None
    
#     final_links = []
#     for i in raw_links:
#         link = get_direct_music_url(i)
#         print(f"\n{link}\n")
#         final_links.append(link["formats"][1]["url"])

#     # logging.warning(final_links)
#     return final_links
    





# data = search_for_music(
#     search_data = "sophie powers",
#     max_results = 100
# )

# print("\n**************\n")
# for i in data:
#     print(i)

# data = get_direct_music_url(
#     "https://soundcloud.com/krono_music/aaron-smith-dancin-remix-by"
# )


