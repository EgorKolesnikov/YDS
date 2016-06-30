#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <list>
#include <queue>

class SpecialDijkstra{

private:

	struct edge {
		int to;
		int weight;

		edge(int to = -1, int weight = -1)
			: to(to)
			, weight(weight)
		{ }
	};

	int vertices;
	int edges;
	int changes;
	int answer;

	std::vector<std::vector<unsigned long long int>> distance;
	std::vector<bool> used;
	std::vector<std::list<edge>> graph;


	void build_path() {
		for(int k = 0; k <= changes; ++k) {
			distance[k][1] = 0;
			for(int i = 1; i <= vertices; ++i){
				used[i] = false;
			}
			std::priority_queue<
				std::pair<unsigned long long int, int>
				, std::vector<std::pair<unsigned long long int, int>> 
				, std::greater<std::pair<unsigned long long int, int>>
			> queue;


			queue.push(std::make_pair(0, 1));
			for(int count_vertex = 0; count_vertex < vertices; ++count_vertex) {
				std::pair<unsigned long long int, int> vertex = queue.top();
				queue.pop();

				int from = vertex.second;
				used[from] = true;
				
				for(edge& e : graph[vertex.second]) {
					int to = e.to;
					int weight = e.weight;
					if(!used[to]){
						if(distance[k][to] > distance[k][from] + weight){
							distance[k][to] = distance[k][from] + weight;
							queue.push(std::make_pair(distance[k][to], to));
						}
						if(k > 0 && distance[k][to] > distance[k - 1][from]){
							distance[k][to] = distance[k - 1][from];
							queue.push(std::make_pair(distance[k - 1][to], to));
						}
					}
				}
			}
		}
	}

	void relax_path() {
		answer = distance[changes][vertices];
	}


public:

	SpecialDijkstra() 
		: vertices(0)
		, edges(0)
		, changes(0)
		, answer(0)
	{ }

	void readData(std::istream& in){
		in >> vertices >> edges >> changes;

		graph.resize(vertices + 1, std::list<edge>());
		distance.resize(changes + 1, std::vector<unsigned long long int>(vertices + 1, 1 << 29));
		used.resize(vertices + 1, false);

		int from, to, weight;
		for(int i = 0; i < edges; ++i){
			in >> from >> to >> weight;
			graph[from].push_back(edge(to, weight));
		}
	}

	void solve(){
		build_path();
		relax_path();
	}

	void writeData(std::ostream& out){
		std::cout << answer;
	}
};


int main(){
	//freopen("in.txt", "r", stdin);
	SpecialDijkstra test;
	test.readData(std::cin);
	test.solve();
	test.writeData(std::cout);

	std::cout << std::endl;
	return 0;
}

/*
private:

	struct edge {
		int to;
		int weight;

		edge(int to = -1, int weight = -1)
			: to(to)
			, weight(weight)
		{ }
	};

	int vertices;
	int edges;
	int changes;

	std::vector<int> path;
	std::vector<int> distance;
	std::vector<bool> used;
	std::vector<std::list<edge>> graph;


	void build_path(){
		distance[1] = 0;
		std::priority_queue<
			std::pair<int, int>
			, std::vector<std::pair<int, int>> 
			, std::greater<std::pair<int, int>>
		> queue;


		queue.push(std::make_pair(0, 1));
		for(int count_vertex = 0; count_vertex < vertices; ++count_vertex) {
			std::pair<int, int> vertex = queue.top();
			queue.pop();
			used[vertex.second] = true;

			for(edge& e : graph[vertex.second]){
				if(!used[e.to] && distance[e.to] > distance[vertex.second] + e.weight){
					distance[e.to] = distance[vertex.second] + e.weight;
					path[e.to] = vertex.second;
					queue.push(std::make_pair(distance[e.to], e.to));
				}
			}
		}
	}
*/