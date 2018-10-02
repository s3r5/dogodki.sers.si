# Pogledi

## Glavni pogled
Vsak uporabnik po prijavi vidi ta zaslon.

**Odprti dogodki** so vsi dogodki, na katere se uporabnik lahko prijavi.  
**Pretekli dogodki** so dogodki, katerih datum je pretekel pred vsaj 1 dnevom.

![Skica glavnega pogleda](https://dev.franga2000.com/Ip19/design/view_main_1.jpg)

## Ogled dogodka
Prikazuje glavne podatke o dogodku, skupine in prijavljene v njih. 

V glavi vsake skupine je prikazano število prijavljenih in število mest ( *prijavljeni / mesta* ). 
V nezapolnjenih skupinah je pod seznamom prijavljenih gumb za prijavo. Če je uporabnik že prijavljen, je njegovo ime posebej označeno, zravem pa gumb, ki omogoča odjavo.

![Skica pogleda za ogled dogodka](https://dev.franga2000.com/Ip19/design/view_dogodek_1.jpg)

## Urejanje / ustvarjanje dogodka
Pogled omogoča ustvarjanje novega ali urejanje obstoječega dogodka.

Kartica **Podatki o dogodku** omogoča urejanje osnovnih lastnosti dogodka.  
Rubrika **Skupine** vsebuje kartice za posamezne skupine. Gumb **[+]** na dnu doda novo prazno skupino.  
Vsaka **kartica skupine** omogoča urejanje podatkov o posamezni skupini.  
Kartica **povabljeni** omogoča dodajanje uporabnikov na seznam povabljenih. 
> TODO: [Design] kartica za urejanje povabljenih

![Skica pogleda za urejanje dogodka](https://dev.franga2000.com/Ip19/design/view_ustvari_1.jpg)

# Struktura podatkov
Glavni podatkovni tipi so **Dogodek** (predstavlja en dogodek), **Skupina** (predstavlja eno skupino na enem dogodku) in **Uporabnik** (predstavlja enega uporabnika).

Vsak Dogodek lahko ima več Skupin. Vsak Uporabnik je lahko povabljen k večim Dogodkom. Vsak Uporabnik je lahko pod vsakim Dogodkom prijavljen le v eno Skupino.

![Skica sheme relacijske podatkovne baze](https://dev.franga2000.com/Ip19/design/database_1.jpg)

# Uporabniki in prijava
Prijava bo potekala preko sistema Armes AAI, ki uporablja protokol SAML2. 

Trenutni najboljši načrt:

Po prvi prijavi preko AAI se ustvari uporabnik. Ob vsaki prijavi se posodobijo vsi lokalni podatki, ki jih lahko dobimo preko AAI (upam da vsaj ime, priimek, e-pošto, oddelek). Vsak oddelek je skupina uporabnikov. 

# Problemi
> TODO: [Plan] Reši vse probleme z načrtom
 - Če so **vabila vezana na uporabnika** (povabilo oddelka povabi vsakega uporabnika posebej) **imamo težavo s posodabljanjem** (sistem ne ve, da je uporabnik v drugem oddelku, če se ne uporabnik ne prijavi in informacije posodobi iz AAI).  
   - Če so **vabila vezana na oddelke** (povabilo oddelka povabi skupino) **je sistem manj fleksibilen**, a *najverjetneje* reši to težavo
 - Ker **sistem nikoli nima popolnih podatkov o vseh uporabnikih in skupinah** (ker se sproti posodabljajo iz AAI) **je obveščanje neizvedljivo** (če se npr. nek uporabnik ni prijavil odkar je napredoval v naslednji letnik, bi ga sistem še vedno obveščal za dogodke prejšnjega oddelka)