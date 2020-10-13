var filePath = "17MarchHtmlTest-FR.json";
var regex = "(http|https)://(www)*(.|\w|/|-|=|&|%|(|))*";
var text = "";
var urlCount = 0;
var processedUrlCount = 0;

function readFile() {
    $.get(filePath, function(data) {
        var matches = /(http|https):\/\/(\w+)(\.|\w|\/|-|\?|=|&|%|\(|\))*/g.execAll(JSON.stringify(data));
        document.getElementById("demo").innerHTML = "Validating urls, please wait...";
        text = "<ul>";

        matches.forEach(function(element) {
            var url = element.toString().split(",")[0];
            document.getElementById("demo").innerHTML += "<br/>Verifying " + url;
            var status = validateUrl(url);

            if (status == 200) {
                text += "<li>" + "<b><a href='" + url + "'>" + url + "</a></b>: valid</li>";
            } else {
                text += "<li>" + "<b><a href='" + url + "'>" + URLSearchParams + "</a></b> invalid</li>";
            }

            document.getElementById("demo").innerHTML = text;
        });

        text += "</ul>";
        //document.getElementById("demo").innerHTML = text;
    });
}

function validateUrl(url) {
    var request;
    if (window.XMLHttpRequest) {
        request = new XMLHttpRequest();
    } else {
        request = new ActiveXObject("Microsoft.XMLHTTP");
    }

    request.open('GET', url, false);
    request.send();
    return request.status;
}

// Return all pattern matches with captured groups
RegExp.prototype.execAll = function(string) {
    var match = null;
    var matches = new Array();
    while (match = this.exec(string)) {
        var matchArray = [];
        for (i in match) {
            if (parseInt(i) == i) {
                matchArray.push(match[i]);
            }
        }
        matches.push(matchArray);
    }
    return matches;
}