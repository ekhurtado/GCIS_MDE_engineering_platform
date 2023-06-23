# Node-RED plataformaren abiarazpena

Karpeta honetan Node-RED plataforma abiarazteko fitxategiak multzokatu dira. Deskribapen honetan, plataforma abiarazteko aukera desberdinak aurkeztuko dira, eta baita sortzen den fitxategi-egitura ere.

## Node-RED plataformaren Docker irudia
Lehenik eta behin, aipatu beharra dago Node-RED plataformaren Docker irudia jada sortuta dagoela, eta DockerHub errepositorioan biltegiratuta, `ekhurtado/gcis-fog:nodered` etiketarekin eskuragarri dagoena. Hala ere, eraiki nahi izanez gero, bi aukera daude (betiere karpeta honetan kokatu komando-lerroko interfaze bat ireki behar duzu):

- Docker-compose fitxategia erabili nahi izanez gero, Docker instalatuta dagoen gailu batean hurrengo komandoa exekutatu:
```
docker-compose build
```
- Zuzenean Dockerfile fitxategia erabilita irudia sortu nahi bada, hurrengo komandoa erabil ezazu
```
docker build -f Dockerfile_NodeRed -t ekhurtado/gcis-fog:nodered .
```

Irudia eraikita dagoenean (`docker images` komandoarekin konproba dezakezu), errepositoriora igo dezakezu. Hori bai, kontuan eduki _ekhurtado_ MAL honen egilearen errepositorio pribatua dela, beraz, zeurearekin aldatu.

## Node-RED plataformaren abiarazpena
Irudia errepositorioan edukita, abiarazi ahalko dugu. Horretarako ere bi aukera daude, plataforma non abiarazi nahi den kontuan edukiz.

### Gailu lokaleko abiarazpena
Gailu lokalean exekuta nahi bada, hurrengo Docker komandoak erabil ditzakezu (aurrekoaren berdina, _docker-compose_ erabiltzea aukeratzen baduzu edo _Docker_ normala):
```
docker-compose build
```
edo
```
 docker run -it -p 1880:1880 -v node_red_data:/data --name nodered ekhurtado/gcis-fog:nodered
```
### Kubernetesen abiarazpena
Kubernetes inplementazio-plataforma bezala aukeratu denez, Node-RED tresna abiarazteko erabil daiteke, nahi izanez gero. Horretarako `Kubernetes_hedatze_fitxategiak` karpetako fitxategi guztiak Kubernetes klusterrean hedatu beharko dira.

Egin behar den gauza bakarra, klusterraren nodo nagusian komando-lerroko interfaze bat ireki, fitxategi guzti horiek karpeta berdinean kopiatu, eta hurrengo komando exekutatu:
```
kubectl apply -f .
```

## Node-RED plataformaren egitura eta nola atzitu 
Node-RED abiarazita dagoenean, 1880 portuan egongo da entzuten. Bertara sartuz, plataformaren interfaze grafikoa irekiko zaigu. Gailu lokalean abiarazi bada, nabigatzailean honako webgunea sar ezazu:
```
http://localhost:1880
```
Kubernetes abiarazpen-plataforma bezala erabili baduzu, nodo nagusiko IP helbidea lor ezazu, eta nabigatzailea hona joan:
```
http://<nodo nagusiko IP helbidea>:31880
```

Azkenik, plataformaren egitura aurkeztuko da. Bi aukerekin Dockerreko _volume_ baliabidea erabili denez, Node-REDen nodo perstonalizatuak gailuko karpeta batean egongo dira. Gailu lokala Linux sistema eragilea badauka, nodo pertsonalizatuak hurrengo karpeta egongo dira (agian `sudo` erabili behar da baimenengatik):
```
/var/lib/docker/volumes/nodered_node-red-data/_data/node_modules
```

Kubernetesen kasuan, zein langile-nodoan abiarazi den aztertu beharko da, eta gailu horren karpeta nagusian egongo da:
```
/nodered/data/node_modules
```

Nodo berriak sartzeko, karpeta horretara kopiatu beharko dira (nodoaren karpeta guztia) eta Node-RED plataforma berrabiarazi. Horrela, nodoak tresnaren interfaze grafikoaren liburutegian egongo dira eskuragarri.