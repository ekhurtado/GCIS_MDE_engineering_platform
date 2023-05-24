using System.Net.Http;
using System.Text;

// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");

Random random = new Random();
for (int i = 0; i < 5; i++)
{
    int randomNumber = random.Next(1, 1001); // Generates a random number between 1 and 1000
    Console.WriteLine($"Random Number {i + 1}: {randomNumber}");
}

// Send a GET request
using (HttpClient client = new HttpClient())
{
string url = "http://localhost:5000"; // Replace with the desired URL
HttpResponseMessage response = await client.GetAsync(url);

if (response.IsSuccessStatusCode)
{
    string responseContent = await response.Content.ReadAsStringAsync();
    Console.WriteLine("GET request successful");
    Console.WriteLine("Response Content: " + responseContent);
}
else
{
    Console.WriteLine("GET request failed with status code: " + response.StatusCode);
}
}

// Send a POST request with data
using (HttpClient client = new HttpClient())
{
    string url = "http://localhost:5000"; // Replace with the desired URL

    var postData = new Dictionary<string, string>
    {
        { "param1", "25" },
        { "param2", "67" }
    };

    var content = new FormUrlEncodedContent(postData);
    HttpResponseMessage response = await client.PostAsync(url, content);

    if (response.IsSuccessStatusCode)
    {
        string responseContent = await response.Content.ReadAsStringAsync();
        Console.WriteLine("POST request successful");
        Console.WriteLine("Response Content: " + responseContent);
    }
    else
    {
        Console.WriteLine("POST request failed with status code: " + response.StatusCode);
    }
}

using (HttpClient client = new HttpClient())
{
    string requestBody = "Ahora un simple string";
    Console.WriteLine(requestBody);
    string url = "http://localhost:5000"; // Replace with the desired URL

    var content = new StringContent(requestBody, Encoding.UTF8, "text/plain");

    // Send the POST request
    HttpResponseMessage response = await client.PostAsync(url, content);

    if (response.IsSuccessStatusCode)
    {
        string responseContent = await response.Content.ReadAsStringAsync();
        Console.WriteLine("POST request successful");
        Console.WriteLine("Response Content: " + responseContent);
    }
    else
    {
        Console.WriteLine("POST request failed with status code: " + response.StatusCode);
    }
}