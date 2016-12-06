var map;
var markerCount;
var userCount;
var ipCount;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 24, lng: 0},
        zoom: 2,
        scrollwheel: false,
        navigationControl: false,
        mapTypeControl: false,
        scaleControl: false,
        // draggable: false,
        streetViewControl: false,
        zoomControl: false,
    });
}

function addMarkerToMap(lat, long, htmlMarkupForInfoWindow){
    var infowindow = new google.maps.InfoWindow();
    var myLatLng = new google.maps.LatLng(lat, long);
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        animation: google.maps.Animation.DROP,
    });

    markerCount++;

    google.maps.event.addListener(marker, 'click', (function(marker, markerCount) {
        return function() {
            infowindow.setContent(htmlMarkupForInfoWindow);
            infowindow.open(map, marker);
        }
    })(marker, markerCount));    
}

function sortTable(table){
    var temp = [];
    for (var i in table){
        temp.push([i,table[i]]);
    }
    temp.sort(function(a,b){
        return a[1] - b[1]
    });
    return temp;
}

function populateTables(){
    var ips = sortTable(ipCount);
    var users = sortTable(userCount);
    var ipsTable = document.getElementById("top-ips")
    var userTable = document.getElementById("top-users");

    for(var i = 0; i < 10; i++){
        var tr = document.createElement('tr');
        for(var j = 0; j < 2; j++){
            var td = document.createElement('td');
            td.appendChild(document.createTextNode(ips[i][j]));
            tr.appendChild(td);
        }
    }
    ipsTable.appendChild(tr);

    for(var i = 0; i < 10; i++){
        var tr = document.createElement('tr');
        for(var j = 0; j < 2; j++){
            var td = document.createElement('td');
            td.appendChild(document.createTextNode(users[i][j]));
            tr.appendChild(td);
        }
    }
    userTable.appendChild(tr);
}

function getDataFromServer(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200){
            // Response Fields:
            // time_stamp
            // user
            // ip
            // lat
            // long
            var data = xmlHttp.responseText;
            for(var obj in data) {
                attack = JSON.parse(obj);
                addMarkerToMap(attack["lat"],attack["long"],attack["time_stamp"]+" - "attack["user"]+":"attack["ip"]);
                userCount[attack["user"]]++;
                ipCount[attack["ip"]]++;
            }
            populateTables();
        }
    }
    xmlHttp.open("GET","live",true);
    xmlHttp.send(null);
}

// function httpGetAsync(theUrl,ip){
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.onreadystatechange = function(){
//         if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
//             var json = xmlHttp.responseText;
//             var obj = JSON.parse(json);
//             addMarkerToMap(obj['latitude'],obj['longitude'],ip);
//         }
//     }
//     xmlHttp.open("GET", theUrl, true);
//     xmlHttp.send(null);
// }

// function parseIPs(){
//     var ip_pattern = new RegExp("(?:[0-9]{1,3}\.){3}[0-9]{1,3}$");
//     var textArea = document.getElementById('ip-entry').value;
//     var lines = textArea.split('\n');
//     for (var i = 0; i < lines.length; i++){
//         if (ip_pattern.test(lines[i])){
//             httpGetAsync("https://freegeoip.net/json/"+lines[i],lines[i])
//         } else {
//             console.log("Didn't recognize "+lines[i]+" as a valid IP address.")
//         }
//     }
// }

// function getDataFromServer()
// {
//     var req = new XMLHttpRequest();
//     req.onreadystatechange = function()
//     {
//         if (req.readyState == 4 && req.status == 200)
//         {
//             var ip_addresses = JSON.parse(req.responseText);
//             for (var i=0;i<ip_addresses.length;i++)
//             {   
//                 ip_addresses[i] = ip_addresses[i].trim();
//                 document.getElementById('ip-entry').value += '\n'+ip_addresses[i];
//             }
//         }
//     }
//     req.open("GET","live",true);
//     req.send(null);
// }