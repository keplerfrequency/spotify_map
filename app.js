function displayPlaylists(id) {
    fetch("playlist.json")
      .then(response => response.json())
      .then(json => {
        
        var countries = json.countries;
        
        for (var i = 0; i < countries.length; i++) {
          var playlists = countries[i].playlists;
          var li = document.createElement("li");
          li.setAttribute("id",countries[i].country);
          document.getElementById(id).appendChild(li);
          //var title = document.createElement("h2");
          //title.textContent = countries[i].name;
          //li.appendChild(title);
          
          for (var j = 0; j < playlists.length; j++) {
            var link = playlists[j].link;
            var newLink = link.replace("open.spotify.com/playlist/", "open.spotify.com/embed/playlist/").concat("?utm_source=generator&theme=0")
            var iframe = document.createElement("iframe");
            iframe.setAttribute("style","border-radius:12px");
            iframe.setAttribute("src",newLink);
            iframe.setAttribute("width","100%");
            iframe.setAttribute("height","200");
            iframe.setAttribute("frameBorder","0");
            iframe.setAttribute("allowfullscreen","");
            iframe.setAttribute("allow","autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture");
            iframe.setAttribute("loading","lazy");
            li.appendChild(iframe);
            li.appendChild(document.createElement("br"));
          }
        }
      });
  }
  