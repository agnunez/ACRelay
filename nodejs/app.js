var http = require('http');
var url = require('url');
var relay = Array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
	 
function request(address, port, path) {
    http.get({ host: address, port: port, path: path}, function(response) {
        // The page has moved make new request
        if (response.statusCode === 302) {
            var newLocation = url.parse(response.headers.location).host;
            console.log('We have to make new request ' + newLocation);
            request(newLocation);
        } else {
            console.log("Response: %d", response.statusCode);
            response.on('data', function(chunk) {
		relay = JSON.parse(chunk);
		buf=''; 
		for(i=0;i<16;i++){
			if(i<8){ buf+='R';j=i;k=0;}else{buf+='S';j=i-8;k=1}
			buf+=j+'='+relay[k][j]+' ';
		}
                console.log(buf);
            });
        }
    }).on('error', function(err) {
        console.log('Error %s', err.message);
    });
}
	 
/* i.e. request('www.google.com', '/search?ie=UTF-8&q=node'); */

request('192.168.1.38', 8081, '/set?r=1&v=1');
setTimeout(function(){request('192.168.1.38', 8081, '/test')},2000);
setTimeout(function(){
		request('192.168.1.38', 8081, '/set?r=1&v=0');
		setTimeout(function(){request('192.168.1.38', 8081, '/test')},2000);
	}, 5000);


