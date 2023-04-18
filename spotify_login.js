const STORAGE_TOKEN_KEY = "token";

//Go to Spotify login page
function authorizeUser() {
    let scopes = [
        'streaming',
        'app-remote-control',
        'user-modify-playback-state',
    ]

    
    SPOTIFY_CLIENT_ID = '948c4e2f99254fcdbf7e8f9779da03b6'
    SPOTIFY_REDIRECT_URI = 'https://keplerfrequency.github.io/spotify_map'
    

var scope = scopes.join(" ")

var url = 'https://accounts.spotify.com/authorize';
url += '?response_type=token';
url += '&client_id=' + encodeURIComponent(SPOTIFY_CLIENT_ID);
url += '&scope=' + encodeURIComponent(scope);
url += '&redirect_uri=' + encodeURIComponent(SPOTIFY_REDIRECT_URI);
document.location = url;
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


//This function will clear any characters in the url that come after the # sign
function clearUrl(){
    var url = window.location.href;
    var index = url.indexOf('#');
    if (index > 0) {
        url = url.substring(0, index);
        window.history.pushState({}, document.title, url);
        document.getElementById("login").remove();
    }
}