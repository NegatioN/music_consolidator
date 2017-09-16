function setup_swapper(){
    var swap_button = document.getElementById("swapper");
    swap_button.onclick = function() {
        var artistElem  = document.getElementById("artist-input");
        var titleElem  = document.getElementById("title-input");
        var artistText = artistElem.value;
        var titleText = titleElem.value;
        artistElem.value = titleText;
        titleElem.value = artistText;
    };
}