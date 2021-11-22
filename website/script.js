const server_ip ="http://54.160.195.210"
function httpGet()
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", server_ip, false );
    xmlHttp.send( null );
    var message = JSON.parse(xmlHttp.responseText).message
    document.getElementById("response").innerHTML = message
}