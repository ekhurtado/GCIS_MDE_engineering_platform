using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;

public static class Utils
{

    public static async Task SendGetRequest(string url)
    {
        using (HttpClient client = new HttpClient())
        {
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
    }

    public static async Task SendPostRequest(string url, string requestBody)
    {
        using (HttpClient client = new HttpClient())
        {
            var content = new StringContent(requestBody, Encoding.UTF8, "text/plain");
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
    }

    public static (string,int) getCustomizationValues(string customization)
    {
        JsonElement root = JsonDocument.Parse(customization).RootElement;
        string type = root.GetProperty("type").GetString();
        int firstValue = root.GetProperty("firstvalue").GetInt32();
        return (type,firstValue);
    }

    public static int getNaturalValue(string customization, int previousValue)
    {
        (string type, int firstValue) = getCustomizationValues(customization);
        Console.WriteLine(type);
        Console.WriteLine(firstValue);

        switch (type)
        {
            case "random":
                Random random = new Random();
                return random.Next(0, 1001);    // ausazko zenbakia 0 eta 1000 artean
            case "increasingValue":
                if (previousValue < 0) { previousValue = 0; }
                return firstValue + 1;
            case "decreasingValue":
                int createdValue = previousValue - 1;
                if (createdValue < 0) { createdValue = 0; }
                return createdValue;
            default:
                Console.WriteLine("Invalid customization name.");
                return -1;
        }
    }


}
