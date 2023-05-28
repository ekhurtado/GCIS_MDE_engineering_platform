import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import sun.misc.IOUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.stream.Collectors;

// Buscar el
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class zenbakienAurkezpena {

//     String function = System.getenv("SERVICE");
//     String inPortNumber = System.getenv("INPORT_NUMBER");
//     String customization = System.getenv("CUSTOMIZATION");

    // TODO Ezabatu
    static String function = "consoleDisplay";
    static int inPortNumber = Integer.parseInt("7000");
    static String customization = "{\"filename\": \"datu_fitxategia\"}";

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(inPortNumber), 0);
        HttpContext context = server.createContext("/");
        context.setHandler(BasicHttpServerExample::handleRequest);
        System.out.println("Starting HTTP server...");
        server.start();
    }

    private static void handleRequest(HttpExchange exchange) throws IOException {

        URI requestURI = exchange.getRequestURI();
        System.out.println("Request URI: " + requestURI);
        System.out.println("Query: " + requestURI.getQuery());

        System.out.println("Headers: ");
        Headers requestHeaders = exchange.getRequestHeaders();
        requestHeaders.entrySet().forEach(System.out::println);

        System.out.println("Principal: " + exchange.getPrincipal());
        System.out.println("HTTP method: " + exchange.getRequestMethod());

        String body = new BufferedReader(
                new InputStreamReader(exchange.getRequestBody(), StandardCharsets.UTF_8)).lines()
                .collect(Collectors.joining("\n"));
        System.out.println("Request body: " + body);

        // Aurreko osagaiari mezua ondo lortu dela esaten diogu
        String response = "OK";
        exchange.sendResponseHeaders(200, response.getBytes().length);//response code and length

        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();

        // Mezu lortuta, aukeratutako funtzionalitatea exekutatuko da
        switch (function) {
            case "consoleDisplay":
                consoleDisplay(body);
                break;
            case "saveTXT":
                saveTXT(body);
                break;
            case "saveCSV":
                saveCSV(body);
                break;
            default:
                System.out.println("Ez da funtzionalitaterik aukeratu.");
                break;
        }
    }

    public static void consoleDisplay(String messageData) {
    // Lehenengo, HTTP mezutik informazio lortuko dugu
        JsonReader jsonReader = Json.createReader(new StringReader(messageData));
        JsonObject jsonObject = jsonReader.readObject();
        String type = jsonObject.getString("type");
        switch (type) {
            case "natural":
            case "integer":
                int value = jsonObject.getInt("value");
                System.out.println("Lortutako balioa" + value + " da.");
                break;
            case "float":
//                 double  value = jsonObject.getJsonNumber("value").doubleValue();
                float floatValue = jsonObject.getJsonNumber("value").floatValue();
                System.out.println("Lortutako balioa" + floatValue + " da.");
                break;
            default:
                System.out.println("Lortutako balioaren mota ez da zuzena.");
                break;
        }
    }

    public static void saveTXT(String messageData) {
        // Lehenengo, HTTP mezutik informazio lortuko dugu
        JsonReader jsonReader = Json.createReader(new StringReader(messageData));
        JsonObject jsonObject = jsonReader.readObject();
        String type = jsonObject.getString("type");

        // Ondoren, fitxategiaren izena lortuko dugu
        JsonReader jsonReader = Json.createReader(new StringReader(customization));
        JsonObject jsonObject = jsonReader.readObject();
        String fileName = jsonObject.getString("filename");
        if (!fileName.contains(".txt")) {
            fileName = fileName + ".txt";
        }

        // Create a FileWriter instance
        FileWriter fileWriter = new FileWriter(fileName);
        // Create a BufferedWriter instance for efficient writing
        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

        switch (type) {
            case "natural":
            case "integer":
                int value = jsonObject.getInt("value");
                bufferedWriter.write("Lortutako balioa" + value + " da.\n");
                break;
            case "float":
//                 double  value = jsonObject.getJsonNumber("value").doubleValue();
                float floatValue = jsonObject.getJsonNumber("value").floatValue();
                bufferedWriter.write("Lortutako balioa" + floatValue + " da.\n");
                break;
            default:
                System.out.println("Lortutako balioaren mota ez da zuzena.");
                break;
        }

        // Close the BufferedWriter
        bufferedWriter.close();

    }

    public static void saveCSV(String messageData) {
        // Lehenengo, HTTP mezutik informazio lortuko dugu
        JsonReader jsonReader = Json.createReader(new StringReader(messageData));
        JsonObject jsonObject = jsonReader.readObject();
        String type = jsonObject.getString("type");

        // Ondoren, fitxategiaren izena lortuko dugu
        JsonReader jsonReader = Json.createReader(new StringReader(customization));
        JsonObject jsonObject = jsonReader.readObject();
        String fileName = jsonObject.getString("filename");
        if (!fileName.contains(".csv")) {
            fileName = fileName + ".csv";
        }

        // Create a FileWriter instance
        FileWriter fileWriter = new FileWriter(fileName);
        // Create a BufferedWriter instance for efficient writing
        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

        switch (type) {
            case "natural":
            case "integer":
                int value = jsonObject.getInt("value");
                bufferedWriter.write(type + "," + value + "\n");
                break;
            case "float":
//                 double  value = jsonObject.getJsonNumber("value").doubleValue();
                float floatValue = jsonObject.getJsonNumber("value").floatValue();
                bufferedWriter.write(type + "," + floatValue + "\n");
                break;
            default:
                System.out.println("Lortutako balioaren mota ez da zuzena.");
                break;
        }

        // Close the BufferedWriter
        bufferedWriter.close();
    }
}