//Go to Spotify login page
function authorizeUser() {
    var scopes = 'app-remote-control user-modify-playback-state streaming';

    
    SPOTIFY_CLIENT_ID = '948c4e2f99254fcdbf7e8f9779da03b6'
    SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5500/index.html'
    
    var url = 'https://accounts.spotify.com/authorize?client_id=' + SPOTIFY_CLIENT_ID +
    '&response_type=token' +
    '&scope=' + encodeURIComponent(scopes) +
    '&redirect_uri=' + encodeURIComponent(SPOTIFY_REDIRECT_URI);
    document.location = url;

    args = parseArgs();
    
    localStorage.setItem('token', args.access_token);

    return;
}

//Get the token from the redirect URL from Spotify
function parseArgs() {
    var hash = location.hash.replace(/#/g, '');
    var all = hash.split('&');
    var args = {};
    all.forEach(element => {
        var kv = element.split('=');
        var key = kv[0];
        var val = kv[1];
        args[key] = val;
    });
    return args;
}


//http://sortyourmusic.playlistmachinery.com/
//On click of the login button call the authorize function to go to spotify and login
window.addEventListener('click', (ev) => {
    //console.log(ev);
    //console.log(ev.target.classList)
    if(ev.target.classList.contains('login_div') || ev.target.classList.contains('login_text')){
        console.log('authorizing user now!')
        authorizeUser();
    }

});