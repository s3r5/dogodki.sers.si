# IP: Sistem za prijavo na športne dneve in obvezne izbirne vsebine

*(inovacijski predlog, oddan na Mladi za napredek Maribora 2019 - področje **računalništvo in informatika**)*

V srednjih in osnovnih šolah se vsako leto srečujemo s prijavami na razne šolske dejavnosti in športne dneve. Pri teh prijavah vedno pride do zmede z zbiranjem prijav na razne aktivnosti, še posebej, če je na izbiro več dejavnosti v enem dnevu in je število mest omejeno. 

Obstoječi sistemi ne omogočajo potrebnega nivoja nadzora (specifično omejitev po oddelkih in podskupinah), hkrati pa rešitve, ki se temu približajo, za uporabo v šolskem okolju z vidika varstva osebnih podatkov niso sprejemljiva.

Cilj je ustvariti sistem, ki bo dijakom olajšal prijavo k šolskim dejavnostim in razvrstitev po skupinah, profesorjem pa omogočil boljši pregled nad udeleženimi. Istočasno, pa bomo poskusili ohraniti sistem čim bolj fleksibilen, da bo lahko uporaben tudi v drugih situacijah, ter poskrbeli za enostavno samo-gostovanje na šolski infrastrukturi (in se tako izognili nevšečnostim z vidika VOP)

## Sposobnosti

 - Uvoz podatkov iz sistema eAsistent
 - Prijava z Arnes AAI ali šolskimi Microsoft računi (odvisno od različice)
 - Razpisovanje dogodkov za oddelke, skupine dijakov in točno določene dijake
 - Pregled povabil in prijav
 - Vodenje evidence prisotnosti

## Struktura

Sistem je zgrajen na platformi Django in za pravilno delovanje potrebuje okolje Python >= 3.5, podprt spletni strežnik in eno izmed podprtih podatkovnih baz (priporočen PostgreSQL). Tehnične podrobnosti so podrobneje opisane v [DESIGN.md](DESIGN.md). Za lažjo namestitev je na voljo tudi konfiguracija Docker in docker-compose.

Konfiguracija poteka s pomočjo okoljskih spremenljivk, prijavni sistem pa je odvisen od veje, ki jo uporabljate (`auth-microsoft` ali `arnes-aai`; enaka imena imata pripadajoči Docker sliki).

## Galerija

![Zaslonska slika domače strani](http://dev.franga2000.com/Ip19/view_main_1.png)

![Zaslonska slika pogleda dogodka](http://dev.franga2000.com/Ip19/view_dogodek_1.png)

## Dovoljenja

Kljub temu, da je polna izvorna koda programa prosto na voljo v pregled javnosti, se s tem ne prenašajo tudi druge pravice (npr. do uporabe ali spreminjanja za lastno rabo). Izvorna koda je javna z namenom zagotavljanja transparentnosti pri obdelavi podatkov. Čeprav možnost kasnejše objave pod odprtokodno licenco ni izključena, se to do sedaj še ni zgodilo in je zato uporaba programa v lastne namene možna le po dogovoru z avtorji.
