# Fog osagaien fitxategiak

Karpeta honek kontzeptu-probarako garatu diren osagaien kodea eta beraien exekuzioa ahalbidetzeko beharrezko fitxategiak gordetzen ditu. Hala nola, Fog osagai bakoitzak gutxienez bi fitxategi mota desberdin edukiko ditu:

- **Dockerfile fitxategia**: Fog osagaiaren oinarri-irudia sortzeko definizio fitxategia. Docker irudia izanda, fitxategi honi _Dockerfile_ deritzo.
- **Iturri-kodearen fitxategia**: Fog osagaiaren funtzionalitatearen exekuziorako fitxategia.
- **Fog osagairen eredua**: Fog osagaiaren eredua XML formatuan.

Azter daitekeenez, Fog osagai bakoitza programazio-lengoaia desberdin batekin garatu da. Beraz, beraien `Dockerfile` fitxategiaren edukia desberdina izango da, bertan aukeratutako irudiarekin batera.

## Fog osagai-programatzaileentzako jarraibideak

Fog osagai programatzaileak jarraitu beharreko pausoak hurrengoak dira:

1. Iturri-kodearen fitxategia garatu.
2. Iturri-kodearen programazio-lengoaia eta programak behar dituen baliabideak kontuan edukiz, Dockerfile fitxategia garatu.
3. Fog osagairen oinarri-irudia sortu eta irudi-errepositoriora igo. Horretarako, aurreko bi pausoetako fitxategiak sortuta egon behar dira. Ondoren, irudiaren izena (Docker terminologian `tag` edo etiketa) zehaztu beharko du, eta hurrengo komandoak erabiliz, irudia sortu eta errepositoriora igo daiteke.
    ```
    docker build -f <Dockerfile fitxategia> -t <oinarri-irudiaren etiketa> .
    ```
    ```
    docker push <oinarri-irudiaren etiketa>
    ```
4. Fog osagaiaren XML eredua garatu.