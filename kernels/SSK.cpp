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

char *s, *t; // documents/strings s and t
double lambda = 0.5; // parameter lambda; amount of exponental falloff due to string length
int n;

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



void readFromFile(int argc, char const *argv[],int& sl, int& tl) {
	
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
		lambda = atof(argv[4]);
	assert(lambda > 0 && lambda < 1);
}

void readFromStdin(int argc, char const* argv[], int& sl, int& tl) {
	// parameter n of the Kernel
	n = atoi(argv[1]);
	assert(n >= 1);

	// get optional lambda
	if (argc == 2)
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
const int MAX_STRING_SIZE = 2000;
double mem[6][MAX_STRING_SIZE][MAX_STRING_SIZE];
typedef double (*Mem) [MAX_STRING_SIZE];
Mem KPmemPrev = mem[0];
Mem KPmemNext = mem[1];
Mem KmemPrev = mem[2];
Mem KmemNext = mem[3];
Mem KPPmemPrev = mem[4];
Mem KPPmemNext = mem[5];

const double NOTSET = -1;

void resetMem() {
	for (int j = 0; j < MAX_STRING_SIZE; ++j)
	for (int k = 0; k < MAX_STRING_SIZE; ++k){
		KPPmemPrev[j][k] = NOTSET;
		KPmemPrev[j][k] = NOTSET;
		KmemPrev[j][k] = NOTSET;
	}
}

void switchMem() {

	// std::cerr << (void*) KmemPrev << ' ' << (void*) KmemNext << ' ' << (void*) KPmemPrev << ' ' << (void*) KPmemNext << ' ' << (void*) KPPmemPrev << ' ' << (void*) KPPmemNext << std::endl;

	std::swap(KmemPrev, KmemNext);
	std::swap(KPmemPrev, KPmemNext);
	std::swap(KPPmemPrev, KPPmemNext);

	// std::cerr << (void*) KmemPrev << ' ' << (void*) KmemNext << ' ' << (void*) KPmemPrev << ' ' << (void*) KPmemNext << ' ' << (void*) KPPmemPrev << ' ' << (void*) KPPmemNext << std::endl;
}

int main(int argc, char const *argv[])
{

	if (argc == 1) {
		printf("Usage:%s n filename1 filename2 [lambda]\nn: kernel parameter, number of letters to consider\nfilename1,filename2: paths to files to calculate the kernel for\nlambda: exponental falloff parameter, default value is %lf\n\nOr:\nn lambda\nsend strings through standard input as:\nsize_of_string_1\nstring_1\nsize_of_string_2\nstring_2\n",argv[0], lambda);
		exit(1);
	}

	// read input

	int SL,TL;
	if (argc > 3)
		readFromFile(argc,argv,SL,TL);
	if (argc <= 3)
		readFromStdin(argc,argv,SL,TL);

	if (SL >= MAX_STRING_SIZE || TL >= MAX_STRING_SIZE){
		std::cerr << "Only supports strings of size up to " << MAX_STRING_SIZE << "!\n";
		exit(EXIT_FAILURE);
	}

	// init KP
	for (int i = 0; i < MAX_STRING_SIZE; ++i)
	for (int j = 0; j < MAX_STRING_SIZE; ++j)
		KPmemPrev[i][j] = 1;


	for (int i = 1; i <= n; ++i){

		// edge values
		for (int sl = 0; sl < SL; ++sl)
		for (int tl = 0; std::min(sl,tl) < i && tl < TL; ++tl)
			KmemNext[sl][tl] = KPmemNext[sl][tl] = KPPmemNext[sl][tl] = 0;

		for (int sl = i; sl < SL; ++sl)
		for (int tl = i; tl < TL; ++tl){

			// do K
			{
				double kpsum;
				char x = s[sl-1];
				for (int j = 0; j < tl; ++j) {
					if (t[j] != x) continue;
					kpsum += KPmemPrev[sl-1][j];// kp(i-1, sl-1, j);
				}
				KmemNext[sl][tl] = KmemNext[sl-1][tl] + kpsum*lambda*lambda; // k(i, sl-1, tl) + kpsum*lambda*lambda;
			}

			// now KPP
			{
				// kpp (sx, tu) = lambda^|u| * kpp (sx,t) if x does not occur in u.
				char x = s[sl-1];
				if (t[tl-1] != x)
					KPPmemNext[sl][tl] = lambda * KPPmemPrev[sl][tl-1];
				else
					KPPmemNext[sl][tl] = lambda * ( KPPmemNext[sl][tl-1] + lambda*KPmemPrev[sl-1][tl-1] );
				// double val = c * lambda * ( kpp(i,sl,tl-1) + lambda*kp(i-1,sl-1,tl-1) );
			}

			// and at last KP
			{
				KPPmemNext[sl][tl] = lambda*KPmemNext[sl-1][tl] + KPPmemNext[sl][tl];
				// double val = lambda*kp(i, sl-1, tl) + kpp(i, sl, tl);
			}


		}

		printf("K\n");
		for (int sl = 0; sl < SL; ++sl){
			for (int tl = 0; tl < TL; ++tl)
				printf("%.1lf ", KmemNext[sl][tl]);
			putchar('\n');
		}
		printf("KPP\n");
		for (int sl = 0; sl < SL; ++sl){
			for (int tl = 0; tl < TL; ++tl)
				printf("%.1lf ", KPPmemNext[sl][tl]);
			putchar('\n');
		}
		printf("KP\n");
		for (int sl = 0; sl < SL; ++sl){
			for (int tl = 0; tl < TL; ++tl)
				printf("%.1lf ", KPmemNext[sl][tl]);
			putchar('\n');
		}
		
		// switch buffers for next iteration
		switchMem();

	}


	// KmemPrev[SL-1][TL-1] should contain our sought after value
	printf("%lf\n", KmemPrev[SL-1][TL-1]);

	}
		
