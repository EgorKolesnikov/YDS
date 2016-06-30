#include <iostream>
#include <string>
#include <vector>

#define max(a, b) ((a) > (b) ? (a) : (b))

class LongestSubpalindrome {
private:
	int word_length, subpalindrome_length;
	std::string word;
	std::string subpalindrome;
	std::vector< std::vector<int> > smaller_task;
	void countLengthOfSubpalindrome() {
		/*
		* Because of memory limit I had to inverse the matrix of states, and
		* allocate the memory for it like staircase. So in 'for' loop using
		* 'right < left' only for better understanding 'longest[left][right]'.
		* (actually here 'left' means right bound of string, and right - left bound)
		*/
		int left, right, tab, left_state, right_state;
		for(tab = 1; tab < word_length; ++tab) {
			for(right = 0, left = tab; left < word_length; ++left, ++right) {
				if(word[left] == word[right]) {
					if(right + 1 > left - 1)
						smaller_task[left][right] = 2;
					else
						smaller_task[left][right] = smaller_task[left - 1][right + 1] + 2;
				}
				else {
					left_state = smaller_task[left - 1][right];
					right_state = smaller_task[left][right + 1];
					smaller_task[left][right] = max(left_state, right_state);
				}
			}
		}
		subpalindrome_length = smaller_task[word_length - 1][0];
	}
	void buildSubpalindrome() {
		int palindrome_Left = 0, palindrome_Right = subpalindrome_length - 1;
		int left = word_length - 1, right = 0;
		subpalindrome.resize(subpalindrome_length);
		while(left >= right) {
			if(left == right && smaller_task[left][right] == 1) {
				subpalindrome[palindrome_Left++] = word[left++];
				break;
			}
			else {
				if(word[left] == word[right]) {
					subpalindrome[palindrome_Left++] = word[left--];
					subpalindrome[palindrome_Right--] = word[right++];
				}
				else {
					if(smaller_task[left][right + 1] > smaller_task[left - 1][right])
						++right;
					else
						--left;
				}
			}
		}
	}

public:
	LongestSubpalindrome() {}

	void solve() {
		countLengthOfSubpalindrome();
		buildSubpalindrome();
	}
	friend std::istream& operator>> (std::istream& in, LongestSubpalindrome& object) {
		in >> object.word;
		object.word_length = object.word.length();
		object.smaller_task = std::vector< std::vector<int> >(object.word_length);
		for(int i = 0; i < object.word_length; ++i) {
			object.smaller_task[i] = std::vector<int>(i + 1, 0);
			object.smaller_task[i][i] = 1;
		}
		return in;
	}
	friend std::ostream& operator<< (std::ostream& out, const LongestSubpalindrome& object) {
		out << object.subpalindrome;
		return out;
	}
};


int main() {
	LongestSubpalindrome task;
	std::cin >> task;
	task.solve();
	std::cout << task;
	return 0;
}