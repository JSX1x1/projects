using System;
using System.Linq;
using System.Text;
using System.Threading;

class Program
{
    static void Main()
    {
        Console.WriteLine("🔐 Brute Force Emulator - Educational Use Only");
        Console.Write("Enter a password to simulate brute force attack: ");
        string targetPassword = Console.ReadLine();

        string charSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        int maxLength = targetPassword.Length; // Only brute force up to the correct length

        Console.WriteLine("\nStarting brute force simulation...\n");
        string crackedPassword = BruteForceAttack(targetPassword, charSet, maxLength);

        if (crackedPassword != null)
        {
            Console.WriteLine($"\n✅ Password found: {crackedPassword}");
        }
        else
        {
            Console.WriteLine("\n❌ Failed to crack the password.");
        }
    }

    static string BruteForceAttack(string target, string charSet, int maxLength)
    {
        foreach (int length in Enumerable.Range(1, maxLength))
        {
            foreach (var guess in GenerateCombinations(charSet, length))
            {
                Console.Write($"\rTrying: {guess}  "); // Update console with current guess
                Thread.Sleep(10); // Simulate realistic processing delay

                if (guess == target)
                {
                    return guess; // Password matched!
                }
            }
        }
        return null;
    }

    static IEnumerable<string> GenerateCombinations(string charSet, int length)
    {
        if (length == 1)
        {
            foreach (char c in charSet)
                yield return c.ToString();
        }
        else
        {
            foreach (var prefix in GenerateCombinations(charSet, length - 1))
            {
                foreach (char c in charSet)
                    yield return prefix + c;
            }
        }
    }
}
