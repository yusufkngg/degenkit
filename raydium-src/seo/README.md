# SEO notları (degenkit.app)
Yeni sayfa/başlık değiştirince:  `python3 seo/apply_seo.py && python3 blog-src/build.py`
Yeni blog yazısı ekleyince:      `python3 blog-src/build.py`   (sitemap, RSS, şema otomatik)
Deploy sonrası bir kez:          `python3 seo/indexnow.py`      (Bing, Yandex, Naver, Seznam'a anında bildirim)

## Elle yapılacaklar (bende hesap yok, sende yapılır, ~10 dk)
1. Google Search Console → "URL prefix" ile https://degenkit.app/ ekle (DNS TXT ya da HTML meta ile doğrula) → Sitemaps: `sitemap.xml`
2. Bing Webmaster Tools → "Import from Google Search Console" ile tek tıkla içe aktar
3. Yandex Webmaster ve (isteğe bağlı) Naver Search Advisor / Baidu: sitemap.xml ekle
4. Netlify: Domain settings'te www → apex (degenkit.app) yönlendirmesi ve HTTPS açık olsun

## Sıra
`python3 seo/apply_seo.py && python3 seo/add_guides.py && python3 blog-src/build.py` (add_guides, apply_seo'dan SONRA çalışmalı; FAQ schema'sını apply_seo siler).
