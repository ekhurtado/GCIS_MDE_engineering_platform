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

public class BasicHttpServerExample {

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8500), 0);
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


        String response = "Hi there!";
        exchange.sendResponseHeaders(200, response.getBytes().length);//response code and length




        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}