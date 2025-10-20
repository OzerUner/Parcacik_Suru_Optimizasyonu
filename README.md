🌀 Parçacık Sürü Optimizasyonu - PyQt5

Python ve PyQt5 ile geliştirilmiş, Parçacık Sürü Optimizasyonu algoritmasını görselleştiren bir masaüstü uygulamasıdır. 
Kullanıcılar algoritmanın parametrelerini değiştirip en iyi çözümü (gbest) ve uygunluk değerini anlık olarak görebilir. 
Parametreler arasında parçacık sayısı, maksimum iterasyon, inersya (w), bilişsel (c1), sosyal (c2) katsayılar ve X min/max sınırları bulunmaktadır. 
Canlı sonuçlar modern bir arayüz ile gösterilir. Örnek problem olarak f(x) = x^2 + 2x - 3 fonksiyonu kullanılmıştır ve amaç 0’a en yakın değeri bulmaktır 
(yaklaşık kökler x = -3 ve x = 1).

Kurulum ve Kullanım: 
Python 3.x yüklü olmalıdır. 
PyQt5 paketi yüklemek için `pip install PyQt5` komutunu çalıştırın. 
Arayüzdeki parametreleri ayarlayın: Parçacık Sayısı, Maksimum İterasyon, İnertya (w), Bilişsel (c1) ve Sosyal (c2) katsayılar, X Min/Max sınırları. 
"Optimizasyonu Başlat" butonuna tıklayın. Sonuçlar ekranda görüntülenecektir: En İyi Pozisyon (gbest) ve En İyi Uygunluk Değeri. 
Aynı parametrelerle farklı sonuçlar görebilirsiniz; PSO stohastik bir algoritmadır.
Uygulama, kullanıcıların kendi uygunluk fonksiyonlarını doğrudan matematiksel ifade olarak yazabilmesini destekler.
Fonksiyon yalnızca x değişkenini kullanır.math modülü kullanılabilir (math.sin, math.cos, math.exp, vb.).
Kod güvenliği için eval yalnızca x ve math ile sınırlıdır;.
Fonksiyon hatalı yazılırsa uygulama çökmez. Uyarı mesajı gösterir ve optimizasyon başlatılmaz.
Min X değeri Max X değerinden küçük olmalıdır. Maksimum iterasyon ve parçacık sayısı çok yüksekse performans düşebilir. 

Arayüz Tasarımı: 
Arka Plan: Açık mavi (#f0f8ff), 
GroupBox: Açık mavi (#e6f2fa), 
Çerçeve: Koyu mavi (#0b58a5), 
Buton: Koyu mavi (#0b58a5), 
Hover: #09477a, 
Pressed: #083a62. 
<img width="600" height="688" alt="image" src="https://github.com/user-attachments/assets/bc057d9e-8b5b-4685-b833-168fb7357590" />
