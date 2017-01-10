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

class PyramidDataReader {
private:
	char buffer[PAGE_SIZE << 2];
	
	void process_pyramid(vector< vector< vector<float> > >& vec, 
		const char* str) {
		vector< vector<float> > v;
		for (int i = 0, l = 0, r = 0; i < 14; i ++) {
			v.push_back(vector<float>());
			for (int j = 0; j < 4096; j ++) {
				l = r;
				while ((str[l] < '0' || str[l] > '9')) l ++;
				for (r = l; str[r] >= '0' && str[r] <= '9' || str[r] == '.'; r++);
				char buffer[50];
				memcpy(buffer, str + l, sizeof buffer[0] * (r-l));
				buffer[r-l] = 0;
				float number = atof(buffer);
				v[i].push_back(number);
			}
		}
		vec.push_back(v);
	}
public:
	void ReadPyramid(const char* filename, 
		vector< vector< vector<float> > >& vec, 
		const int read_number = 1125) {
		int fd = open(filename, O_RDWR | O_APPEND | O_CREAT);
		if (fd < 0) {
			printf("open failed!\n");
			exit(1);
		}
		
		char *p_map = (char *) mmap(
			0, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
		if (p_map == MAP_FAILED) {
			printf("mmap failed!\n");
			munmap(p_map, PAGE_SIZE);
			exit(1);
		}
		strcpy(buffer, p_map);
		int cnt = 0;
		long long buffer_head = 0;
		for (char* pos = strstr(buffer, "\n"); pos != NULL; 
			pos = strstr(buffer, "\n")) {
			*pos = 0;
			process_pyramid(vec, buffer);
			strcpy(buffer, pos + 1);
			printf("%d %d %d\n", ++ cnt, strlen(buffer), strlen(p_map));
			if (cnt == read_number - 1) {
				process_pyramid(vec, buffer);
				break;
			}
			if (strlen(buffer) < PAGE_SIZE) {
				munmap(p_map, PAGE_SIZE);
				p_map = (char *) mmap(
					NULL, PAGE_SIZE, PROT_READ, MAP_SHARED, fd, 
					buffer_head += PAGE_SIZE);
				if (p_map == MAP_FAILED) {
					printf("mmap failed!\n");
					munmap(p_map, PAGE_SIZE);
					exit(1);
				}
				strcpy(buffer + strlen(buffer), p_map);
			}
		}
		munmap(p_map, PAGE_SIZE);
	}
};


class PyramidMatcher{
private:
	static float Dist(const vector<float>& db, const vector<float>& q) {
		float ret = 0;
		for (int i = 0; i < db.size(); i++) {
			ret += (db[i] - q[i]) * (db[i] - q[i]);
		}
		return sqrt(ret);
	}

	static float MatchScore (const vector< vector<float> > &db,
	const vector< vector<float> > & q) {
		float ret = 0;
		// layer 1
		ret += Dist(db[0], q[0]);
		// layer 2
		for (int i = 0; i < 5; i ++) {
			float score = 1e10;
			for (int j = 0; j < 5; j ++) {
				score = min(score, Dist(q[i], db[j]));
			}
			ret += score / 4;
		}
		// layer 3
		for (int i = 5; i < 14; i ++) {
			float score = 1e10;
			for (int j = 5; j < 14; j ++) {
				score = min(score, Dist(q[i], db[j]));
			}
			ret += score / 9;
		}
		return ret;
	}
	static vector< pair<float, int> > MostMatch(
		const vector< vector< vector<float> > >& db, 
		const vector< vector< vector<float> > >& q, 
		const int qid) {
		vector< pair<float,int> > result;
		for (int i = 0; i < db.size(); i ++) {
			if (i % 1000 == 0) {
				printf("did: %d\n", i);
			}
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
		const vector< vector< vector<float> > >& db, 
		const vector< vector< vector<float> > >& q, 
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


vector< vector< vector<float> > > pyramid_vector;
vector< vector< vector<float> > > pyramid_Q_vector;
PyramidDataReader reader;
int main() {
	reader.ReadPyramid("../../data/netvlad_finetune_pyramid_vector.json", 
		pyramid_vector, 75984);
	reader.ReadPyramid("../../data/netvladQ_finetune_pyramid_vector.json", 
		pyramid_Q_vector);
	
	PyramidMatcher::OutputMatchResult(pyramid_vector, pyramid_Q_vector,
		"../../data/netvlad_pyramid_vgg-cnn-m_matchresult.json");
	
	return 0;
}
