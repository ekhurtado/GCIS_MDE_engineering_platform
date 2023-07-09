# IDE_plataforma

Karpeta honek IDE plataformaren kode guztia barneratzen du. Aukeratutako IDEa Node-RED izanik, bertan zuzenean integra daitezkeen nodoen fitxategiak ere eskuragarri daude.

Karpeta honen antolakuntza hurrengoa da:

- [nodoak](https://github.com/ekhurtado/EkaitzHurtado-MAL/tree/main/Kodea/IDE_plataforma/nodoak): Fog Computing Liburutegia osatzen duten Fog osagaien nodoen fitxategiak biltegiratzen dira karpeta honetan.
- [plataforma_abiarazpena](https://github.com/ekhurtado/EkaitzHurtado-MAL/tree/main/Kodea/IDE_plataforma/plataforma_abiarazpena): Kasu honetan Node-RED plataforma abiarazteko fitxategiak aurkezten dira. Gainera, barruan beste _README_ fitxategi bat gehitu da abiarazpena zuzen gauzatzeko jarraibideekin. 
- [txantiloiak](https://github.com/ekhurtado/EkaitzHurtado-MAL/tree/main/Kodea/IDE_plataforma/txantiloiak): Karpetan honetan MAL honek proposatutako ikuspegian beharrezko txantiloiak biltegiratzen dira. Hain zuzen ere, honela antolatuta dago:
  - [customNode](https://github.com/ekhurtado/EkaitzHurtado-MAL/tree/main/Kodea/IDE_plataforma/txantiloiak/customNode): Honek Node-RED plataformarako nodo pertsonalizatuak sortzeko beharrezko baliabideak barneratzen ditu. Horietatik hauek nabarmentzen dira:
    - [nodeGenerator.py](https://github.com/ekhurtado/EkaitzHurtado-MAL/blob/main/Kodea/IDE_plataforma/txantiloiak/customNode/nodeGenerator.py): Nodo-pertsonalizatuak automatikoki sortzeko programa. Honi Fog osagaien eredu bat pasa behar zaio, eta automatikoki nodo pertsonalizatuko fitxategi guztiak sortu eta programa exekutatzen den leku bereko karpeta batean gordeko ditu. Programa abiarazteko honakoa komandoa exekuta daiteke komando-lerroko interfaze batean:
    ```
    python3 nodeGenerator.py
    ```
    - [webView.xslt](https://github.com/ekhurtado/EkaitzHurtado-MAL/blob/main/Kodea/IDE_plataforma/txantiloiak/customNode/webView.xslt): Nodo-pertsonalizatuen atal bisuala sortzeko XSLT fitxategia.
    - [functionalPart.xslt](https://github.com/ekhurtado/EkaitzHurtado-MAL/blob/main/Kodea/IDE_plataforma/txantiloiak/customNode/functionalPart.xslt): Nodo-pertsonalizatuen atal funtzionala sortzeko XSLT fitxategia.
