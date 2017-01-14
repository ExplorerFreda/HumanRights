#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <math.h>
#include <vector>
#include <algorithm>

using namespace std;

const int PAGE_SIZE = 4096 << 9;

class SingleDataReader {
private:
	char buffer[PAGE_SIZE << 2];
	
	void process_single(vector< vector<float> >& vec, 
		const char* str) {
		vector<float> v;
		int l = 0, r = 0;
		for (int j = 0; j < 4096; j ++) {
			l = r;
			while ((str[l] < '0' || str[l] > '9') && str[l]!='-') l ++;
			for (r = l+1; str[r] >= '0' && str[r] <= '9' || str[r] == '.'; r++);
			char buffer[50];
			memcpy(buffer, str + l, sizeof buffer[0] * (r-l));
			buffer[r-l] = 0;
			float number = atof(buffer);
			v.push_back(number);
		}
		vec.push_back(v);
	}
public:
	void ReadSingle(const char* filename, 
		vector< vector<float> >& vec) {
		
		FILE* fin = fopen(filename, "r");
		while (fgets(buffer, PAGE_SIZE << 2, fin)) {
			if (vec.size() % 1000 == 0)
				printf("%d\n", vec.size());
			process_single(vec, buffer);
		}
	}
};


class SingleMatcher{
private:
	static float Dist(const vector<float>& db, const vector<float>& q) {
		float ret = 0;
		for (int i = 0; i < db.size(); i++) {
			ret += (db[i] - q[i]) * (db[i] - q[i]);
		}
		return sqrt(ret);
	}

	static float MatchScore (const vector<float> &db, const vector<float> &q) {
		return Dist(db, q);
	}
	static vector< pair<float, int> > MostMatch(
		const vector< vector<float> >& db, const vector< vector<float> >& q, 
		const int qid) {
		vector< pair<float,int> > result;
		for (int i = 0; i < db.size(); i ++) {
			result.push_back(make_pair(MatchScore(db[i], q[qid]), i));
		}
		sort(result.begin(), result.end());
		
		vector< pair<float,int> > ret;
		for (int i = 0; i < 25; i++) {
			ret.push_back(result[i]);
		}
		return ret;
	}
public:
	static void OutputMatchResult(
		const vector< vector<float> >& db, 
		const vector< vector<float> >& q, 
		const char* filename) {
		FILE* fout = fopen(filename, "w");
		fprintf(fout, "[");
		for (int i = 0; i < q.size(); i++) {
			printf("qid: %d\n", i);
			vector< pair<float,int> > result = MostMatch(db, q, i);
			fprintf(fout, "[");
			for (int j = 0; j < result.size(); j ++) {
				fprintf(fout, "[%d, %.6f]", result[j].second, result[j].first);
				if (j != result.size() - 1) {
					fprintf(fout, ", ");
				}
			}
			fprintf(fout, "]");
			if (i != q.size() - 1) {
				fprintf(fout, ", ");
			}
		}
		fprintf(fout, "]\n");
		fclose(fout);
	}
};


vector< vector<float> > single_vector;
vector< vector<float> > single_Q_vector;
SingleDataReader reader;
int main() { 
	// finetune
//	reader.ReadSingle("../../data/netvlad_finetune_vector.json", 
//		single_vector);
//	reader.ReadSingle("../../data/netvladQ_finetune_vector.json", 
//		single_Q_vector);
//	SingleMatcher::OutputMatchResult(single_vector, single_Q_vector,
//		"../../data/netvlad_single_finetune_matchresult.json");
	

	// vgg-cnn-m
	reader.ReadSingle("../../data/netvlad_vgg-cnn-m_vector.json", 
		single_vector);
	reader.ReadSingle("../../data/netvladQ_vgg-cnn-m_vector.json", 
		single_Q_vector);
	SingleMatcher::OutputMatchResult(single_vector, single_Q_vector,
		"../../data/netvlad_single_vgg-cnn-m_matchresult.json");
	
	return 0;
}
