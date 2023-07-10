// C++ program to display
// Prime numbers till N
#include <bits/stdc++.h>
#include <iomanip>
#include <iostream>
#include <sstream>
using namespace std;

// Function to check if a
// given number is prime
bool isPrime(int n)
{
      // Since 0 and 1 is not
      // prime return false.
      if(n == 1 || n == 0) return false;

      // Run a loop from 2 to n-1
      for(int i = 2; i < n; i++)
      {
        // if the number is divisible by i,
        // then n is not a prime number.
        if(n % i == 0) return false;
      }
      // Otherwise n is a prime number.
      return true;
}

// Main program accepts one argument.
// The  program generate primes up to this number
int main(int argc, char *argv[]){
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " [generate primes up to this number]" << endl;
        return 1;
    }

    int N = atoi(argv[1]);
    if (N < 0) {
        cout << "Invalid number of decimal places: " << N << endl;
        return 1;
    }

    ostringstream result;
    ofstream file("prime_numbers.out");
    if (!file.is_open()) {
        cout << "Failed to open output file" << endl;
        return 1;
    }
    // Check for every number from 1 to N
    for(int i = 1; i <= N; i++)
    {
        // Check if current number is prime
        if(isPrime(i))
        {
          result << i << ", ";
        }
    }
    cout << result.str() << endl;
    file << result.str() << endl;
    file.close();

    return 0;
}
