/* 
 * Calculate the SSK Kernel between 2 strings s and t;
 * 
 *
 * 	Usage 1: programname n filename1 filename2 [lambda]
 *
 * 		n: kernel parameter, number of letters to consider
 *
 * 		filename1,filename2: paths to files that contain s and t
 *
 * 		lambda: exponental falloff parameter
 *
 *
 *	Usage 2: programname n [lambda]
 *
 * 		n: kernel parameter, number of letters to consider
 *
 * 		lambda: exponental falloff parameter
 *		
 *  	send strings into standard input the following way:
 *
 *			size_of_string_1\n
 *			string_1\n
 *			size_of_string_2\n
 *			string_2\n
 *			
 *
 *
 * 	FIXME: Seems to work for all n except n=1
 */

#include <algorithm>
#include <map>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <tuple>
#include <cassert>
#include <iostream>

const double DEFAULT_LAMBDA = 0.5; // parameter lambda; amount of exponental falloff due to string length

// generic power function using repeated squaring
template<typename T>
T pow (T b, T e) {
	T r = 1;
	while (e){
		if (e&1)
			r *= b;
		e >>= 1;
		b *= b;
	}
	return r;
}



void readFromFile(int argc, char const *argv[],int& sl, int& tl, char*& s, char*& t, int& n, double& lambda) {
	
	// parameter n of the Kernel
	n = atoi(argv[1]);
	assert(n >= 1);

	// Open files
	FILE* sf = fopen(argv[2],"r");
	FILE* tf = fopen(argv[3],"r");

	// get length of files
	fseek(sf, 0L, SEEK_END);
	fseek(tf, 0L, SEEK_END);
	sl = ftell(sf);
	tl = ftell(tf);
	fseek(sf, 0L, SEEK_SET);
	fseek(tf, 0L, SEEK_SET);

	// allocate memory
	s = new char[sl + 1];
	t = new char[tl + 1];

	// read files into RAM
	int num_read = fread((void*) s, sizeof(char), sl, sf);
	assert(num_read == sl);
	num_read = fread((void*) t, sizeof(char), tl, tf);
	assert(num_read == tl);

	// add null termination to strings
	s[sl] = '\0';
	t[tl] = '\0';

	// get optional lambda
	if (argc > 4)
		lambda = atof(argv[argc-1]);
	assert(lambda > 0 && lambda < 1);

	// close files
	fclose(sf);
	fclose(tf);
}

void readFromStdin(int argc, char const* argv[], int& sl, int& tl, char*& s, char*& t, int& n, double& lambda) {
	// parameter n of the Kernel
	n = atoi(argv[1]);
	assert(n >= 1);

	// get optional lambda
	if (argc > 2)
		lambda = atof(argv[2]);
	assert(lambda > 0 && lambda < 1);

	// get s and t from input
	int gotten;
	gotten = scanf("%i",&sl); // read string length
	assert(gotten > 0);
	getchar(); // throw endline
	s = new char[sl + 1]; // allocate
	char* r = fgets(s, sl + 1 , stdin); // read string
	assert(r == s);

	gotten = scanf("%i",&tl); // read string length
	assert(gotten > 0);
	getchar(); // throw endline
	t = new char[tl + 1]; // allocate
	r = fgets(t, tl + 1, stdin); // read string
	assert(r == t);

}

// memoization.
const int MAX_STRING_SIZE = 9000;
const int MAX_K = 15;

void print( double (*m) [MAX_STRING_SIZE], int n, int SL) {
	for (int i = n-1; i >= 0; --i) {
		for (int sl = 0; sl <= SL; ++sl)
			std::cerr << m[i][sl] << ' ';
		std::cerr << '\n';
	}
	std::cerr << '\n';
}

