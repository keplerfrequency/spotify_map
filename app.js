//Load the playlists when the window loads 
window.onload = function() {
  document.getElementById("search").value = "";
  
  if (!localStorage.getItem("popupShown")) {
    showPopup();
  }   
  
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
  });
}

//This function will toggle the spotify playlists
document.addEventListener('DOMContentLoaded', function(){
  const playlistByValue = "Spotify";

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
  // Get the input value
  var input = document.getElementById("search").value.toLowerCase();

  // Get all playlist cards
  var playlists = document.getElementsByClassName("playlist_card");

  // Loop through each playlist card
  for (var i = 0; i < playlists.length; i++) {
    // Get the playlist name
    var playlistName = playlists[i].getElementsByTagName("p")[0].innerHTML.toLowerCase();

    // Check if the playlist name contains the input value
    if (playlistName.includes(input)) {
      playlists[i].classList.remove("not_searched")
    } else {
      playlists[i].classList.add("not_searched")
    }
  }
}



function showPopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "block";
}

function closePopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "none";
  localStorage.setItem("popupShown", "true");
}


