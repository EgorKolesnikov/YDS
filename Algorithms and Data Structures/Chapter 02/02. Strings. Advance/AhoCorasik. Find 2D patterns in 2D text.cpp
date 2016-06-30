#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <map>


template<typename PatternType, typename AlphabetType>
class Trie {

private:
	struct node {
		std::map<AlphabetType, int> next;
		int suffix_link;
		int parent_node;
		bool leaf;
		AlphabetType symbol_to_here;
		std::vector<int> here_patterns_id;

		node() {
			suffix_link = -1;
			parent_node = 0;
			symbol_to_here = -1;
			leaf = false;
		}
	};

	int new_node() {
		trie.push_back(node());
		return trie_size++;
	}

	int get_suffix_link(int v) {
		if (trie[v].suffix_link == -1) {
			if (v == Root || trie[v].parent_node == Root) {
				trie[v].suffix_link = Root;
			}
			else {
				trie[v].suffix_link = go(get_suffix_link(trie[v].parent_node), trie[v].symbol_to_here);
			}

		}
		return trie[v].suffix_link;
	}


public:

	Trie() { }

	Trie(std::vector<PatternType>& patterns)
		: patterns(patterns)
		, numerate(0)
	{
		trie_size = 0;
		Root = new_node();
		new_patterns.resize(patterns.size());
		build_trie();
		walk_tree();
	}

	// We don't need to copy new patterns after first AhoCorasik work.
	// That's why we need move constructor
	Trie(std::vector<PatternType> && patterns)
		: patterns(patterns)
		, numerate(0)
	{
		trie_size = 0;
		Root = new_node();
		new_patterns.resize(patterns.size());
		build_trie();
		walk_tree();
	}

	void add_character(int& now, AlphabetType character) {
		if (trie[now].next.find(character) == trie[now].next.end()) {
			trie[now].next[character] = new_node();
			trie[trie[now].next[character]].suffix_link = -1;
			trie[trie[now].next[character]].parent_node = now;
			trie[trie[now].next[character]].symbol_to_here = character;
		}
		now = trie[now].next[character];
	}

	// There some significant differences between building trie with
	// std::vector<std::vector<int>> and std::vector<std::string>.
	// So there are two different versions for Trie<std::vector<std::vector<int>>, int>
	// and Trie<std::vector<std::string>, char>, which are 
	// implemented down below (after class decloration)
	void build_trie();


	// Walk through tree to set suffix links for each node
	void walk_tree() {
		std::queue<int> q;
		q.push(Root);
		while (!q.empty()) {
			int now = q.front();
			q.pop();

			trie[now].suffix_link = get_suffix_link(now);

			for (auto iter = trie[now].next.begin(); iter != trie[now].next.end(); ++iter) {
				q.push(iter->second);
			}
		}
	}


public:

	int Root;
	int trie_size;
	int numerate;
	std::vector<node> trie;
	std::vector<PatternType> patterns;
	std::vector<std::vector<int>> new_patterns;	


	//
	//	Interface for AhoCorasik2D
	//
	int getRoot() {
		return Root;
	}

	bool is_leaf(int v) {
		return trie[v].leaf;
	}

	int get_patterns_number() {
		return patterns.size();
	}

	std::vector<int>& get_patterns_id(int vertex) {
		return trie[vertex].here_patterns_id;
	}

	// As I commented earlier: we don't need to save new_patterns
	// for correct work of first trie (we do that work only for second trie)
	std::vector<std::vector<int>>&& get_new_patterns() {
		return std::move(new_patterns);
	}

	int go(int v, AlphabetType ch) {
		if (trie[v].next.find(ch) != trie[v].next.end()) {
			return trie[v].next[ch];
		}
		else {
			return (v == 0 ? 0 : go(get_suffix_link(v), ch));
		}
	}
};

template<>
void Trie<std::vector<std::string>, char>::build_trie() {
	for (size_t pattern = 0; pattern < patterns.size(); ++pattern) {
		for (size_t line = 0; line < patterns[pattern].size(); ++line) {
			int now = Root;
			for (char character: patterns[pattern][line]) {
				add_character(now, character);
			}

			if (!trie[now].leaf) {
				trie[now].leaf = true;
				trie[now].here_patterns_id.push_back(numerate);
				new_patterns[pattern].push_back(numerate++);
			}
			else {
				new_patterns[pattern].push_back(trie[now].here_patterns_id[0]);
			}
		}
	}
}

template<>
void Trie<std::vector<int>, int>::build_trie() {
	for (size_t pattern = 0; pattern < patterns.size(); ++pattern) {
		int now = Root;
		for (int character : patterns[pattern]) {
			add_character(now, character);
		}

		trie[now].leaf = true;
		trie[now].here_patterns_id.push_back(pattern);
	}
}


class AhoCorasik2D {

private:
	Trie<std::vector<std::string>, char> preprocess;
	Trie<std::vector<int>, int> process;
	std::vector<int> answer;
	std::vector<std::string> text;
	std::vector<std::vector<std::string>> patterns;


	// using result from preprocess, so just move, no need to copy
	std::vector<int> count_patterns_match(std::vector<std::vector<int>> && new_text) {
		answer.resize(patterns.size());
		std::vector<int> temp_pattern_id;

		for (size_t column = 0; column < new_text[0].size(); ++column) {
			int now = process.getRoot();
			for (size_t row = 0; row < new_text.size(); ++row) {
				now = process.go(now, new_text[row][column]);

				if (process.is_leaf(now)) {
					temp_pattern_id = process.get_patterns_id(now);
					for (size_t i = 0; i < temp_pattern_id.size(); ++i) {
						++answer[temp_pattern_id[i]];
					}
				}
			}
		}

		return answer;
	}

	std::vector<std::vector<int>> preprocess_work() {
		std::vector<std::vector<int>> result(text.size(), std::vector<int>(text[0].size(), -1));

		for (size_t row = 0; row < text.size(); ++row) {
			int now = preprocess.getRoot();
			for (size_t column = 0; column < text[row].size(); ++column) {
				now = preprocess.go(now, text[row][column]);

				if (preprocess.is_leaf(now)) {
					result[row][column] = preprocess.get_patterns_id(now)[0];
				}
			}
		}

		return result;
	}

public:

	AhoCorasik2D() { }

	void read_data(std::istream& in) {
		int t, N, M;
		in >> N >> M;
		std::string tempstr;
		for (int i = 0; i < N; ++i) {
			in >> tempstr;
			text.push_back(tempstr);
		}

		in >> t >> N >> M;
		patterns.resize(t);
		for (int i = 0; i < t; ++i) {
			for (int j = 0; j < N; ++j) {
				in >> tempstr;
				patterns[i].push_back(tempstr);
			}
		}
	}

	void solve() {
		// can use regular or move constructor (for task and testing I choose move)
		preprocess = Trie<std::vector<std::string>, char>(std::move(patterns));
		process = Trie<std::vector<int>, int>(preprocess.get_new_patterns());

		count_patterns_match(preprocess_work());
	}

	void write_data(std::ostream& out) {
		for (int pattern_count : answer) {
			out << pattern_count << " ";
		}
	}
};


int main() {	
	AhoCorasik2D test;
	test.read_data(std::cin);
	test.solve();
	test.write_data(std::cout);	

	std::cout << std::endl;
	return 0;
}