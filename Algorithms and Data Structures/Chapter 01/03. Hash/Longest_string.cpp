#include <iostream>
#include <algorithm>
#include <vector>
#include <map>

int inputLength;
std::string inputString;
unsigned long long p = 73;
std::vector<unsigned long long> pPower;
std::vector<unsigned long long> suff_hash;

void init(std::string& str){
	inputString = str;
	inputLength = inputString.size();
	pPower.resize(inputLength + 1);	
	suff_hash.resize(inputLength + 1);

	pPower[0] = 1;
	for(int i = 1; i <= inputLength; ++i){
		pPower[i] = pPower[i-1] * p;
	}
	suff_hash[inputLength] = 0;
	for(int i = inputLength - 1; i >= 0; --i){
		suff_hash[i] = suff_hash[i + 1] * p + inputString[i];
	}
}

unsigned long long getHash(int l, int r){
	return suff_hash[l] - suff_hash[r] * pPower[r - l];
}

int solve(){
	int left = 0;
	int right = inputLength - 1;
	int middle = 0;
	
	bool found = false;
	unsigned long long hash = 0;
	while(left < right){
		found = false;
		middle = (left + right + 1) / 2;
		std::map<unsigned long long, int> seenAlready;
		for(int i = 0; i <= inputLength - middle; ++i){
			hash = getHash(i, i + middle);
			if(seenAlready[hash]){
				found = true;
				break;
			}
			seenAlready[hash] = 1;
		}
		if(found){
			left = middle; 
		}
		else{
			right = middle - 1;
		}
	}
	return left;
}

int main(){
	std::string str;
	std::cin >> str;
	init(str);
	int answer = solve();
	std::cout << answer << std::endl;
	return 0;
}