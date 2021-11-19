function httpGet()
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://127.0.0.1:80/", false );
    xmlHttp.send( null );
    var message = JSON.parse(xmlHttp.responseText).message
    document.getElementById("response").innerHTML = message
}