# DegenKit blog — yazı ekleme

Panel yok, veritabanı yok: yazılar bir metin dosyası, site tamamen statik. Güvenlik açısından yorum, giriş ve sunucu kodu bulunmuyor.

## Yeni yazı nasıl eklenir
1. `blog-src/posts/_example.md` dosyasını kopyala, adını `2026-11-yazi-adi.md` yap (başında `_` olmasın).
2. Üstteki bilgileri doldur (title, date, excerpt, cover, tags). Altına yazıyı yaz.
3. Görselleri `blog/img/` klasörüne koy, yazıda `/blog/img/dosya.webp` diye çağır.
4. `python3 blog-src/build.py` çalıştır. Liste, yazı sayfaları, RSS ve sitemap otomatik güncellenir.
5. Siteyi yeniden yükle. (İstersen yazıyı ve görselleri bana ver, ben derleyip zip'leyeyim.)

`draft: true` yazarsan yazı yayınlanmaz. Yazar adı gösterilmez, her yazı "DegenKit" imzalı çıkar.

## Görsel ölçüleri
- Kapak: 1600×900 px (16:9), WebP, mümkünse 300 KB altı. Liste, yazı başı ve X paylaşım önizlemesi bunu kullanır.
- Yazı içi görsel: 1400 px genişlik yeterli. Aralara istediğin kadar koyabilirsin.
- GIF yerine kısa `.mp4` (sessiz, döngülü) çok daha hafiftir; aynı şekilde eklenir.

## Güvenlik notları
- Yazı içinde ham HTML/JS çalışmaz, her şey kaçışlanır. Sadece güvenli bağlantılar (http, https, mailto, site içi) kabul edilir.
- Dış bağlantılar `noopener noreferrer` ile yeni sekmede açılır.
- YouTube videoları `youtube-nocookie.com` ile gömülür.
