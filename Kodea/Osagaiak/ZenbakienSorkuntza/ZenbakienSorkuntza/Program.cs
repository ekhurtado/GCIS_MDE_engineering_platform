using System;
using System.Globalization;

public class ZenbakienSorkuntza
{

    static string function = Environment.GetEnvironmentVariable("SERVICE");
//    static string customization = Environment.GetEnvironmentVariable("CUSTOMIZATION");

//    static string type = Environment.GetEnvironmentVariable("CUSTOM_TYPE");
    static string type = Environment.GetEnvironmentVariable("CUSTOM_MOTA");
//    static string firstValue = Environment.GetEnvironmentVariable("CUSTOM_FIRSTVALUE");
    static string firstValue = Environment.GetEnvironmentVariable("CUSTOM_HASIERAKOBALIOA");

    static string output = Environment.GetEnvironmentVariable("OUTPUT");
    static string output_port = Environment.GetEnvironmentVariable("OUTPUT_PORT");

//    static string function = "FloatValue";
//    static string type = "decreasingValue";
//    static string firstValue = "3.5";
//    static string output = "localhost";
//    static string output_port = "7000";
    static string url = "http://"+output+":" + output_port; // Replace with the desired URL

    public static async Task Main(string[] args)
    {
        Console.WriteLine("Kaixo! Ongi etorri ZenbakienSorkuntza aplikaziora");

        Thread.Sleep(5000); // 5 segundo itxarongo ditugu beste osagaiek zuzen abiarazteko

        // Send a GET request
//        await Utils.SendGetRequest(url);

        // Send a POST request
//        string requestBody = "This is a simple string as the request body.";
//        await Utils.SendPostRequest(url, requestBody);

        // TODO EZABATU (INGURUNE-ALDAGAI BEZALA HARTU BEHAR DIRA)
//        string function = "FloatValue";

        Console.WriteLine(function);

        switch (function)
        {
//            case "NaturalValue":
            case "BalioNaturalak":
                await NaturalValue();
                break;
//            case "IntegerValue":
            case "BalioOsoak":
                await IntegerValue();
                break;
//            case "FloatValue":
            case "BalioDezimalak":
                await FloatValue();
                break;
            default:
                Console.WriteLine("Invalid function name.");
                break;
        }
    }

    public static async Task NaturalValue()
    {
        Console.WriteLine("NaturalValue funtzioa aukeratuta");
        // TODO EZABATU (INGURUNE-ALDAGAI BEZALA HARTU BEHAR DIRA)
//        string customization = @"{""type"": ""decreasingValue"", ""firstvalue"": 3}";

        // Lehenengo aldian hasierako zenbakia bidaliko da
//        (string type, int firstValue) = Utils.getCustomizationValues(customization);
        int intFirstValue = int.Parse(firstValue);
        string requestBody = @"{""type"": ""natural"",""value"": " +intFirstValue+ "}";
        await Utils.SendPostRequest(url, requestBody);  // Send a POST request
        Console.WriteLine(requestBody);
        Thread.Sleep(5000); // Pause for 5 seconds

        int createdValue = intFirstValue;
        while (true)
        {
            createdValue = Utils.getNaturalValue(type, createdValue);
            Console.WriteLine("Created value: " + createdValue);

            // Sortutako zenbakia bidaltzen dugu
            requestBody = @"{""type"": ""natural"",""value"": " +createdValue+ "}";
            try {
                await Utils.SendPostRequest(url, requestBody);  // Send a POST request
            } catch(Exception e) {
                // perhaps log exception?
                Console.Write("Konexio errorea!");
            }

            // Pause for 5 seconds
            Thread.Sleep(5000);
        }

    }

    public static async Task IntegerValue()
    {
        Console.WriteLine("IntegerValue funtzioa aukeratuta");

        // TODO EZABATU (INGURUNE-ALDAGAI BEZALA HARTU BEHAR DIRA)
//        string customization = @"{""type"": ""decreasingValue"", ""firstvalue"": 3}";

        // Lehenengo aldian hasierako zenbakia bidaliko da
//        (string type, int firstValue) = Utils.getCustomizationValues(customization);
        int intFirstValue = int.Parse(firstValue);
        string requestBody = @"{""type"": ""integer"",""value"": " +intFirstValue+ "}";
        await Utils.SendPostRequest(url, requestBody);  // Send a POST request
        Console.WriteLine(requestBody);
        Thread.Sleep(5000); // Pause for 5 seconds

        int createdValue = intFirstValue;
        while (true)
        {
            createdValue = Utils.getIntegerValue(type, createdValue);
            Console.WriteLine("Created value: " + createdValue);

            // Sortutako zenbakia bidaltzen dugu
            requestBody = @"{""type"": ""integer"",""value"": " +createdValue+ "}";
            try {
                await Utils.SendPostRequest(url, requestBody);  // Send a POST request
            } catch(Exception e) {
                // perhaps log exception?
                Console.Write("Konexio errorea!");
            }

            // Pause for 5 seconds
            Thread.Sleep(5000);
        }
    }

    public static async Task FloatValue()
    {
        Console.WriteLine("FloatValue funtzioa aukeratuta");

        // TODO EZABATU (INGURUNE-ALDAGAI BEZALA HARTU BEHAR DIRA)
//        string customization = @"{""type"": ""random"", ""firstvalue"": 2.5}";

        // Lehenengo aldian hasierako zenbakia bidaliko da
//        (string type, float firstValue) = Utils.getCustomizationValuesF(customization);
        float floatFirstValue = float.Parse(firstValue, CultureInfo.InvariantCulture.NumberFormat);
        string valueString = floatFirstValue.ToString().Replace(',', '.');   // C# lengoaian float-ak komarekin erabiltzen dira
        string requestBody = @"{""type"": ""float"",""value"": " +valueString+ "}";
        await Utils.SendPostRequest(url, requestBody);  // Send a POST request
        Console.WriteLine(requestBody);
        Thread.Sleep(5000); // Pause for 5 seconds

        float createdValue = floatFirstValue;
        while (true)
        {
            createdValue = Utils.getFloatValue(type, createdValue);
            Console.WriteLine("Created value: " + createdValue);

            // Sortutako zenbakia bidaltzen dugu
            valueString = createdValue.ToString("0.00").Replace(',', '.');
            requestBody = @"{""type"": ""float"",""value"": " +valueString+ "}";
            try {
                await Utils.SendPostRequest(url, requestBody);  // Send a POST request
            } catch(Exception e) {
                // perhaps log exception?
                Console.Write("Konexio errorea!");
            }

            // Pause for 5 seconds
            Thread.Sleep(5000);
        }
    }
}