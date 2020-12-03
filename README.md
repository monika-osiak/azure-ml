# EY - Aspect based sentiment analysis
> Projekt w ramach przedmiotu "Wprowadzenie do aplikacji i rozwiązań opartych o Sztuczną Inteligencję i Microsoft Azure", Politechnika Warszawska, Wydział Elektryczny, 2020Z

Autorzy:
1. Monika Osiak (291094) *(liderka grupy projektowej)*,
2. Mikołaj Czarkowski (299240),
3. Jan Dobrowolski (299242),
4. Piotr Ferdynus (299244)

## Opis
### Wstęp
Zadaniem postawionym przez firmę EY jest wykrywanie sentymentu tweetów w języku polskim, w których użyto
danego hasztagu. W zależności od treści tweeta, może on zostać określony jako pozytywny, neutralny lub negatywny.

### Rozwiązanie
Zdecydowaliśmy się na stworzenie prostej aplikacji webowej, dzięki której użytkownik może wpisać hasztag i wybrać
przedział czasowy, w którym mają zawierać się analizowane tweety. W odpowiedzi aplikacja pokaże informacje
o sentymencie znalezionych tweetów w postaci wykresów czytelnych dla użytkownika, a także przykładowe tweety.

Dodatkowo, rozwiązanie zostanie przetestowane na 20 hasztagach zaproponowanych przez firmę, a wyniki zostaną 
zaprezentowane w formie sprawozdania

### Zbiór danych
Aplikacja będzie korzystać z API Twittera w celu pobrania tweetów w języku polskim w zadanym okresie czasu.
Do analizy emocji związanych z wpisami użyjemy modelu dostępnego w Text Analytics API z Microsoft Azure.

### Stos technologiczny
1. Python 3.x:
    1. Flask - aplikacja webowa,
    2. biblioteki do analizy danych: pandas, seaborn, etc.
2. D3.js - wizualizacja danych

## Funkcjonalności
1. Użytkownik podaje hasztag i okres, z jakiego mają pochodzić dane. 
Jako wynik dostaje:
    1. wykres kołowy, który pokazuje ilość tweetów pozytywnych, neutralnych i negatywnych - pokazujący ogólny sentyment,
    2. graficzną prezentację sentymentu w czasie w postaci wykresu liniowego,
    3. 3 przykładowe tweety dla danego hasztagu,
    4. po 3 przykładowe tweety dla danego sentymentu.
2. Analiza hasztagów podanych przez firmę zostanie pokazana w formie sprawozdania w pliku PDF.

## Architektura projektu
Użyte narzędzia Microsoft Azure:
1. Azure App Service - hostowanie aplikacji,
2. Text Analytics API - analiza nacechowania emocjonalnego tweetów,
3. Azure Table Storage - nierelacyjna baza danych, w której przechowywane będą przez pewien czas już przeanalizowane wpisy z przypisanym sentymentem,
4. Azure Functions - cykliczne wywoływanie skryptu czyszczącego bazę danych

![](https://github.com/monika-osiak/azure-ml/blob/readme-update/resources/components.png)

## Harmonogram projektu
| Zajęcia | Data       | Kamień milowy                                                                                     | Uwagi                |
|---------|------------|---------------------------------------------------------------------------------------------------|----------------------|
| P2      | 26.11.2020 | Specyfikacja funkcjonalna projektu                                                                |                      |
| P3      | 10.12.2020 | Skrypt, który pobiera X najnowszych tweetów z podanym hasztagiem                                  | check-point z PO     |
| P4      | 07.01.2021 | Wykonana analiza sentymentu dla tweetów podanych przez firmę                                      |                      |
| P5      | 14.01.2021 | Aplikacja webowa, do której podłączony zostanie model                                             | obecność obowiązkowa |
| P6      | 21.01.2021 | Aplikacja webowa umożliwia analizę dla dowolnych hasztagów z dowolnego przedziału czasowego       |                      |
| P7      | 28.01.2021 | C'est fini mes amis !                                                                             | prezentacja projektu |
