import os
from supabase_py import create_client

def init_supabase():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase = create_client(supabase_url, supabase_key)
    return supabase

def fetch_spotify_id(nfc_id):
    db = init_supabase()
    tables = ['Artists', 'Albums', 'Playlists']
    media_types = ['artist', 'album', 'playlist']

    for table, media_type in zip(tables, media_types):
        result = db.table(table).select('spotify_id').eq('nfc_id', str(nfc_id)).execute()
        if result and len(result['data']) > 0:
            return {"spotify_id": result[0].get('spotify_id'), "media_type": media_type}

    return None
