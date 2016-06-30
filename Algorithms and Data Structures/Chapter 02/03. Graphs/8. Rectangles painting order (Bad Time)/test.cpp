#include <iostream>
#include <fstream>
#include <vector>
#include <cstring>
#include <algorithm>
#include <ctime>
#include <random>

class Test {

private:
	int min_size, max_size;
	int size;
	std::vector<std::vector<int>> generated;
	bool test_verdict;

public:

	Test(int min_s, int max_s) 
		: min_size(min_s)
		, max_size(max_s)
	{
		srand(time(NULL));
	}

	int get_random(int from, int to){
		return from + (rand() % (int)(to - from + 1));
	}

	void generate(std::string&& output) {
		size = get_random(min_size, max_size);
		generated.resize(size, std::vector<int>(size, 0));

		int min = 0;
		int max = size - 1;
		for(int color = 1; color <= size; ++color){
			int left = get_random(min, max);
			int top = get_random(min, max);
			int right = get_random(left, max);
			int bottom = get_random(top, max);

			for(int i = top; i <= bottom; ++i){
				for(int j = left; j <= right; ++j){
					generated[i][j] = color;
				}
			}
		}

		std::ofstream out(output);
		out << size << "\n";
		for(int i = 0; i < size; ++i){
			for(int j = 0; j < size; ++j){
				out << generated[i][j] << "\t";
			}
			out << "\n";
		}
		out.close();
	}

	void test(std::string&& standard, std::string&& for_test) {
		std::ifstream good(standard);
		std::ifstream test(for_test);

		int good_size, test_size;
		int from_good, from_test;
		good >> good_size;
		test >> test_size;

		if(good_size == test_size){
			generated.resize(good_size, std::vector<int>(good_size, 0));
			int color, left, right, top, bottom;
			for(int counter = 1; counter <= good_size; ++counter){
				test >> color >> top >> left >> bottom >> right;

				for(int i = top - 1; i < bottom; ++i){
					for(int j = left - 1; j < right; ++j){
						generated[i][j] = color;
					}
				}
			}

			std::ofstream OUT("test.rebuild.txt");
			OUT << good_size << "\n";
			for(int i = 0; i < good_size; ++i){
				for(int j = 0; j < good_size; ++j){
					OUT << generated[i][j] << "\t";
				}
				OUT << "\n";
			}

			for(int i = 0; i < good_size; ++i){
				for(int j = 0; j < good_size; ++j){
					good >> from_good;
					from_test = generated[i][j];

					if(from_good != from_test){
						test_verdict = false;
						std::cout << i << j;
						std::cout << "Bad.\n";
						return;
					}
				}
			}
		}

		std::cout << "Good.\n";
	}
};

int main(int argc, char *argv[]){
	Test tester(15, 20);

	if(strcmp(argv[1], "compare") == 0){
		tester.test(std::string(argv[2]), std::string(argv[3]));
	}
	else {
		tester.generate(std::string(argv[2]));
	}

	std::cout << std::endl;
	return 0;
}