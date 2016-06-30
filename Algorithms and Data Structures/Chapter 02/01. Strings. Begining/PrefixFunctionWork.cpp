#include <iostream>
#include <vector>
#include <cstring>
#include <string>
#include <algorithm>


class PrefixFunctionWork {

private:
	int length = 0;
	std::vector<int> pi;
	std::vector<int> result;

	bool isCorrect() {
		for (int i = 0; i < pi.size(); ++i) {
			if (pi[i] < 0 || (i > 0 && pi[i] > pi[i - 1] + 1)) {
				return false;
			}
		}
		return pi[0] == 0;
	}

	std::vector<int> calculate_z(std::vector<int>& str) {
		int length = str.size();
		std::vector<int> z(length);

		for (int index = 1, left = 0, right = 0; index < length; ++index) {
			if (index < right) {
				z[index] = std::min(z[index - left], right - index + 1);
			}

			while (index + z[index] < length && str[index + z[index]] == str[z[index]]) {
				++z[index];
			}
			if (index + z[index] - 1 > right) {
				right = index + z[index] - 1;
				left = index;
			}
		}

		return z;
	}

	std::vector<int> calculate_pi(std::vector<int>& str) {
		int length = str.size();
		std::vector<int> new_pi(length);

		for (int index = 1; index < length; ++index) {
			int equal_length = new_pi[index - 1];
			while (equal_length > 0 && str[equal_length] != str[index]) {
				equal_length = new_pi[equal_length - 1];
			}

			if (str[index] == str[equal_length]) {
				++equal_length;
			}
			new_pi[index] = equal_length;
		}

		return new_pi;
	}

	bool check(std::vector<int>& str, std::vector<int>& input) {
		int length = input.size();
		std::vector<int> new_pi = calculate_pi(str);

		for (int i = 0; i < length; ++i) {
			if (input[i] != new_pi[i]) {
				return false;
			}
		}
		return true;
	}

public:
	PrefixFunctionWork() {}

	void string_from_pi() {
		if (isCorrect()) {
			int now = 0;
			result.resize(length);
			pi.push_back(pi[pi.size() - 1] + 1);
			for (int i = 0; i < length; ++i) {
				if (pi[i] == 0) {
					result[i] = now++;
				} else {
					result[i] = result[pi[i] - 1];
				}
			}
			pi.pop_back();
		} else {
			result = std::vector<int> { -1 };
		}

		if (!check(result, pi)) {
			result = std::vector<int> { -1 };
		}
	}

	void z_from_pi() {
		int now = 0;
		result.resize(length);
		pi.push_back(pi[pi.size() - 1] + 1);
		for (int i = 0; i < length; ++i) {
			if (pi[i] == 0) {
				result[i] = now++;
			} else {
				result[i] = result[pi[i] - 1];
			}
		}
		pi.pop_back();
		result = calculate_z(result);
	}

	void readData(std::istream& in) {
		in >> length;
		pi.resize(length);
		for (int index = 0; index < length; ++index) {
			in >> pi[index];
		}
	}

	void writeData(std::ostream& out) {
		for (int index = 0; index < result.size(); ++index) {
			out << result[index] << " ";
		}
	}
};


int main() {
	PrefixFunctionWork test;
	test.readData(std::cin);
	test.z_from_pi();
	test.writeData(std::cout);

	std::cout << std::endl;
	return 0;
}