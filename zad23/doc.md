Eksperymenty zostały wykonane dla parametrów:
- czas blokady serwera: 200ms
- wysyłane dane: 3500B
- bufor nadawczy klienta: 1024B, 4096B, 16384B
- bufor odbiorczy serwera: 8192B

## Wykresy

### Bufor 1024
![](log1024-plot.png)

![](thr-1024.png)

### Bufor 4096
![](log4096-plot.png)
![](thr-4096.png)

### Bufor 16384
![](log16384-plot.png)
![](thr-16384.png)

### Ustalanie okna

![](ss.png)



## Wnioski

- w przypadku bufora 1024B można zaobserwować obszar w którym klient przy każdym wysłaniu był blokowany
- w czasach wysłania występują piki, które świadczą o momencie przepełnienia bufora i konieczności zablokowania klienta
- dla małych wartości na osi OX można zaobserować brak pików - jest to moment w którym serwer i klient przetwarzali dane bez przestojów, bufory obu nie były jeszcze przepełnione
- w raz z wzrostem wielkości bufora malał czas blokady klienta, oraz ilość występowania owych blokad
- Korzystając z narzędzia wireshark można było zaobserwować przesył ramek z ustawieniem okna na 0