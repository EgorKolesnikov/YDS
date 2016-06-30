#include <iostream>
#include <vector>
#include <algorithm>

class NumberOfSectionsFilledWithOnes {
private:
	struct node {
		int answer;
		short fill;
		bool attached_to_left_bound;
		bool attached_to_right_bound;
		node()
			: fill(0)
			, answer(0)
			, attached_to_left_bound(false)
			, attached_to_right_bound(false)                                                                                                                     {
 }
		node(int e)
			: fill(e)
			, answer(e == 1 ? 1 : 0)
			, attached_to_left_bound(e == 1 ? true : false)
			, attached_to_right_bound(e == 1 ? true : false) 
		{ }
	};
	int sequence_length;
	int number_of_queries;
	std::vector<int> input_sequence;
	std::vector<int> results;
	std::vector<node> tree;

	inline int RightSon(int& vertex) {
		return vertex << 1;
	}
	inline int LeftSon(int& vertex) {
		return (vertex << 1) + 1;
	}
	inline int Father(int& vertex) {
		return vertex >> 1;
	}

	void push(int vertex) {
		if(tree[vertex].fill != -1) {
			tree[LeftSon(vertex)] = tree[RightSon(vertex)] = tree[vertex];
		}
	}
	node combine(node& left, node& right) {
		node result;
		result.fill = (left.fill == right.fill) ? left.fill : -1;
		result.attached_to_left_bound = left.attached_to_left_bound;
		result.attached_to_right_bound = right.attached_to_right_bound;
		result.answer = left.answer + right.answer - (left.attached_to_right_bound && right.attached_to_left_bound ? 1 : 0);
		return result;
	}
	void build() {
		tree.resize(sequence_length * 4, node(0));
	}
	void update(int vertex, int vertex_left_bound, int vertex_right_bound, int update_left_bound, int update_right_bound, int value) {
		if(update_left_bound > update_right_bound) {
			return;
		}
		if(update_left_bound == vertex_left_bound && update_right_bound == vertex_right_bound) {
			tree[vertex] = node(value);
		}
		else {
			int vertex_middle = (vertex_left_bound + vertex_right_bound) / 2;
			push(vertex);
			update(LeftSon(vertex), vertex_left_bound, vertex_middle, update_left_bound, std::min(vertex_middle, update_right_bound), value);
			update(RightSon(vertex), vertex_middle + 1, vertex_right_bound, std::max(vertex_middle + 1, update_left_bound), update_right_bound, value);
			tree[vertex] = combine(tree[LeftSon(vertex)], tree[RightSon(vertex)]);
		}
	}
	node query(int vertex, int vertex_left_bound, int vertex_right_bound, int query_left_bound, int query_right_bound) {
		if(vertex != 1 && tree[Father(vertex)].fill != -1) {
			push(Father(vertex));
		}
		if(query_left_bound == vertex_left_bound && query_right_bound == vertex_right_bound) {
			return tree[vertex];
		}

		int vertex_middle = (vertex_left_bound + vertex_right_bound) / 2;
		if(query_right_bound <= vertex_middle) {
			return query(LeftSon(vertex), vertex_left_bound, vertex_middle, query_left_bound, query_right_bound);
		}
		if(query_left_bound > vertex_middle) {
			return query(RightSon(vertex), vertex_middle + 1, vertex_right_bound, query_left_bound, query_right_bound);
		}
		node left_result = query(LeftSon(vertex), vertex_left_bound, vertex_middle, query_left_bound, vertex_middle);
		node right_result = query(RightSon(vertex), vertex_middle + 1, vertex_right_bound, vertex_middle + 1, query_right_bound);
		return combine(left_result, right_result);
	}

public:
	NumberOfSectionsFilledWithOnes() {}

	void solve(std::istream &in) {
		build();
		int type, left, right;
		for(int next_query = 0; next_query < number_of_queries; ++next_query) {
			in >> type >> left >> right;
			switch(type) {
				case 0:
					update(1, 0, sequence_length - 1, left - 1, right - 1, 0);
					break;
				case 1:
					update(1, 0, sequence_length - 1, left - 1, right - 1, 1);
					break;
				case 2:
					results.push_back(query(1, 0, sequence_length - 1, left - 1, right - 1).answer);
					break;
			}
		}
	}
	void readData(std::istream &in) {
		in >> sequence_length;
		in >> number_of_queries;
		input_sequence.resize(sequence_length, 0);
	}
	void writeData(std::ostream &out) {
		for(size_t i = 0; i < results.size(); ++i) {
			out << results[i] << "\n";
		}
	}
};

int main() {
	NumberOfSectionsFilledWithOnes task;
	task.readData(std::cin);
	task.solve(std::cin);
	task.writeData(std::cout);
	std::cout << std::endl;
	return 0;
}