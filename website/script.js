const server_ip ="123"
function httpGet()
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", server_ip, false );
    xmlHttp.send( null );
    var message = JSON.parse(xmlHttp.responseText).message
    document.getElementById("response").innerHTML = message
}