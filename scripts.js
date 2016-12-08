var map;
var markerCount=0;
var userCount=0;
var ipCount=0;

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
            data = JSON.parse(data);
            for(var i=0;i<data.length;i++) {
                attack = data[i];
                msg = attack['ip']
                addMarkerToMap(attack["lat"],attack["long"],msg);
            }
            // populateTables();
        }
    }
    xmlHttp.open("GET","live",true);
    xmlHttp.send();
}
