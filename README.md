# Projekt na Programowanie aplikacji mobilnych i webowych

[![Board Status](https://dev.azure.com/01133318/58577f27-c36e-47d0-9166-d776046c9d72/b8c46cd8-ad29-4083-8158-d84b59d074b3/_apis/work/boardbadge/1c7d0226-0595-4aa6-b9e1-2e99eadfd43d)](https://dev.azure.com/01133318/58577f27-c36e-47d0-9166-d776046c9d72/_boards/board/t/b8c46cd8-ad29-4083-8158-d84b59d074b3/Microsoft.RequirementCategory)

Realizacja kolejnych etapów projektów laboratoryjnych.

## Cel projektu

Napisanie aplikacji do zarządzania źródłami w pracach naukowych.

## Etap 1 - Formularz rejestracyjny

Opracowanie formularza rejestracyjnego dla nowych użytkowników. Formularz musi pozwalać na **walidowanie wszystkich pól na bieżąco**. Kod JavaScript, HTML i CSS muszą być od siebie **odesparowane**. Komunikaty błędów muszą być tworzone dynamicznie przez kod JS. Polę login użytkownika będzie sprawdzane pod kątem dostępności **asynchronicznie**. Dane do rejestracji będą przesyłane do na zewnętrzny serwer. Kod HTML i CSS musi przechodzić walidację.

### Istotne elementy

* czy kod HTML posiada puste węzły na komunikaty (źle, powinny być one dodawane dynamicznie),
* czy wykorzystywane są elementy HTML5 zamiast generycznych, np. `<div class='menu'/>`, `<span id='footer'></span>`,
* jak analizowana jest odpowiedź o dostępności loginu (czy sprawdzany tylko tekst odpowiedzi, czy też kod statusu).

### Uruchomienie Formularza

Strona wymaga **połączenia z Internetem**, ponieważ ładuje biblioteki z CDN oraz sprawdza poprawność loginu na zewnętrznym serwerze.

#### Docker

Zbudowanie obrazu z pliku [Dockerfile](./Dockerfile).  
`docker build -t biblio-cloud .`

Uruchomienie kontenera.  
`run --rm  --name nginx -p 8080:80 -it biblio-cloud`

Następnie strona powinna być dostępna pod adresem [http://localhost:8080](http://localhost:8080/).

#### Docker-compose

Alternatywnie można uruchomić projekt poleceniem `docker-compose up`.

Następnie strona powinna być dostępna pod adresem [http://localhost:8080](http://localhost:8080/).

### Opis plików

Informacja o plikach składających się na projekt.

#### Pliki projektu

* **login.html** - Struktura strony logowania
* **styles/login.css** - Wygląd strony logowania
* **img/** - Obrazy znajdujące się na stronie
* **scripts/script.js** - Skrypt bezpośrednio związany z ekranem logowania
* **scripts/utils.js** - Przydatne funkcje nie będące bezpośrednio związane z projektem
* **scripts/validateExtensions.js** - Dodatkowe funkcje i walidatory związane z biblioteką _validate.js_

#### Pliki konfiguracji (serwer)

* **nginx.conf** - Konfiguracja serwera _Nginx_
* **Dockerfile** - Opis jak zbudować kontener serwujący stronę

----------------------

## Przydatne materiały

* [Pozbywanie się Callback Hell](https://www.nafrontendzie.pl/jak-pozbyc-sie-callback-hell)
* [Testy i mockowanie AJAXa](https://www.nafrontendzie.pl/jquery-deffered-oraz-promise-pigulce)
