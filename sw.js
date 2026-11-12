const C="roma-v2";
const A=["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "img/bocca.jpg", "img/campidoglio.jpg", "img/campo.jpg", "img/castel.jpg", "img/circo.jpg", "img/colosseum.jpg", "img/constantine.jpg", "img/forum.jpg", "img/monti.jpg", "img/navona.jpg", "img/palatine.jpg", "img/pantheon.jpg", "img/pincio.jpg", "img/popolo.jpg", "img/sistine.jpg", "img/spagna.jpg", "img/stpeter.jpg", "img/trastevere.jpg", "img/trevi.jpg", "img/vatican.jpg", "img/vittoriano.jpg"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;
 e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).then(res=>{
  if(res.ok&&(e.request.url.startsWith(self.location.origin)||e.request.url.includes("fonts.g"))){const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp))}
  return res}).catch(()=>caches.match("index.html"))))});
