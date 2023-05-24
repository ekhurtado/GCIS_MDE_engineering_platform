using System;

public class ZenbakienSorkuntza
{

//    string function = Environment.GetEnvironmentVariable("SERVICE");
//    string customization = Environment.GetEnvironmentVariable("CUSTOMIZATION");
    static string url = "http://localhost:5000"; // Replace with the desired URL

    public static async Task Main(string[] args)
    {
        Console.WriteLine("Kaixo! Ongi etorri ZenbakienSorkuntza aplikaziora");

        // Send a GET request
        await Utils.SendGetRequest(url);

        // Send a POST request
        string requestBody = "This is a simple string as the request body.";
        await Utils.SendPostRequest(url, requestBody);

        // TODO EZABATU (INGURUNE-ALDAGAI BEZALA HARTU BEHAR DIRA)
        string function = "NaturalValue";

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
    }

    public static async Task FloatValue()
    {
        Console.WriteLine("FloatValue funtzioa aukeratuta");
    }
}