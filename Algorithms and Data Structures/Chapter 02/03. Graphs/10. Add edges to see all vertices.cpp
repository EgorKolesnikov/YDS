#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <list>


class AddGraph {

private:
	int vertices;
	int edges;
	int answer;
	std::vector<bool> used;
	std::vector<int> time_out;
	std::vector<std::vector<int>> components;
	std::vector<std::list<int>> graph;
	std::vector<std::list<int>> inverse_graph;
	std::vector<std::list<int>> new_graph;
	std::vector<int> vertex_component_mark;
	int where_first_vertex;


	void dfs1(int from) {
		used[from] = true;
		for(int to : graph[from]){
			if(!used[to]){
				dfs1(to);
			}
		}
		time_out.push_back(from);
	}

	void dfs2(int from) {
		used[from] = true;
		vertex_component_mark[from] = components.size();
		components[components.size() - 1].push_back(from);
		for(int to : inverse_graph[from]){
			if(!used[to]){
				dfs2(to);
			}
		}
	}

	void initialize_components(){
		used.assign(vertices + 1, false);
		for(int vertex = 1; vertex <= vertices; ++vertex){
			if(!used[vertex]){
				dfs1(vertex);
			}
		}

		used.assign(vertices + 1, false);
		for(int vertex = 1; vertex <= vertices; ++vertex){
			int v = time_out[vertices - vertex];
			if(!used[v]) {
				components.push_back(std::vector<int>());
				dfs2(v);
			}
		}
	}

	void build_new_graph() {
		new_graph.resize(components.size() + 1, std::list<int>());

		for(int vertex = 1; vertex <= vertices; ++vertex){
			for(int to : inverse_graph[vertex]){
				if(vertex_component_mark[vertex] != vertex_component_mark[to]){
					new_graph[vertex_component_mark[vertex]].push_back(vertex_component_mark[to]);
				}
			}
		}
	}

	void count() {
		answer = 0;
		for(int component = 1; component <= components.size(); ++component){
			if(component != vertex_component_mark[1] && new_graph[component].size() == 0){
				++answer;
			}
		}
	}




public:
	AddGraph() 
		: vertices(0)
		, edges(0)
		, answer(0)
	{ }

	void readData(std::istream& in){
		in >> vertices >> edges;
		graph.resize(vertices + 1, std::list<int>());
		inverse_graph.resize(vertices + 1, std::list<int>());
		used.resize(vertices + 1, false);
		vertex_component_mark.resize(vertices + 1);

		int from, to;
		for(int edge = 0; edge < edges; ++edge){
			in >> from >> to;
			if(from != to){
				graph[from].push_back(to);
				inverse_graph[to].push_back(from);
			}
		}
	}

	void solve() {
		initialize_components();
		build_new_graph();
		count();
	}

	void writeData(std::ostream& out){
		std::cout << answer;
	}

};


int main() {
	AddGraph test;

	test.readData(std::cin);
	test.solve();
	test.writeData(std::cout);

	std::cout << std::endl;
	return 0;
}