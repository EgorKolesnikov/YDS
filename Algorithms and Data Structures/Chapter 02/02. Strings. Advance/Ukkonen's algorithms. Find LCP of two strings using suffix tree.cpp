#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>

class SuffixTree {

private:
	struct Node {
		std::map<char, int> next;	// id of next node, in which we can go if we will follow by char
		int left, right;			// edge to this vector is marked with s[left;right)
		int parent;					// id of parent
		int suffix_link;	
		int depth;					// depth of the node (by symbols, not number of edges)
		int mark;					// suffix of what string ends in subtree of that node (if 3 - then both)

		Node(int parent = -1, int l = 0, int r = 0)
			: parent(parent)
			, left(l)
			, right(r)
			, suffix_link(-1)
			, mark(0)
		{ }

		int length() { 
			return right - left; 
		}
	};

	struct Location {
		int node, shift;
		Location(int n, int s)
			: node(n)
			, shift(s)
		{ }
	};

	std::string s;
	std::vector<Node> nodes;
	Location current_location;

	// Need to find LCP.
	// If length of the edge, which goes to leaf greater
	// than second_string_length, then here (in that leaf)
	// ends suffix of the first string, now second.
	int second_string_length;
	int lcp;


public:

	SuffixTree(std::string& s1, std::string& s2)
		: s(s1 + "#" + s2 + "$")
		, current_location(0, 0)
		, second_string_length(s2.length())
		, lcp(0)
	{
		nodes.reserve(5 * s.length());
		build_tree();
	}

	SuffixTree(std::string& s1)
		: s(s1 + "$")
		, current_location(0, 0)
		, second_string_length(-1)
		, lcp(0)
	{
		nodes.reserve(5 * s.length());
		build_tree();
	}

	void print_tree(int node = 0) {
		for (auto&& edge : nodes[node].next) {
			std::cout
				<< node << " --> "
				<< edge.second << " with '"
				<< s.substr(nodes[edge.second].left, nodes[edge.second].length())
				<< "'. Mark = " << nodes[node].mark << ". Depth = " << nodes[node].depth << "\n";
		}
		if (nodes[node].next.empty()) {
			std::cout 
				<< node << " --> " << node 
				<< ". Leaf. Mark = " << nodes[node].mark 
				<< ". Depth = " << nodes[node].depth << "\n";
		}

		for (auto&& edge : nodes[node].next) {
			print_tree(edge.second);
		}
	}

	int find_lcp() {
		nodes[0].depth = 0;
		mark_nodes(0);
		return lcp;
	}


private:

	/*
	*	Compute longest common substring length.
	*	Set depth and mark each node, and calculate lcp.
	*/
	char mark_nodes(int node) {
		nodes[node].depth = nodes[(nodes[node].parent == -1 ? 0 : nodes[node].parent)].depth + nodes[node].right - nodes[node].left;

		if (nodes[node].next.empty()) {
			if (nodes[node].right - nodes[node].left > second_string_length) {
				nodes[node].mark = 1;
			}
			else {
				nodes[node].mark = 2;
			}
			return nodes[node].mark;
		}

		for (auto son : nodes[node].next) {
			char res = mark_nodes(son.second);
			if (nodes[node].mark == 1) {
				if (res == 2) {
					nodes[node].mark = 3;
					lcp = std::max(lcp, nodes[node].depth);
				}
			}
			else if (nodes[node].mark == 2) {
				if (res == 1) {
					nodes[node].mark = 3;
					lcp = std::max(lcp, nodes[node].depth);
				}
			}
			else if (nodes[node].mark == 0) {
				nodes[node].mark = res;
			}
		}

		return 0;
	}


	/*
	*	Building suffix tree.
	*/

	template<class... Args>
	int addNode(Args&&... args) {
		nodes.emplace_back(std::forward<Args>(args)...);
		return nodes.size() - 1;
	}

	Location go(Location from, int left, int right) {
		while (left < right) {
			if (from.shift != nodes[from.node].length()) {
				if (s[nodes[from.node].left + from.shift] != s[left]) {
					return Location(-1, -1);
				}
				if (right - left < nodes[from.node].length() - from.shift) {
					return Location(from.node, from.shift + right - left);
				}

				left += nodes[from.node].length() - from.shift;
				from.shift = nodes[from.node].length();
			}
			else {
				if (nodes[from.node].next.find(s[left]) == nodes[from.node].next.end()) {
					return Location(-1, 0);
				}
				from = Location(nodes[from.node].next[s[left]], 0);
			}
		}
		return from;
	}

	int splitLocation(Location position) {
		if (position.shift == nodes[position.node].length()) {
			return position.node;
		}
		if (position.shift == 0) {
			return nodes[position.node].parent;
		}

		int new_node = addNode(
			nodes[position.node].parent, 
			nodes[position.node].left, 
			nodes[position.node].left + position.shift
		);
		nodes[nodes[position.node].parent].next[s[nodes[position.node].left]] = new_node;
		nodes[new_node].next[s[nodes[position.node].left + position.shift]] = position.node;
		nodes[position.node].parent = new_node;
		nodes[position.node].left += position.shift;
		return new_node;
	}

	int get_suffix_link(int v) {
		if (nodes[v].suffix_link == -1) {
			if (nodes[v].parent == -1) {
				return 0;
			}
			else {
				int to = get_suffix_link(nodes[v].parent);
				nodes[v].suffix_link = splitLocation(
					go(
						Location(to, nodes[to].length())
						, nodes[v].left + (nodes[v].parent == 0)
						, nodes[v].right
					)
				);
			}
		}
		return nodes[v].suffix_link;
	}

	void addCharacter(int position) {
		char c = s[position];

		while (true) {
			Location nptr = go(current_location, position, position + 1);
			if (nptr.node != -1) {
				current_location = nptr;
				return;
			}

			int splittedNode = splitLocation(current_location);
			int newLeaf = addNode(splittedNode, position, s.size());
			nodes[splittedNode].next[s[position]] = newLeaf;

			current_location.node = get_suffix_link(splittedNode);
			current_location.shift = nodes[current_location.node].length();

			if (!splittedNode) {
				break;
			}
		}
	}

	void build_tree() {
		addNode(-1, 0, 0);
		for (size_t i = 0; i < s.size(); ++i) {
			addCharacter(i);
		}
	}
};


int main() {
	std::ios_base::sync_with_stdio(false);
	std::string s1, s2;
	std::cin >> s1 >> s2;

	SuffixTree tree(s1, s2);
	std::cout << tree.find_lcp();

	std::cout << std::endl;
	return 0;
}