using System;
using System.Net.Http;
using HTTPMethods;

namespace NetCore.Docker
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");


            Random rnd = new Random();
            for (int j = 0; j < 5; j++)
            {
                Console.WriteLine(rnd.Next(0, 1000)); // 0 eta 1000 arteko zenbakiak sortzen ditugu
            }

            using var client = new HttpClient();

            HTTPMethods metodoak = new HTTPMethods();

            await metodoak.GetAsync();

        }
    }

}
