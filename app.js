//Run a series of actions when the window loads 
window.onload = function() {
  document.getElementById("search").value = "";
  
  if (!localStorage.getItem("popupShown")) {
    showPopup();
  }
  
  args = parseArgs();
    
  localStorage.setItem(STORAGE_TOKEN_KEY, args.access_token);
  
  displayPlaylists("playlists");
} 

// This function creates the plalist cards for every playlist
async function displayPlaylists(id){
  fetch('playlist.json')
  .then(response => response.json())
  .then(data => {
    const countryPlaylist = {}
    data.countries.forEach(country => {
      country.playlists.forEach(playlist => {
        countryPlaylist[country.country] = countryPlaylist[country.country] || []
        countryPlaylist[country.country].push(playlist)
      })
    })

    Object.entries(countryPlaylist).forEach(([country, playlists]) => {
      const container = document.createElement('li');
      
      container.setAttribute("id", country);
      container.setAttribute("class", 'country');

      playlists.forEach(playlist => {
        const box = document.createElement('div');
        box.setAttribute("loading", "lazy")
        box.classList.add('playlist_card')

        const a = document.createElement('a');
        a.target = "_blank";
        a.rel = "noopener noreferrer";

        const img = document.createElement('img');
        img.setAttribute("class", "playlist-img");
        img.setAttribute("loading", "lazy");
        img.setAttribute("src", playlist.img);
        img.setAttribute("data-href", playlist.link);
        a.appendChild(img);
        box.appendChild(a);

        const text = document.createElement('p');
        text.innerText = playlist.name;
        const text1 = document.createElement('p1');
        text1.innerText = playlist.playlist_by;
        box.appendChild(text);
        box.appendChild(text1);
        
        box.dataset.playlistBy = playlist.playlist_by;
        
        const div = document.createElement('div');
        div.textContent = playlist.description;
        div.setAttribute("class", "playlist_description")
        box.appendChild(div)

        container.appendChild(box)
      });
      document.getElementById(id).appendChild(container);
    });
    const extraDiv = document.createElement('div');
    extraDiv.setAttribute('id', 'buffer_area');
    document.getElementById(id).appendChild(extraDiv);

    var loadingMessage = document.getElementById('loading-message');
    loadingMessage.style.display = 'none';

  });
}

document.addEventListener('DOMContentLoaded', function(){
  const playlistByValue = "Spotify";

  //This function will toggle the spotify playlists
  document.querySelector("#toggle-button-spotify input").addEventListener("change", (ev) => {
    for (element of document.querySelectorAll(`[data-playlist-by='${playlistByValue}']`)) {
      element.classList.toggle("hidden", !ev.target.checked)
    }
  })

  //This function toggles the non user playlists
  document.querySelector("#toggle-button-user input").addEventListener("change", (ev) => {
    for (element of document.querySelectorAll(`[data-playlist-by]:not([data-playlist-by='${playlistByValue}'])`)) {
      element.classList.toggle("hidden", !ev.target.checked)
    }
  })

  var searchInput = document.getElementById("search");

  searchInput.addEventListener("input", function() {
    searchPlaylist();
  });

})

//This code places the href from the playlist into the embedded player upon image click
window.addEventListener('click', (ev) => {
  if(ev.target.classList.contains('playlist-img')){
    const iframe = document.querySelector('#embedded_player'); 
    const clicked_item = ev.target;

    let link = clicked_item.getAttribute('data-href')
    link = link.replace('playlist', 'embed/playlist')+"?utm_source=generator&theme=0";
    iframe.src = link;
  }
})

//Search functionlaity
function searchPlaylist() {
  console.log("Starting to search playlists");

  // Get the input value
  let input = document.getElementById("search").value.toLowerCase();
  console.log("Selected search element ");
  
  // Loop through each playlist card
  let playlists = $(document).find('.playlist_card');
  console.log(" Found " + playlists.length + " playlists")
  playlists.each(function(index) {
    let element = this;

    let playlistName = $(element).find('p').eq(0).html().toLowerCase();
    if (playlistName.includes(input)) {
      $(element).removeClass('not_searched');
    } else {
      $(element).addClass('not_searched');
    }

  });
  console.log("Finished refresh of page ");
  
}

//Show and close the pop up
function showPopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "block";
}

function closePopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "none";
  localStorage.setItem("popupShown", "true");
}

window.onSpotifyWebPlaybackSDKReady = () => {
  const token = localStorage.getItem('token')

  const player = new window.Spotify.Player({
  name: 'Spotify map',
  getOAuthToken: cb => { cb(token); },
  volume: 0.5
  });

// Ready
player.addListener('ready', ({ device_id }) => {
  console.log('Ready with Device ID', device_id);
});

// Not Ready
player.addListener('not_ready', ({ device_id }) => {
  console.log('Device ID has gone offline', device_id);
});

player.addListener('initialization_error', ({ message }) => {
  console.error(message);
});

player.addListener('authentication_error', ({ message }) => {
  console.error(message);
});

player.addListener('account_error', ({ message }) => {
  console.error(message);
});
/*         document.getElementById('togglePlay').onclick = function() {
player.togglePlay();
}; */
  player.connect();
}