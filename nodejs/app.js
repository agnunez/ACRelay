var http = require('http');
var url = require('url');
	 
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
                console.log('Body ' + chunk);
            });
        }
    }).on('error', function(err) {
        console.log('Error %s', err.message);
    });
}
	 
/* i.e. request('www.google.com', '/search?ie=UTF-8&q=node'); */

request('192.168.1.38', 8081, '/set?r=1&v=0');
setTimeout(function(){
	request('192.168.1.38', 8081, '/set?r=1&v=1');
	}, 5000);


