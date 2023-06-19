import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.stream.Collectors;

// JSON objektuak irakurtzeko liburutegia
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class ZenbakienAurkezpena {

     static String function = System.getenv("SERVICE");
     static int inPortNumber = Integer.parseInt(System.getenv("INPORT_NUMBER"));
//     String customization = System.getenv("CUSTOMIZATION");
//	static String fileName = System.getenv("CUSTOM_FILENAME");
	static String fileName = System.getenv("CUSTOM_FITXATEGIIZEN");

    // TODO Ezabatu
//    static String function = "saveTXT";
//    static int inPortNumber = Integer.parseInt("7000");
////    static String customization = "{\"filename\": \"datu_fitxategia\"}";
//    static String fileName = "datuak.txt";

    static JSONParser jsonParser = null;
    static JSONObject jsonObject = null;
    static DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
    static int id = 0;

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", inPortNumber), 0);
        HttpContext context = server.createContext("/");
        context.setHandler(ZenbakienAurkezpena::handleRequest);
//        System.out.println("Starting HTTP server in port " + inPortNumber + "...");
        server.start();
    }

    private static void handleRequest(HttpExchange exchange) throws IOException {

//        URI requestURI = exchange.getRequestURI();
//        System.out.println("Request URI: " + requestURI);
//        System.out.println("Query: " + requestURI.getQuery());

//        System.out.println("Headers: ");
//        Headers requestHeaders = exchange.getRequestHeaders();
//        requestHeaders.entrySet().forEach(System.out::println);

//        System.out.println("Principal: " + exchange.getPrincipal());
//        System.out.println("HTTP method: " + exchange.getRequestMethod());

        String body = new BufferedReader(
                new InputStreamReader(exchange.getRequestBody(), StandardCharsets.UTF_8)).lines()
                .collect(Collectors.joining("\n"));
//        System.out.println("Request body: " + body);

        // Aurreko osagaiari mezua ondo lortu dela esaten diogu
        String response = "OK\n";
        exchange.sendResponseHeaders(200, response.getBytes().length);	//response code and length
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();


        // Mezu lortuta, aukeratutako funtzionalitatea exekutatuko da
        switch (function) {
//            case "consoleDisplay":
            case "PantailaAurkezpen":
                consoleDisplay(body);
                break;
//            case "saveTXT":
            case "GordeTXT":
                saveTXT(body);
                break;
//            case "saveCSV":
            case "GordeCSV":
                saveCSV(body);
                break;
            default:
                System.out.println("Ez da funtzionalitaterik aukeratu.");
                break;
        }
    }

    public static void consoleDisplay(String messageData) {
    	// Lehenengo, HTTP mezutik informazio lortuko dugu
    	jsonParser = new JSONParser();
		try {
			jsonObject = (JSONObject) jsonParser.parse(messageData);
		} catch (ParseException e) {
			System.err.println("Heldutako JSON mezua ez da zuzena.");
			e.printStackTrace();
		}

		// Datuak kontsolatik erakusten hasiko gara. Hasteko, datuen data zehatza lortuko da
		System.out.println("-----------");
		System.out.println("Datu berria:");
		System.out.println("	-> Datuen data: " + dtf.format(LocalDateTime.now()));

        String type = (String) jsonObject.get("type");
        System.out.println("	-> Zenbaki mota: " + type);
        switch (type) {
            case "natural":
            case "integer":
                int value = ((Long) jsonObject.get("value")).intValue();
                System.out.println("	-> Lortutako balioa: " + value);
                break;
            case "float":
                Double floatValue = (Double) jsonObject.get("value");
                System.out.println("	-> Lortutako balioa: " + floatValue);
                break;
            default:
                System.out.println("	-> Lortutako balioaren mota ez da zuzena.");
                break;
        }
        System.out.println("-----------");

    }

    public static void saveTXT(String messageData) throws IOException {
        // Lehenengo, HTTP mezutik informazio lortuko dugu
    	jsonParser = new JSONParser();
		try {
			jsonObject = (JSONObject) jsonParser.parse(messageData);
		} catch (ParseException e) {
			System.err.println("Heldutako JSON mezua ez da zuzena.");
			e.printStackTrace();
		}

        // Ondoren, fitxategiaren izena lortuko dugu
        if (!fileName.contains(".txt"))
            fileName = fileName + ".txt";

        // Create a FileWriter instance
        FileWriter fileWriter = new FileWriter(fileName, true);
        // Create a BufferedWriter instance for efficient writing
        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

        bufferedWriter.write("-----------\n");
        bufferedWriter.write("Datu berria:\n");
		bufferedWriter.write("	-> Datuen data: " + dtf.format(LocalDateTime.now()) + "\n");

		String type = (String) jsonObject.get("type");
		bufferedWriter.write("	-> Datuen mota: " + type + "\n");
        switch (type) {
            case "natural":
            case "integer":
                int value = ((Long) jsonObject.get("value")).intValue();
                bufferedWriter.write("	-> Lortutako balioa: " + value + "\n");
                break;
            case "float":
            	Double floatValue = (Double) jsonObject.get("value");
                bufferedWriter.write("	-> Lortutako balioa: " + floatValue + "\n");
                break;
            default:
                System.out.println("	-> Lortutako balioaren mota ez da zuzena.\n");
                break;
        }
        bufferedWriter.write("-----------\n");

        // Close the BufferedWriter
        bufferedWriter.close();
        System.out.println("Datuak TXT fitxategian zuzen gordeta.");
    }

    public static void saveCSV(String messageData) throws IOException {
        // Lehenengo, HTTP mezutik informazio lortuko dugu
    	jsonParser = new JSONParser();
		try {
			jsonObject = (JSONObject) jsonParser.parse(messageData);
		} catch (ParseException e) {
			System.err.println("Heldutako JSON mezua ez da zuzena.");
			e.printStackTrace();
		}

        // Ondoren, fitxategiaren izena lortuko dugu
        if (!fileName.contains(".csv")) {
            fileName = fileName + ".csv";
        }

        // Create a FileWriter instance
        FileWriter fileWriter = new FileWriter(fileName, true);
        // Create a BufferedWriter instance for efficient writing
        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

        if (id == 0)	// lehenengo aldia bada, datuen izenburuak zehaztuko ditugu
        	bufferedWriter.write("id,type,value,time\n");

        String type = (String) jsonObject.get("type");
        switch (type) {
            case "natural":
            case "integer":
            	int value = ((Long) jsonObject.get("value")).intValue();
                bufferedWriter.write(id + "," + type + "," + value + ",\"" + dtf.format(LocalDateTime.now()) + "\"\n");
                break;
            case "float":
            	Double floatValue = (Double) jsonObject.get("value");
                bufferedWriter.write(id + "," + type + "," + floatValue + ",\"" + dtf.format(LocalDateTime.now()) + "\"\n");
                break;
            default:
                System.out.println("Lortutako balioaren mota ez da zuzena.");
                break;
        }
        id += 1;

        // Close the BufferedWriter
        bufferedWriter.close();
        System.out.println("Datuak CSV fitxategian zuzen gordeta.");
    }
}