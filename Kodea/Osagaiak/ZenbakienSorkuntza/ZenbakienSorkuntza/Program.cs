using System;

public class ZenbakienSorkuntza
{

    static string function = Environment.GetEnvironmentVariable("SERVICE");
    static string customization = Environment.GetEnvironmentVariable("CUSTOMIZATION");
    static string output = Environment.GetEnvironmentVariable("OUTPUT");
    static string output_port = Environment.GetEnvironmentVariable("OUTPUT_PORT");
    static string url = "http://"+output+":" + output_port; // Replace with the desired URL

    public static async Task Main(string[] args)
    {
        Console.WriteLine("Kaixo! Ongi etorri ZenbakienSorkuntza aplikaziora");

        Thread.Sleep(3000); // 3 segundo itxarongo ditugu beste osagaiek zuzen abiarazteko

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
            case "NaturalValue":
                await NaturalValue();
                break;
            case "IntegerValue":
                await IntegerValue();
                break;
            case "FloatValue":
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
        string customization = @"{""type"": ""decreasingValue"", ""firstvalue"": 3}";

        // Lehenengo aldian hasierako zenbakia bidaliko da
        (string type, int firstValue) = Utils.getCustomizationValues(customization);
        string requestBody = @"{""type"": ""natural"",""value"": " +firstValue+ "}";
        await Utils.SendPostRequest(url, requestBody);  // Send a POST request
        Console.WriteLine(requestBody);
        Thread.Sleep(5000); // Pause for 5 seconds

        int createdValue = firstValue;
        while (true)
        {
            createdValue = Utils.getNaturalValue(customization, createdValue);
            Console.WriteLine("Created value: " + createdValue);

            // Sortutako zenbakia bidaltzen dugu
            requestBody = @"{""type"": ""natural"",""value"": " +createdValue+ "}";
            await Utils.SendPostRequest(url, requestBody);  // Send a POST request

            // Pause for 5 seconds
            Thread.Sleep(5000);
        }

    }

    public static async Task IntegerValue()
    {
        Console.WriteLine("IntegerValue funtzioa aukeratuta");

        // TODO EZABATU (INGURUNE-ALDAGAI BEZALA HARTU BEHAR DIRA)
        string customization = @"{""type"": ""decreasingValue"", ""firstvalue"": 3}";

        // Lehenengo aldian hasierako zenbakia bidaliko da
        (string type, int firstValue) = Utils.getCustomizationValues(customization);
        string requestBody = @"{""type"": ""integer"",""value"": " +firstValue+ "}";
        await Utils.SendPostRequest(url, requestBody);  // Send a POST request
        Console.WriteLine(requestBody);
        Thread.Sleep(5000); // Pause for 5 seconds

        int createdValue = firstValue;
        while (true)
        {
            createdValue = Utils.getIntegerValue(customization, createdValue);
            Console.WriteLine("Created value: " + createdValue);

            // Sortutako zenbakia bidaltzen dugu
            requestBody = @"{""type"": ""integer"",""value"": " +createdValue+ "}";
            await Utils.SendPostRequest(url, requestBody);  // Send a POST request

            // Pause for 5 seconds
            Thread.Sleep(5000);
        }
    }

    public static async Task FloatValue()
    {
        Console.WriteLine("FloatValue funtzioa aukeratuta");

        // TODO EZABATU (INGURUNE-ALDAGAI BEZALA HARTU BEHAR DIRA)
        string customization = @"{""type"": ""random"", ""firstvalue"": 2.5}";

        // Lehenengo aldian hasierako zenbakia bidaliko da
        (string type, float firstValue) = Utils.getCustomizationValuesF(customization);
        string valueString = firstValue.ToString().Replace(',', '.');   // C# lengoaian float-ak komarekin erabiltzen dira
        string requestBody = @"{""type"": ""float"",""value"": " +valueString+ "}";
        await Utils.SendPostRequest(url, requestBody);  // Send a POST request
        Console.WriteLine(requestBody);
        Thread.Sleep(5000); // Pause for 5 seconds

        float createdValue = firstValue;
        while (true)
        {
            createdValue = Utils.getFloatValue(customization, createdValue);
            Console.WriteLine("Created value: " + createdValue);

            // Sortutako zenbakia bidaltzen dugu
            valueString = createdValue.ToString("0.00").Replace(',', '.');
            requestBody = @"{""type"": ""float"",""value"": " +valueString+ "}";
            await Utils.SendPostRequest(url, requestBody);  // Send a POST request

            // Pause for 5 seconds
            Thread.Sleep(5000);
        }
    }
}