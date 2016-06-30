#include <iostream>
#include <vector>
#include <algorithm>
#include <map>

class UniqueNumbers {
private:
	struct node {
		node* left;
		node* right;
		int count;

		node() {}
		node(int value)
			: left(NULL)
			, right(NULL)
			, count(value == -1 ? 1 : 0)
		{ }
		node(node* left_node, node* right_node)
			: left(left_node)
			, right(right_node)
			, count(0) {
			if(left_node) count += left_node->count;
			if(right_node) count += right_node->count;
		}
	};
	int root;
	int sequence_length;
	int number_of_queries;
	std::vector<int> sequence;
	std::vector<int> query_results;
	std::vector<int> position_of_next_same;
	std::vector<node*> roots;

	node* build(int left, int right) {
		if(left == right) {
			return new node(position_of_next_same[left]);
		}
		return new node(
			build(left, (left + right) >> 1),
			build(((left + right) >> 1) + 1, right)
		);
	}
	int count_unique_elements(node* vertex, int left, int right, int query_left, int query_right) {
		if(query_left > query_right) {
			return 0;
		}
		if(query_left == left && query_right == right) {
			return vertex->count;
		}
		return count_unique_elements(vertex->left, left, (left + right) >> 1, query_left, std::min(query_right, (left + right) >> 1))
			 + count_unique_elements(vertex->right, ((left + right) >> 1) + 1, right, std::max(query_left, ((left + right) >> 1) + 1), query_right);
	}
	node* change(node* vertex, int left, int right, int position, int value) {
		if(left == right) {
			return new node(value);
		}
		if(position <= (left + right) >> 1) {
			return new node(
				change(vertex->left, left, (left + right) >> 1, position, value),
				vertex->right
				);
		}
		else {
			return new node(
				vertex->left,
				change(vertex->right, ((left + right) >> 1) + 1, right, position, value)
				);
		}
	}

public:
	void solve_online(std::istream& in) {
		int root_counter = 1;
		in >> sequence_length >> number_of_queries;
		roots.resize(sequence_length + 1);
		sequence.resize(sequence_length);
		query_results.resize(number_of_queries);
		position_of_next_same.resize(sequence_length, -1);
		std::map<int, int> visited_elements;
		std::map<int, int>::iterator finder;
		
		roots[0] = build(0, sequence_length - 1);
		for(size_t bound = 0; bound < sequence_length; ++bound) {
			roots[root_counter] = roots[root_counter - 1];
			in >> sequence[bound];
			finder = visited_elements.find(sequence[bound]);
			if(finder != visited_elements.end()) {
				roots[root_counter] = change(roots[root_counter], 0, sequence_length - 1, (*finder).second, bound);
			}
			visited_elements[sequence[bound]] = bound;
			++root_counter;
		}

		int left_bound, right_bound;
		for(size_t query = 0; query < number_of_queries; ++query) {
			std::cin >> left_bound >> right_bound;
			query_results[query] = count_unique_elements(roots[right_bound], 0, sequence_length - 1, left_bound - 1, right_bound - 1);
		}
	}
	void writeData(std::ostream& out) {
		for(size_t query = 0; query < number_of_queries; ++query) {
			out << query_results[query] << "\n";
		}
	}
};

int main() {
	UniqueNumbers task;
	task.solve_online(std::cin);
	task.writeData(std::cout);
	std::cout << std::endl;
	return 0;
}