double getK(const int n, const int SL, const int TL, const char* s, const char* t, double lambda) {
	static double mem[4][MAX_K][MAX_STRING_SIZE];
	typedef double (*Mem) [MAX_STRING_SIZE];
	Mem KPmemPrev = mem[0];
	Mem KPmemNext = mem[1];
	Mem KPPmemPrev = mem[2];
	Mem KPPmemNext = mem[3];

	// init KP
	for (int sl = 0; sl <= SL; ++sl)
		KPmemPrev[0][sl] = 1;

	for (int i = 1; i <= n; ++i)
	for (int sl = 0; sl <= SL; ++sl)
		KPmemPrev[i][sl] = KPPmemPrev[i][sl] = 0;

	double kpsum = 0.0;

	for (int tl = 1; tl < TL; ++tl){


		// std::cerr << tl << '\n';
		// print(KPmemPrev, n, SL);

		// edge cases
		//TODO: remove

		// print(KPmemNext, n, SL);

		// if i == 0 put to 1
		for (int sl = 0; sl <= SL; ++sl)
			KPmemNext[0][sl] = 1;

		// print(KPmemNext, n, SL);

		// if min(sl,tl) < i put to 0
		for (int i = 1; i <= tl && i <= n; ++i)
		for (int sl = 0; sl < i; ++sl)
			KPmemNext[i][sl] = KPPmemNext[i][sl] = 0;

		// print(KPmemNext, n, SL);

		// if (min(sl,tl) < i) put to 0
		for (int i = tl+1; i <= n; ++i)
		for (int sl = 0; sl <= SL; ++sl)
			KPmemNext[i][sl] = KPPmemNext[i][sl] = 0;

		// print(KPmemNext, n, SL);

		// now do recursion
		for (int i = 1; i <= tl && i <= n; ++i)
		for (int sl = i; sl <= SL; ++sl) 
		{
			{
				char x = s[sl-1];
				if (t[tl-1] != x)
					KPPmemNext[i][sl] = lambda * KPPmemPrev[i][sl];
				else
					KPPmemNext[i][sl] = lambda * ( KPPmemPrev[i][sl] + lambda*KPmemPrev[i-1][sl-1] );
			}

			{
				KPmemNext[i][sl] = lambda*KPmemNext[i][sl-1] + KPPmemNext[i][sl];
			}

		}

		// print(KPmemNext, n, SL);

		// calculate K from values of k'
		for (int sl = SL; sl >= n; --sl) {
			const char x = s[sl-1];
			if (t[tl] == x) {
				kpsum += KPmemNext[n-1][sl-1]; // kp(i-1, sl-1, j);
				// std::cerr << "+\n";
				// std::cerr << x << ' ' << t[tl] << ' ' << sl << ' ' << tl << ' ' << KPmemNext[n-1][sl-1] << '\n';
			}
		}
		// std::cerr << kpsum << std::endl;

		// switch buffers for next iteration
		std::swap(KPmemPrev, KPmemNext);
		std::swap(KPPmemPrev, KPPmemNext);

	}
	
	// std::cerr << TL << '\n';
	// print(KPmemPrev, n, SL);

	// std::cerr << kpsum << std::endl;

	double K = lambda*lambda*kpsum; // k(i, sl-1, tl) + kpsum*lambda*lambda;

	return K;

}

int main(int argc, char const *argv[])
{

	if (argc == 1) {
		printf("Usage:%s n filename1 filename2 [lambda]\nn: kernel parameter, number of letters to consider\nfilename1,filename2: paths to files to calculate the kernel for\nlambda: exponental falloff parameter, default value is %lf\n\nOr:\nn lambda\nsend strings through standard input as:\nsize_of_string_1\nstring_1\nsize_of_string_2\nstring_2\n",argv[0], DEFAULT_LAMBDA);
		exit(1);
	}

	// read input

	int SL,TL;
	char *s, *t;
	int n;
	double lambda = DEFAULT_LAMBDA;
	if (argc > 3) {

		readFromFile(argc,argv,SL,TL,s,t,n,lambda);

		for (int i = 0; i <= argc-5; ++i) {

			if (SL >= MAX_STRING_SIZE || TL >= MAX_STRING_SIZE){
				std::cerr << "Only supports strings of size up to " << MAX_STRING_SIZE << "!\n";
				exit(EXIT_FAILURE);
			}

			double K = getK(n, SL, TL, s, t, lambda);
			double Ks = getK(n, SL, SL, s, s, lambda);
			double Kt = getK(n, TL, TL, t, t, lambda);

			K = K / sqrt( Ks*Kt );

			std::cout.precision(std::numeric_limits<double>::digits10);
			std::cout << std::fixed <<  K << std::endl;
			// printf("%lf %lf %lf\n", K, Ks, Kt);

			delete [] t;

			if (i != argc-5){
				// Open files
				FILE* tf = fopen(argv[4+i],"r");

				// get length of files
				fseek(tf, 0L, SEEK_END);
				TL = ftell(tf);
				fseek(tf, 0L, SEEK_SET);

				// allocate memory
				t = new char[TL + 1];

				// read files into RAM
				int num_read = fread((void*) t, sizeof(char), TL, tf);
				assert(num_read == TL);

				// add null termination to strings
				t[TL] = '\0';

				// close file
				fclose(tf);
			}

		}

		delete [] s;

	}



	else if (argc <= 3){
		readFromStdin(argc,argv,SL,TL,s,t,n,lambda);

		if (SL >= MAX_STRING_SIZE || TL >= MAX_STRING_SIZE){
			std::cerr << "Only supports strings of size up to " << MAX_STRING_SIZE << "!\n";
			exit(EXIT_FAILURE);
		}

		double K = getK(n, SL, TL, s, t, lambda);
		double Ks = getK(n, SL, SL, s, s, lambda);
		double Kt = getK(n, TL, TL, t, t, lambda);

		K = K / sqrt( Ks*Kt );

		std::cout.precision(std::numeric_limits<double>::digits10);
		std::cout << std::fixed <<  K << std::endl;
		// printf("%lf\n", K);

		delete [] t;
		delete [] s;
	}

}
		
