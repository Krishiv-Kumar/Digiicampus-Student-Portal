const CACHE_NAME = 'portal-shell-v1';
const ASSETS = [
  './',
  './index.html',
  './demo_data.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('fetch', (e) => {
  if (e.request.url.includes('/api/')) return;
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});