const observer = new MutationObserver(function(mutationsList) {
    console.log("mutation detected");
    handleLiElements()
  });
  
const targetNode = document.getElementById('playlists');
const config = { attributes: true, childList: true, subtree: true };
let liElements = document.querySelectorAll('#playlists li');

observer.observe(targetNode, config);

function handleLiElements() {


    let allHidden = true;

    for (let i = 0; i < liElements.length; i++) {
        if (liElements[i].style.display !== 'none') {
        allHidden = false;
        break;
        }
    }

    if (allHidden) {
        for (let i = 0; i < liElements.length; i++) {
        liElements[i].style.display = '';
        }
    }

}


 

  