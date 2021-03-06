function pack(bytes) {
    var chars = [];
    for(var i = 0, n = bytes.length; i < n;) {
/*       chars.push(((bytes[i++] & 0xff) << 8) | (bytes[i++] & 0xff)); */
        sp.write(((bytes[i++] & 0xff) << 8) | (bytes[i++] & 0xff));
    }
    return String.fromCharCode.apply(String, chars);
}

function unpack(str) {
    var bytes = [];
    for(var i = 0, n = str.length; i < n; i++) {
        var char = str.charCodeAt(i);
        bytes.push(char >>> 8, char & 0xFF);
    }
    return bytes;
}

function chksum(cmd,msk,p1,p2){
    return (((~(0x04+cmd+msk+p1+p2))+0x01)&0xff);
}

function packet(cmd,msk,p1,p2){
    return pack([0x04,cmd,msk,p1,p2,chksum(cmd,msk,p1,p2),0x0f]);
}


var serialport = require("serialport");
  var SerialPort = serialport.SerialPort; // localize object constructor
  
  var sp = new SerialPort("/dev/ttyACM0", { 
    parser: serialport.parsers.raw, baudrate: 19200
  });


sp.write(packet(0x51,0x01,0,0));

