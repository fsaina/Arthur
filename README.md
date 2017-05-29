# Sustav za predikciju vremenskih serija 'Arthur'

Sustav za predikciju potrosnje elektricne energije Zvijezda d.d. skladista.
mStart 'Inovativko' natjecanje 2017.

## Instalacija

Za instalaciju potrebno je samo imati noviju verziju Docker-a (https://www.docker.com/)
instaliranu na racunalu i internet preglednik. Cijeli sustav je dockeriziran zbog 
izbjegavanja rucne instalacije niza paketa.

## Koristenje

### Preuzimanje sa Docker Hub-a
Sustav je javno dostupan za preuzimanje sa Docker Hub-a (hub.docker.com).
Ime repositorija je fsaina/arthur te ga najprije preuzmite lokalno sa:

docker pull fsaina/arthur:latest

Ovo ce pokrenuti preuzimanje slike, te kada zavrsi - mozete pokrenuti
jednu instancu sa:

docker run -p 8000:8000 fsaina/arthur

Ovime se pokrenuo Django server

nakon par trenutaka Django server ce se pokrenuti sa ucitanim sustavom 
te mozete pristupiti aplikaciji preko svog internet preglednika na:

localhost:8000


## Struktura direktorija
Direktoriji je podijeljen na 4 poddirektorija, redom:
    - models - Sadrzi sve trenirane modele u Tensorflow-u, kao i finalni koristeni
    - scripts - Sve python skripe (preprocesiranje, dohvat podataka, pokretanje Keras-a)
    - support - Razne informacije o projektu, predvideno kao dokumentacija
    - web - Django server i frontend za prikaz Arthur korisnickog sucelja

## Autor

Filip Saina
filip.saina@gmail.com
