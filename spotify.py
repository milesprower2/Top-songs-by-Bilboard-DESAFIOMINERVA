import requests
import urllib.parse

def get_spotify_data(song_with_artist):
    """
    Recebe: 'Song — Artist'
    Retorna:
      - link Spotify
      - imagem do álbum (iTunes)
    """

    # -----------------------------
    # Normalização do texto
    # -----------------------------
    if "—" in song_with_artist:
        song, artist = song_with_artist.split("—", 1)
    elif "-" in song_with_artist:
        song, artist = song_with_artist.split("-", 1)
    else:
        song = song_with_artist
        artist = ""

    song = song.strip()
    artist = artist.strip()

    # -----------------------------
    # Spotify (link)
    # -----------------------------
    spotify_query = urllib.parse.quote(f"{song} {artist}")
    spotify_link = f"https://open.spotify.com/search/{spotify_query}"

    # -----------------------------
    # iTunes (imagem)
    # -----------------------------
    itunes_term = urllib.parse.quote(f"{song} {artist}")
    itunes_url = (
        "https://itunes.apple.com/search"
        f"?term={itunes_term}&media=music&entity=song&limit=1"
    )

    image = None
    try:
        response = requests.get(itunes_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("resultCount", 0) > 0:
            image = data["results"][0].get("artworkUrl100")
            if image:
                image = image.replace("100x100", "300x300")
    except Exception:
        pass

    return {
        "link": spotify_link,
        "image": image
    }
