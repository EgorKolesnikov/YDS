#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <list>
#include <cstdlib>

class GetRectangles {

	enum class Intersection { 
		NO, NO_MATTER, FIRST_ABOVE, SECOND_ABOVE 
	};

	struct bounds {
		static const int MAX = 1 << 30;
		int left, right;
		int top, bottom;
		int color;

		bounds(
			int left = MAX, int right = -1,
			int top = MAX, int bottom = -1
		):
			left (left), right(right),
			top (top), bottom(bottom)
		{ }

		bool not_initialized(){
			if(left == MAX || top == MAX ||
			   right == -1 || bottom == -1) {
				return true;
			}
			return false;
		}
	};

private:

	int size;
	int definetly_not_null;
	std::vector<std::vector<int>> table;
	std::vector<bounds> rectangles;
	std::vector<std::list<int>> graph;
	std::vector<bool> used;
	std::vector<int> answer;

public:

	GetRectangles() {}

	void readData(std::istream& in) {
		in >> size;
		table.resize(size + 1, std::vector<int>(size + 1));
		rectangles.resize(size + 1);
		graph.resize(size + 1, std::list<int>());
		used.resize(size + 1, false);

		// read rectangles and init edges
		for(int row = 1; row <= size; ++row){
			for(int column = 1; column <= size; ++column){
				in >> table[row][column];

				int color = table[row][column];
				if(color != 0){
					definetly_not_null = color;
					rectangles[color].left = std::min(rectangles[color].left, column);
					rectangles[color].right = std::max(rectangles[color].right, column);
					rectangles[color].top = std::min(rectangles[color].top, row);
					rectangles[color].bottom = std::max(rectangles[color].bottom, row);
				}
			}
		}

		// if there no such color - initialize
		for(int color = 1; color <= size; ++color) {
			rectangles[color].color = color;
			if(rectangles[color].not_initialized()){
				rectangles[color] = bounds(
					rectangles[definetly_not_null].left,
					rectangles[definetly_not_null].left,
					rectangles[definetly_not_null].top,
					rectangles[definetly_not_null].top);
			}
		}
	}


	/*
		May be TL, but I need to be sure that I am doing the right thing
	*/
	Intersection intersection(bounds& first, bounds& second) {
		// check if definetly don't intersect
		if(first.right < second.left || first.bottom < second.top || first.top > second.bottom){
			return Intersection::NO;
		}

		// init intersection bounds
		int left = std::max(first.left, second.left);
		int right = std::min(first.right, second.right);
		int top = ((first.top > second.top) ? first.top : second.top);
		int bottom = std::min(first.bottom, second.bottom);

		// check who is on the top
		for(int i = top; i <= bottom; ++i){
			for(int j = left; j <= right; ++j){
				if(table[i][j] == first.color){
					return Intersection::FIRST_ABOVE;
				}
				else if(table[i][j] == second.color){
					return Intersection::SECOND_ABOVE;
				}
			}
		}

		return Intersection::NO_MATTER;
	}

	void create_graph() {
		for(int first_color = 1; first_color <= size; ++first_color){
			for(int second_color = first_color + 1; second_color <= size; ++second_color) {
				int first_to_intersect = first_color, second_to_intersect = second_color;
				if(rectangles[first_color].left >= rectangles[second_color].left){
					first_to_intersect = second_color;
					second_to_intersect = first_color;
				}

				Intersection verdict = intersection(rectangles[first_to_intersect], rectangles[second_to_intersect]);
				switch(verdict){
					case Intersection::NO:
						// graph[first_to_intersect].push_back(second_to_intersect);
						// graph[second_to_intersect].push_back(first_to_intersect);
						break;
					case Intersection::NO_MATTER:
						// graph[first_to_intersect].push_back(second_to_intersect);
						// graph[second_to_intersect].push_back(first_to_intersect);
						break;
					case Intersection::FIRST_ABOVE:
						graph[second_to_intersect].push_back(first_to_intersect);
						break;
					case Intersection::SECOND_ABOVE:
						graph[first_to_intersect].push_back(second_to_intersect);
						break;
				}
			}
		}
	}

	void dfs(int vertex){
		used[vertex] = true;
		for(int to : graph[vertex]){
			if(!used[to]){
				dfs(to);
			}
		}
		answer.push_back(vertex);
	}

	void topological_sort(){
		for(int vertex = 1; vertex <= size; ++vertex){
			if(!used[vertex]){
				dfs(vertex);
			}
		}
		std::reverse(answer.begin(), answer.end());
	}


	std::vector<int> colors;

	void dfs_cycles(int vertex){
		colors[vertex] = 1;
		for(int to : graph[vertex]){
			if(colors[to] == 0){
				dfs_cycles(to);
			}
			if(colors[to] == 1){
				std::cout << "CYCLE!!!!\n";
				exit(0);
			}
		}
		colors[vertex] = 2;
	}

	void check_cycles(){
		colors.resize(size + 1, 0);

		for(int vertex = 1; vertex <= size; ++vertex){
			if(colors[vertex] == 0){
				dfs_cycles(vertex);
			}
		}
	}

	void solve(){
		create_graph();
		// check_cycles();
		topological_sort();
	}

	void writeData(std::ostream& out) {
		// out << size << "\n";
		for(int color : answer) {
			out << color << ' '
				<< rectangles[color].top << ' ' << rectangles[color].left << ' '
				<< rectangles[color].bottom << ' ' << rectangles[color].right << '\n';
		}
	}
};



/*// tester
int main(int argc, char *argv[]) {
	freopen(argv[1], "r", stdin);
	freopen(argv[2], "w", stdout);

	GetRectangles test;

	test.readData(std::cin);
	test.solve();
	test.writeData(std::cout);

	std::cout << std::endl;
	return 0;
}*/



int main(){
	// freopen("input.txt", "r", stdin);
	GetRectangles test;

	test.readData(std::cin);
	test.solve();
	test.writeData(std::cout);

	std::cout << std::endl;
	return 0;
}