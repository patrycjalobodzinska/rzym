import os, json
src = open("app.html", encoding="utf-8").read()
head = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2C6B5E">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Roma">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>:root{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""
body_split = src.index('<div class="app"')
open("index.html","w",encoding="utf-8").write(head + src[:body_split] + "</head>\n<body>\n" + src[body_split:] + "\n</body>\n</html>\n")
imgs = sorted("img/"+f for f in os.listdir("img") if f.endswith(".jpg"))
assets = ["./","index.html","manifest.webmanifest","icon-192.png","icon-512.png","apple-touch-icon.png"] + imgs
open("sw.js","w").write(f"""const C="roma-v1";
const A={json.dumps(assets)};
self.addEventListener("install",e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(A)));self.skipWaiting()}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()}});
self.addEventListener("fetch",e=>{{if(e.request.method!=="GET")return;
 e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request).then(res=>{{
  if(res.ok&&(e.request.url.startsWith(self.location.origin)||e.request.url.includes("fonts.g"))){{const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp))}}
  return res}}).catch(()=>caches.match("index.html"))))}});
""")
json.dump({"name":"Roma w 3 dni","short_name":"Roma","start_url":"./","scope":"./","display":"standalone",
 "background_color":"#F2F0EB","theme_color":"#2C6B5E","lang":"pl",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},
 open("manifest.webmanifest","w"),ensure_ascii=False,indent=1)
print("ok", len(assets))
