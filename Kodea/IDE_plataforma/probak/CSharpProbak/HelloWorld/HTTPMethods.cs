class HTTPMethods
{
    static async Task GetAsync(HttpClient httpClient)
    {
        var content = await client.GetStringAsync("http://localhost:8500");

        Console.WriteLine(content);
    }
}