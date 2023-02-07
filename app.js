//Load the playlists when the window loads 
window.onload = function() {
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
