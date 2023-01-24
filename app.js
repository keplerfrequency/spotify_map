// This fcuntion creates the plalist cards for every playlist
  function displayPlaylists(id){
    fetch('playlist.json')
    .then(response => response.json())
    .then(data => {
      data.countries.forEach(country => {
        country.playlists.forEach(playlist => {
          const box = document.createElement('li');
          box.setAttribute("class", "playlist_card")
          box.setAttribute("id",country.country);
  
          const a = document.createElement('a');
          a.target = "_blank";
          a.rel = "noopener noreferrer";
  
          const img = document.createElement('img');
          img.setAttribute("class", "playlist-img");
          img.src = playlist.img;
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

          document.getElementById(id).appendChild(box);
        });
      });
    });
  }

//This function will toggle the spotify playlists
document.addEventListener('DOMContentLoaded', function(){
  const toggleButton = document.getElementById("toggle-button-spotify").querySelector('input');
  const playlistByValue = "Spotify";

  toggleButton.addEventListener("change", function() {
    const elements = document.querySelectorAll(`[data-playlist-by='${playlistByValue}']`);
    elements.forEach(function(element) {
      element.classList.toggle("hidden", !this.checked);
    }.bind(this));
  });
});

//This function toggles the non user playlists
document.addEventListener('DOMContentLoaded', function(){
  const toggleButton = document.getElementById("toggle-button-user").querySelector('input');
  const playlistByValue = "Spotify";

  toggleButton.addEventListener("change", function() {
    const elements = document.querySelectorAll(`[data-playlist-by]:not([data-playlist-by='${playlistByValue}'])`);
    elements.forEach(function(element) {
      element.classList.toggle("hidden", !this.checked);
    }.bind(this));
  });
});

//This code places the href from the playlist into the embedded player upon image click
window.onclick = e => {
  if(e.target.classList.contains('playlist-img')){
    const iframe = document.querySelector('#embedded_player'); 
    const clicked_item = e.target;

    let link = clicked_item.getAttribute('data-href')
    link = link.replace('playlist', 'embed/playlist')+"?utm_source=generator&theme=0";
    iframe.src = link;
  }
} 
