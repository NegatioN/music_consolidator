
function updateMetadata(){
    var formLink = document.getElementById("link");
    var val = "";
    formLink.addEventListener('input', function(event) {
        if (val != this.value) {
            val = this.value;
            if (matchYoutubeLink(val) != -1) {
                getMetaData(val);
            }
        }
    });
}

function getMetaData(link) {
    var loader = document.getElementById("loader-container");
    loader.style.opacity = 1;

    var encodedLink = encodeURIComponent(link);
    var request = new XMLHttpRequest();

    request.onreadystatechange = function(response) {
        if (this.readyState == 4 && this.status == 200) {
            var info = guessTitle(this.responseText);
            document.getElementById("artist-input").value = info[0];
            document.getElementById("title-input").value = info[1];
            loader.style.opacity = 0;
        }
    };

    request.open('GET', '/metadata/'+encodedLink);
    request.send();
}

function matchYoutubeLink(text) {
    return text.search(/(v=|\.be\/|\/v\/).{11}/g);
}

function guessTitle(responseText) {
    return responseText.split(/\s*(?:-|\/|／)\s*/);
}

if (typeof exports !== 'undefined') {
    exports.guessTitle = guessTitle;
    exports.matchYoutubeLink = matchYoutubeLink;
}
