#include <iostream>
#include <vector>
#include <algorithm>

class LongestAlternatingSubsequence {
private:
	enum Direction { Down = 0, Up = 1 };

	size_t sequence_length;
	size_t solution_length;
	std::vector<int> sequence;
	std::vector<int> solution;
	std::vector<std::vector<int>> local_answer;
	std::vector<std::vector<int>> next_index_in_solution;

	void computeDP() {
		for(int bound = static_cast<int>(sequence_length) -1; bound >= 0; --bound) {
			int here;
			for(here = bound + 1; here < sequence_length; ++here) {
				if(sequence[bound] > sequence[here]) {
					if(local_answer[Direction::Down][bound] <= local_answer[Direction::Up][here]) {
						local_answer[Direction::Down][bound] = 1 + local_answer[Direction::Up][here];
						next_index_in_solution[Direction::Down][bound] = here;
					}
				}
			}
			for(here = bound + 1; here < sequence_length; ++here) {
				if(sequence[bound] < sequence[here]) {
					if(local_answer[Direction::Up][bound] <= local_answer[Direction::Down][here]) {
						local_answer[Direction::Up][bound] = 1 + local_answer[Direction::Down][here];
						next_index_in_solution[Direction::Up][bound] = here;
					}
				}
			}
		}
	}
	void build_solution() {
		int here, answer = -1, where_answer_reached;
		where_answer_reached = std::distance(begin(local_answer[Direction::Up]), std::max_element(local_answer[Direction::Up].begin(), local_answer[Direction::Up].end()));
		answer = local_answer[Direction::Up][where_answer_reached];

		Direction direction = Direction::Up;
		solution_length = answer + 1;
		solution.resize(solution_length);
		here = -1;
		while(where_answer_reached != -1) {
			solution[++here] = where_answer_reached + 1;
			where_answer_reached = next_index_in_solution[direction][where_answer_reached];
			direction = (direction == Direction::Down ? Direction::Up : Direction::Down);
		}
	}

public:
	LongestAlternatingSubsequence() {}

	void solve() {
		computeDP();
		build_solution();
	}
	void readData(std::istream& in) {
		in >> sequence_length;
		sequence.resize(sequence_length);
		for(size_t i = 0; i < sequence_length; ++i) {
			in >> sequence[i];
		}
		local_answer.resize(2, std::vector<int>(sequence_length));
		next_index_in_solution.resize(2, std::vector<int>(sequence_length, -1));
	}
	void writeData(std::ostream& out) const {
		out << solution.size() << "\n";
		for(size_t i = 0; i < solution.size(); ++i) {
			out << solution[i] << " ";
		}
	}
};

int main() {
	LongestAlternatingSubsequence task;
	task.readData(std::cin);
	task.solve();
	task.writeData(std::cout);
	return 0;
}
