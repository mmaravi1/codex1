const http = require('http');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8' };

http.createServer((req, res) => {
  const requestPath = req.url === '/' ? '/index.html' : req.url.split('?')[0];
  const filename = path.resolve(root, `.${requestPath}`);
  if (!filename.startsWith(root)) { res.writeHead(403); return res.end('Forbidden'); }
  fs.readFile(filename, (err, file) => {
    if (err) { res.writeHead(404); return res.end('Not found'); }
    res.writeHead(200, {
      'Content-Type': types[path.extname(filename)] || 'application/octet-stream',
      'Cache-Control': 'no-store'
    });
    res.end(file);
  });
}).listen(3000, () => console.log('Lingua Scout: http://localhost:3000'));
