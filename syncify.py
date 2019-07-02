"""
Syncs saved songs with a shareable playlist.
"""
import sys
import spotipy
import spotipy.util as sutil
import config

class Progress(object):
    """
    A simple progress indicator that can be used as a context manager.

    The object can be initialized with a message. Upon successfully exiting the
    will print "done," otherwise the error message and traceback will be printed
    and the program will terminate.
    """
    def __init__(self, message):
        self.message = message
    def __enter__(self):
        sys.stdout.write("{0}... ".format(self.message))
    def __exit__(self, type, value, traceback):
        if value is not None:
            import traceback as tb
            print("Error.", file=sys.stderr)
            print(value, file=sys.stderr)
            tb.print_tb(traceback)
            sys.exit(1)
        print("done.")

def page_next(sp, page):
    """
    Returns the next paging object for the given page, or none if the page has
    no next.
    """
    if page['next']:
        return sp.next(page)
    else:
        return None

def get_track_ids(tracks_page):
    """
    Returns all the track IDs in the current track page.
    """
    return [item['track']['id'] for item in tracks_page['items']]

def main():
    # The script requires two scopes, one to read from the user's "Saved Songs"
    # and the other to modify the user's public playlists
    scope = 'user-library-read playlist-modify-public'
    token = sutil.prompt_for_user_token(config.USER_NAME, scope,
                                   client_id=config.SPOTIFY_CLIENT_ID,
                                   client_secret=config.SPOTIFY_CLIENT_SECRET,
                                   redirect_uri=config.SPOTIFY_REDIRECT_URL)
    if token:
        sp = spotipy.Spotify(auth=token)

        # Attempt to find the playlist specified by PLAYLIST_NAME in the config
        playlists = sp.current_user_playlists()
        target_playlist = None
        with Progress("Looking for playlist"):
            while playlists:
                for playlist in playlists['items']:
                    if playlist['name'] == config.PLAYLIST_NAME:
                        target_playlist = sp.user_playlist(config.USER_NAME,
                                       playlist['id'],
                                       fields="id,tracks,next,external_urls")
                        break
                playlists = page_next(sp, playlists)

        # If no playlist with the specified name is found, create it.
        if not target_playlist:
            with Progress(
                    "No playlist found with name {0}, creating one".format(
                        config.PLAYLIST_NAME)):
                target_playlist = sp.user_playlist_create(config.USER_NAME,
                                                          config.PLAYLIST_NAME) 
        # Clear the playlist of all songs,
        # This is not a very expensive operation that ensures the playlist
        # matches the list of saved songs down to the ordering of songs.
        with Progress("Clearing playlist"):
            sp.user_playlist_replace_tracks(config.USER_NAME,
                                            target_playlist['id'], [])

        # Get the tracks that are saved by the current user
        saved_tracks = sp.current_user_saved_tracks()

        # Add all the saved tracks to the target playlist
        with Progress("Adding songs to playlist"):
            while saved_tracks:
                sp.user_playlist_add_tracks(config.USER_NAME,
                                        target_playlist['id'],
                                        get_track_ids(saved_tracks))
                saved_tracks = page_next(sp, saved_tracks)

        print("Playlist created successfully, please use this URL to access it")
        print(target_playlist['external_urls']['spotify'])

    else:
        print("Unable to get token for Spotify.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
