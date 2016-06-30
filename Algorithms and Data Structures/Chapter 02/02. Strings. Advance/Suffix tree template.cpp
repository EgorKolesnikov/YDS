//
//	Very kind for Aliaksei Kolesau to create such an excelent template
//

#include <iostream>
#include <cstring>
#include <map>
#include <vector>
#include <algorithm>
#include <queue>

using std::string;
using std::map;
using std::vector;
using std::min;
using std::pair;

struct Node {
    int parent; // id of parent
    int left, right; // edge to this vector is marked with s[left;right)
    int suffix_link;
    map<char, int> next;

    Node(int parent = -1, int left = 0, int right = 0)
        : parent(parent)
        , left(left)
        , right(right)
        , suffix_link(-1)
    {}

    // returns length of label for edge to this node
    int length() const {
        throw std::runtime_error("Not implemented yet");
    }
};

struct Location {
    int node; // we are on the edge going to this node
    int shift; // we already went this many characters on this edge

    Location(int new_node, int new_shift)
        : node(new_node)
        , shift(new_shift)
    {}
};


class SuffixTree {
public:
    SuffixTree(const string& s)
        : s_(s)
        , current_location_(123, 332) // this is not right
    {
        build();
    }

    void walkTree(int node = 0) {
        for (auto&& edge : nodes_[node].next) {
            std::cout << node << " --> " << edge.second << " with '" << s_.substr(nodes_[edge.second].left, nodes_[edge.second].length()) << "'\n";
        }

        for (auto&& edge : nodes_[node].next) {
            walkTree(edge.second);
        }
    }

private:
    // Can we go from this location with this character?
    bool canGoWith(Location from, char c) const {
        throw std::runtime_error("Not implemented yet");
    }

    // Here we sure, that we can go with s_[left, right), so
    // just need to implement skip-count
    // Be careful while switching from one edge to another
    Location goWith(Location from, int left, int right) {
        throw std::runtime_error("Not implemented yet");
    }

    // Just little helper function:
    // it says node 'to' is now son of node 'from'
    // need to update nodes_[from].next accordingly
    void setNextLink(int from, int to) {
        throw std::runtime_error("Not implemented yet");
    }

    // If you still don't know perfect forwarding
    // go and read about it now
    template<class... Args>
    int addNode(Args&&... args) {
        nodes_.emplace_back(std::forward<Args>(args)...);
        return nodes_.size() - 1;
    }

    // We're staying in current location and want to split it (to add new edge from this location)
    // There are two cases (depending on position.shift value), when location is already explicit
    // in these case we have nothing to do, just return this node
    //
    // in the other case we want to create new node in the middle of the edge
    // make sure that you update parent and next links accordingly (also left and right)
    // suffix link might not be calculated here for new node, but you can if you want
    //
    // return value of function is id of new node
    int splitLocation(Location position) {
        throw std::runtime_error("Not implemented yet");
    }

    // this is easy - calculate suffix link of current node
    // as you can see we initialize suffix link with -1
    // -1 means that we haven't calculated this link and need to do it now
    // otherwise we can just return calculated value (one can see, that suffix link
    // once calculated never changes)
    //
    // Remember that calculating suffix link is different depending on who's your daddy
    //
    // As you can see, return value of this function is int, not Location
    // But suffix link of current node can be implicit. So, if we only have the function
    // which makes implicit location explicit :)
    int getSuffixLink(int node) {
        throw std::runtime_error("Not implemented yet");
    }

    void addCharacter(int position) {
        char c = s_[position]; 
        
        while (true) {
            if (canGoWith(current_location_, c)) {
                current_location_ = goWith(current_location_, position, position + 1);
                break;
            }

            int splittedNode = splitLocation(current_location_);
            int newLeaf = addNode(splittedNode, position, s_.size());
            setNextLink(splittedNode, newLeaf);

            current_location_.node = getSuffixLink(splittedNode); 
            current_location_.shift = nodes_[current_location_.node].length();

            if (splittedNode == 0) {
                break;
            }
        }
    }

    void build() {
        addNode(0, 0, 0);
        for (size_t i = 0; i < s_.size(); ++i) {
            addCharacter(i); 
        }
    }

private:
    string s_;
    Location current_location_;
    vector<Node> nodes_;
};

using namespace std;

int main() {
    std::ios_base::sync_with_stdio(false);
    string s;

    SuffixTree tree(s);
    tree.walkTree(0);

    return 0;
}