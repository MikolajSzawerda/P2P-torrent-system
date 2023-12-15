## Komunikacja TCP

Kaszyński Dawid, Jakub Jażdżyk, Mikołaj Szawerda, Wojciech Zarzecki

---

## Polecenie

Napisać zestaw programów - klienta i serwera - komunikujących się poprzez TCP.
1. Napisać klient/serwer przesyłające między sobą złożoną strukturę danych
2. Napisać modyfikację 1. posługującą się IPv6
3. Zbadać wpływ zmiany rozmiaru bufora nadawczego

## Zad 2.1

## Zad 2.2

## Zad 2.3

### Zmiana rozmiaru bufora

```c
int bufferSize = argc > 1 ? atoi(argv[1]) : 1024;
if (setsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &bufferSize, sizeof(bufferSize)) < 0) {
    perror("Error setting socket options");
    close(sockfd);
    exit(EXIT_FAILURE);
}
```

Eksperymenty zostały wykonane dla parametrów:
- czas blokady serwera: 200ms
- wysyłane dane: 3500B
- bufor nadawczy klienta: 1024B, 4096B, 16384B(należało zwrócić uwagę na dolne i górne ograniczenia wyznaczone przez OS)
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