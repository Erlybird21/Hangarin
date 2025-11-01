const CACHE_NAME = 'hangarin-v1';
const URLS_TO_CACHE = [
  '/',                               // Root scope
  '/offline/',                       // Offline fallback page
  '/static/manifest.json',           // Manifest file
  '/static/css/styles.css',          // Your main stylesheet
  '/static/js/app.min.js'            // Your main JS bundle
];

// ✅ INSTALL: Cache essential assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(async cache => {
        const results = await Promise.allSettled(
          URLS_TO_CACHE.map(async url => {
            try {
              const resp = await fetch(url, { cache: 'no-store' });
              if (resp.ok) {
                await cache.put(url, resp.clone());
              } else {
                console.warn(`Skipped caching (bad response): ${url}`);
              }
            } catch (e) {
              console.warn(`Skipped caching ${url}:`, e);
            }
          })
        );
        console.log('Cache results:', results);
      })
      .then(() => self.skipWaiting()) // activate immediately
  );
});

// ✅ ACTIVATE: Clean old caches and take control immediately
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.map(k => k !== CACHE_NAME && caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// ✅ FETCH: Network-first for HTML, cache-first for static assets
self.addEventListener('fetch', event => {
  const req = event.request;

  // Ignore non-GET requests (prevents POST crash)
  if (req.method !== 'GET') return;

  // HTML pages → network-first
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then(resp => {
          const copy = resp.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, copy));
          return resp;
        })
        .catch(() => caches.match('/offline/'))
    );
    return;
  }

  // Static assets → cache-first, then network fallback
  event.respondWith(
    caches.match(req)
      .then(resp => resp || fetch(req)
        .then(networkResp => {
          // Cache new static assets dynamically
          if (networkResp.ok) {
            const copy = networkResp.clone();
            caches.open(CACHE_NAME).then(c => c.put(req, copy));
          }
          return networkResp;
        })
      )
      .catch(() => caches.match('/offline/'))
  );
});

// ✅ Optional: Immediate claim for updates (forces SW refresh on reload)
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
