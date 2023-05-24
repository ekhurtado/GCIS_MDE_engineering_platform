using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public static class HttpHelper
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
}
