function authorizeUser() {
    var scopes = 'app-remote-control user-modify-playback-state streaming';

    SPOTIFY_CLIENT_ID = '948c4e2f99254fcdbf7e8f9779da03b6'
    SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5500/index.html'

    var url = 'https://accounts.spotify.com/authorize?client_id=' + SPOTIFY_CLIENT_ID +
        '&response_type=token' +
        '&scope=' + encodeURIComponent(scopes) +
        '&redirect_uri=' + encodeURIComponent(SPOTIFY_REDIRECT_URI);
    document.location = url;
}


//http://sortyourmusic.playlistmachinery.com/
window.addEventListener('click', (ev) => {
    console.log(ev);
    if(ev.target.classList.contains('login_div' || 'login_text')){
        authorizeUser();
    }

});