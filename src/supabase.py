import os
from supabase_py import create_client

def init_supabase():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase = create_client(supabase_url, supabase_key)
    return supabase

def fetch_all_media():
    '''Fetch all songs from the database'''

    db = init_supabase()
    data = []
    for table in ['artists', 'albums', 'playlists']:
        results = db.table(table).select('*').execute()
        if results and len(results['data'])>0:
            for item in results['data']:
                item['media_type'] = table[:-1]
                data.append(item)
    return data

def fetch_spotify_id(nfc_id, all_media):
    '''Fetch the spotify_id from all media that matches the nfc_id'''
    
    # db = init_supabase()
    # tables = ['artists', 'albums', 'playlists']
    # media_types = ['artist', 'album', 'playlist']

    # for table, media_type in zip(tables, media_types):
    #     result = db.table(table).select('spotify_id').eq('nfc_id', str(nfc_id)).execute()
    #     if result and len(result['data'])>0:
    #         return {"spotify_id": result['data'][0].get('spotify_id'), "media_type": media_type}

    for media in all_media:
        if media.get('nfc_id') == str(nfc_id):
            return {"spotify_id": media.get('spotify_id'), "media_type": media.get('media_type')}

    return None
