Eksperymenty zostały wykonane dla parametrów:
- czas blokady serwera: 100ms
- bufor nadawczy klienta: 1024B, 8096B, 20480B

## Wykresy

### Bufor 1024
![](log1024-plot.png)

![](thr-1024.png)

### Bufor 8096
![](log8096-plot.png)
![](thr-8096.png)

### Bufor 20480
![](log20480-plot.png)
![](thr-20480.png)



## Wnioski

- w czasach wysłania występują piki, które świadczą o momencie przepełnienia bufora i konieczności zablokowania klienta
- dla małych wartości na osi OX można zaobserować brak pików - jest to moment w którym serwer i klient przetwarzali dane bez przestojów, bufory oby nie były jeszcze przepełnione
- w raz z wzrostem wielkości bufora rosła stabilność przetwarzania serwera i mniejsze czasy blokady, oraz średnia przepustowość