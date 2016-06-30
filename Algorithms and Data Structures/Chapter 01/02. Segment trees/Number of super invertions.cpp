#include <iostream>
#include <vector>
#include <algorithm>

class SuperInversions {
private:
	struct info {
		int to_the_left;
		int to_the_right;
		int value;
		info()
			: to_the_left(0)
			, to_the_right(0)
			, value(0) 
		{ }
	};
	int sequence_length;
	long long int result;
	std::vector<info> sequence;
	std::vector<int> tree;
	std::vector<int> mirror;

	void build(int vertex, int left, int right) {
		if(left == right) {
			tree[vertex] = 0;
		}
		else {
			build(vertex * 2, left, (left + right) >> 1);
			build(vertex * 2 + 1, ((left + right) >> 1) + 1, right);
			tree[vertex] = 0;
		}
	}
	void increase(int vertex, int left, int right, int position) {
		if(left == right) {
			tree[vertex] += 1;
		}
		else {
			if(position <= (left + right) >> 1) {
				increase(vertex * 2, left, (left + right) >> 1, position);
			}
			else {
				increase(vertex * 2 + 1, ((left + right) >> 1) + 1, right, position);
			}
			tree[vertex] = tree[vertex * 2] + tree[vertex * 2 + 1];
		}
	}
	int inversions(int vertex, int left, int right, int query_left, int query_right) {
		if(query_left > query_right || query_right < left || query_left > right) {
			return 0;
		}
		else {
			if(query_left == left && query_right == right) {
				return tree[vertex];
			}
			return inversions(vertex * 2, left, (left + right) >> 1, query_left, std::min((left + right) >> 1, query_right)) +
				   inversions(vertex * 2 + 1, ((left + right) >> 1) + 1, right, std::max(((left + right) >> 1) + 1, query_left), query_right);
		}
	}

public:
	SuperInversions() {
		result = 0;
	}

	void solve() {
		int position;
		build(1, 0, sequence_length - 1);
		for(position = sequence_length - 1; position >= 0; --position) {
			sequence[position].to_the_right = inversions(1, 0, sequence_length - 1, 0, mirror[position] - 1);
			increase(1, 0, sequence_length - 1, mirror[position]);
		}
		build(1, 0, sequence_length - 1);
		for(position = 0; position < sequence_length; ++position) {
			sequence[position].to_the_left = inversions(1, 0, sequence_length - 1, mirror[position] + 1, sequence_length - 1);
			increase(1, 0, sequence_length - 1, mirror[position]);
		}

		for(position = 0; position < sequence_length; ++position) {
			result += static_cast<long long int>(sequence[position].to_the_left) * sequence[position].to_the_right;
		}
	}
	void readData(std::istream& in) {
		int index;
		in >> sequence_length;
		sequence.resize(sequence_length);
		mirror.resize(sequence_length);
		tree.resize(sequence_length * 4);
		std::vector<int> sorted(sequence_length);

		for(index = 0; index < sequence_length; ++index) {
			in >> sequence[index].value;
			sorted[index] = sequence[index].value;
		}
		std::sort(begin(sorted), end(sorted));
		for(index = 0; index < sequence_length; ++index) {
			mirror[index] = std::lower_bound(begin(sorted), end(sorted), sequence[index].value) - begin(sorted);
		}
	}
	void writeData(std::ostream& out) {
		out << result;
	}
};

int main() {
	SuperInversions task;
	task.readData(std::cin);
	task.solve();
	task.writeData(std::cout);
	std::cout << std::endl;
	return 0;
}