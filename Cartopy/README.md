# Otselendude Kaart

See projekt visualiseerib otselende Tallinnast aastatel 2020 (enne Covidit) ja 2023, kasutades cartopy ja matplotlib libary´eid. Lennuandmed loetakse CSV-failidest ja liidetakse lennujaama andmetega, et joonistada lennuliinid kaardil.

### Dependencies

* pandas
* cartopy
* matplotlib

### Kasutus

Käivita Pythoni skript main.py, et luua lennukaart.

### Koodi Selgitus

#### FlightsMap Klass
Klass FlightsMap tegeleb lendude andmetöötluse ja visualiseerimisega.

```__init__(self, precovid_flights, flights23, airports)```

Konstruktor initsialiseerib klassi Covid-eelsete lendude, 2023. aasta lendude ja lennujaama andmetega.

```merge_flight_data(self)```

See meetod ühendab lennuandmed lennujaama andmetega, kasutades võtmena veergu "IATA". Ühendatud andmekogumid salvestatakse uute CSV-failidena.

```create_map(self)```

Selle meetodiga luuakse kaart Lamberti Cylindrical projektsiooniga ning lisatakse rannajooned ja piirid.

```plot_flight_route(row, origin_longitude, origin_latitude, line_color, marker_color, marker, label=None, line_style='-', alpha=1)```

See staatiline meetod joonistab kaardil ühe lennumarsruudi, kasutades antud parameetreid. Lennumarsruut on kujutatud joonena ja sihtkoht on kujutatud markeriga.

```display_map(self)```

Selle meetodiga luuakse kaart, joonistatakse Covidi-eelsed ja 2023. aasta lennud, lisatakse pealkiri ja legend, salvestatakse kaart PNG-failina ja kuvatakse kaart.

```title_and_legend(self, line1, line2)```

See meetod seab kaardile pealkirja ja legendi, kasutades antud joonobjektid.

```plot_flight(self, flight23_coordinates, pre_covid_coordinates, tallinn_latitude, tallinn_longitude)```

Selle meetodi abil joonistatakse antud koordinaatide abil kaardil Covid-eelsed ja 2023. aasta lennud.

### Skripti Käivitamine
1. Initsialiseerige klass FlightsMap, sisestades Covid-eelsete lendude, 2023. aasta lendude ja lennujaama andmete failide pathid:

```flights_map = FlightsMap("otselennud20.csv", "otselennud23.csv", "airports.dat")```

2. Ühendage andmekogumid ja salvestage need uutesse CSV-failidesse:

```flights_map.merge_flight_data()```

3. Kuvage ja salvestage lendude kaart:

```flights_map.display_map()```

### Lisad

![](../../../../var/folders/sc/316bz01161g91ztc36k4mzy00000gn/T/TemporaryItems/NSIRD_screencaptureui_rV8mSl/Screenshot 2023-04-27 at 13.11.52.png)

![](../../Desktop/Screenshot 2023-04-27 at 13.14.58.png)