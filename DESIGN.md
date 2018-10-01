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


# Uporabniki in prijava
Prijava bo potekala preko sistema Armes AAI, ki uporablja protokol SAML2. 
