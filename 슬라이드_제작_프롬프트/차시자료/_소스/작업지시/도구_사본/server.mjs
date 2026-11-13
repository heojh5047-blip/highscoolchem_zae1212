import https from 'https'; import fs from 'fs'; import path from 'path';
const root = path.resolve('node_modules/katex/dist');
const types = {'.js':'application/javascript','.css':'text/css','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf'};
https.createServer({key:fs.readFileSync('key.pem'),cert:fs.readFileSync('cert.pem')},(req,res)=>{
  const m = req.url.split('?')[0].match(/^\/npm\/katex@[^/]+\/dist\/(.*)$/);
  const f = m && path.join(root, m[1]);
  if (!f || !f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200,{'Content-Type':types[path.extname(f)]||'application/octet-stream','Access-Control-Allow-Origin':'*'}); fs.createReadStream(f).pipe(res);
}).listen(8443,'127.0.0.1');
