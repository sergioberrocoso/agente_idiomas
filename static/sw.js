const CACHE = 'lang-tutor-v1';

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll([
        '/',
        '/?lang=en',
        '/?lang=de',
        '/?lang=fr',
        '/static/manifest.json',
        '/static/icon-192.svg',
        '/static/icon-512.svg'
      ]);
    })
  );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(r) {
      return r || fetch(e.request).then(function(res) {
        if (res && res.ok && e.request.method === 'GET') {
          var copy = res.clone();
          caches.open(CACHE).then(function(cache) { cache.put(e.request, copy); });
        }
        return res;
      });
    })
  );
});
