using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;
using System.Globalization;

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

    public static (string, int) getCustomizationValues(string customization)
    {
        JsonElement root = JsonDocument.Parse(customization).RootElement;
        string type = root.GetProperty("type").GetString();
        int firstValue = root.GetProperty("firstvalue").GetInt32();
        return (type,firstValue);
    }

    public static (string, float) getCustomizationValuesF(string customization)
    {

        JsonElement root = JsonDocument.Parse(customization).RootElement;
        string type = root.GetProperty("type").GetString();
        float firstValue = root.GetProperty("firstvalue").GetSingle();
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
                return random.Next(1, 1001);    // ausazko zenbakia 1 eta 1000 artean
            case "increasingValue":
                if (previousValue < 1) { previousValue = 1; }
                return firstValue + 1;
            case "decreasingValue":
                int createdValue = previousValue - 1;
                if (createdValue < 1) { createdValue = 1; }
                return createdValue;
            default:
                Console.WriteLine("Invalid customization name.");
                return -1;
        }
    }

    public static int getIntegerValue(string customization, int previousValue)
    {
        (string type, int firstValue) = getCustomizationValues(customization);
        Console.WriteLine(type);
        Console.WriteLine(firstValue);

        switch (type)
        {
            case "random":
                Random random = new Random();
                return random.Next(-1000, 1001);    // ausazko zenbakia -1000 eta 1000 artean
            case "increasingValue":
                return firstValue + 1;
            case "decreasingValue":
                return previousValue - 1;
            default:
                Console.WriteLine("Invalid customization name.");
                return -1;
        }
    }

    public static float getFloatValue(string customization, float previousValue)
    {
        (string type, float firstValue) = getCustomizationValuesF(customization);
        Console.WriteLine(type);
        Console.WriteLine(firstValue);

        switch (type)
        {
            case "random":
                Random random = new Random();
                float minValue = -1000.0f;
                float maxValue = 1000.0f;
                return (float)(random.NextDouble() * (maxValue - minValue) + minValue);    // ausazko zenbakia -1000.0 eta 1000.0 artean
            case "increasingValue":
                return firstValue + 1.0f;
            case "decreasingValue":
                return previousValue - 1.0f;
            default:
                Console.WriteLine("Invalid customization name.");
                return -1.0f;
        }
    }

}
