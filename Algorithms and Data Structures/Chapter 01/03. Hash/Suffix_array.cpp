#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

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

int lcp(int i1, int i2){
	int middle = 0;
	int left = 1;
	int right = inputLength - std::max(i1, i2);
	while(left <= right){
 		middle = (left + right) / 2;
		if(getHash(i1, i1 + middle) == getHash(i2, i2 + middle)){
			left = middle + 1;
		}
		else{
			right = middle - 1;
		}
	}
	return left - 1;
}

bool compare(int i1, int i2){
	int length = lcp(i1, i2);
	return inputString[i1 + length] < inputString[i2 + length];
}

void solve(std::vector<int>& result){
	for(int i=0; i < result.size(); ++i){
		result[i] = i;
	}
	std::sort(begin(result), end(result), compare);
}
int main(){
	std::string str;
	std::cin >> str;
	init(str);
	std::vector<int> result(str.size());
	solve(result);
	for(int i=0; i < result.size(); ++i){
		std::cout << result[i] + 1 << " ";
	}
	std::cout << std::endl;
	return 0;
}