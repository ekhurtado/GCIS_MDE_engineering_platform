using System;

public class HelloHTTP
{
    public static async Task Main(string[] args)
    {
        Console.WriteLine("Hello, World!");

        string url = "http://localhost:5000"; // Replace with the desired URL

        // Send a GET request
        await HttpHelper.SendGetRequest(url);

        // Send a POST request
        string requestBody = "This is a simple string as the request body.";
        await HttpHelper.SendPostRequest(url, requestBody);

    }
}

//using System.Net.Http;
//using System.Text;
//
//// See https://aka.ms/new-console-template for more information
//Console.WriteLine("Hello, World!");
//
//Random random = new Random();
//for (int i = 0; i < 5; i++)
//{
//    int randomNumber = random.Next(1, 1001); // Generates a random number between 1 and 1000
//    Console.WriteLine($"Random Number {i + 1}: {randomNumber}");
//}
//
//string url = "http://localhost:5000"; // Replace with the desired URL
//
//// Send a GET request
//await HttpHelper.SendGetRequest(url);
//
//// Send a POST request
//string requestBody = "This is a simple string as the request body.";
//await HttpHelper.SendPostRequest(url, requestBody);

// ---------------------------------------------------------

//static async Task SendGetRequest()
//{
//    string url = "http://localhost:5000"; // Replace with the desired URL
//
//    using (HttpClient client = new HttpClient())
//    {
//        HttpResponseMessage response = await client.GetAsync(url);
//
//        if (response.IsSuccessStatusCode)
//        {
//            string responseContent = await response.Content.ReadAsStringAsync();
//            Console.WriteLine("GET request successful");
//            Console.WriteLine("Response Content: " + responseContent);
//        }
//        else
//        {
//            Console.WriteLine("GET request failed with status code: " + response.StatusCode);
//        }
//    }
//}
//
//static async Task SendPostRequest(string requestBody)
//{
//    string url = "http://localhost:5000"; // Replace with the desired URL
//
//    using (HttpClient client = new HttpClient())
//    {
//        string requestBody = "Ahora un simple string";
//        var content = new StringContent(requestBody, Encoding.UTF8, "text/plain");
//        HttpResponseMessage response = await client.PostAsync(url, content);
//
//        if (response.IsSuccessStatusCode)
//        {
//            string responseContent = await response.Content.ReadAsStringAsync();
//            Console.WriteLine("POST request successful");
//            Console.WriteLine("Response Content: " + responseContent);
//        }
//        else
//        {
//            Console.WriteLine("POST request failed with status code: " + response.StatusCode);
//        }
//    }
//}
