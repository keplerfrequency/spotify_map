const targetNode = document.getElementsByClassName('country');

const observer = new MutationObserver(function(mutationsList) {
    console.log(1);
    for(let mutation of mutationsList) {
        if (mutation.type === 'subtree') {
            console.log(mutation);
        }
  }
});

const config = { subtree: true,childList: true, attributes:true, characterData:true };
observer.observe(targetNode, config);

 
function handleLiElements() {
    const liElements = document.querySelectorAll('#playlists li');

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
  