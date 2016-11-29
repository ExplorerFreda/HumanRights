#pragma comment(linker, "/STACK:102400000,102400000")
#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <cctype>
#include <map>
#include <set>
#include <queue>
#include <bitset>
#include <string>
#include <complex>
using namespace std;
typedef pair<int,int> Pii;
typedef long long LL;
typedef unsigned long long ULL;
typedef double DBL;
typedef long double LDBL;
#define MST(a,b) memset(a,b,sizeof(a))
#define CLR(a) MST(a,0)
#define SQR(a) ((a)*(a))
#define PCUT puts("\n----------")

const int maxn=500+10;
const DBL eps=1e-8;
int sgn(DBL x){return x>eps? 1: (x<-eps? -1: 0);}
struct Vector
{
    DBL x,y;
    Vector(DBL _x=0, DBL _y=0):x(_x),y(_y){}
    Vector operator + (const Vector &rhs) const {return Vector(x+rhs.x, y+rhs.y);}
    Vector operator - (const Vector &rhs) const {return Vector(x-rhs.x, y-rhs.y);}
    Vector operator * (const DBL &rhs) const {return Vector(x*rhs, y*rhs);}
    Vector operator / (const DBL &rhs) const {return Vector(x/rhs, y/rhs);}
    DBL operator * (const Vector &rhs) const {return x*rhs.x + y*rhs.y;}
    DBL operator ^ (const Vector &rhs) const {return x*rhs.y - rhs.x*y;}
    int read(){return scanf("%lf%lf", &x, &y);}
};
typedef Vector Point;

struct Line
{
    Point u,v;
    Line(){}
    Line(Point _u,Point _v):u(_u),v(_v){}
};
int N,M;
Point A[maxn], B[maxn];
DBL Area(int,Point*);
DBL CPIA(Point*,Point*,int,int);
DBL SPIA(Point*,Point*,int,int);

double CalcArea(Point a[], int n) {
	double res = 0;
	for (int i = 2; i < n; i ++) {
		res += ((a[i]-a[0])^(a[i-1]-a[0]));
	}
	return res;
}

int main()
{
    freopen("in.txt", "r", stdin);
    freopen("out.txt", "w", stdout);
    while(~scanf("%d%d", &N, &M))
    {
        for(int i=0; i<N; i++) A[i].read();
        for(int i=0; i<N; i++) B[i].read();
		if (sgn(CalcArea(A,N)) != sgn(CalcArea(B,M))) {
			reverse(B, B + M);
		}
        printf("%.2f\n", Area(N,A)+Area(M,B)-SPIA(A,B,N,M));
    }
    fclose(stdin);
    fclose(stdout);
    return 0;
}

DBL Area(int siz, Point p[])
{
    DBL res=0;
    for(int i=1; i<siz; i++) res += (p[i-1]^p[i]);
    res += (p[siz-1]^p[0]);
    return fabs(res*0.5);
}

Point GetLineIntSec(Line l1, Line l2)
{
    DBL a = (l1.v-l1.u)^(l2.u-l1.u), b = (l1.u-l1.v)^(l2.v-l1.v);
    if(sgn(a+b)==0) return Point(1e9,1e9);
    return Point((l2.u.x * b + l2.v.x * a) / (a + b), (l2.u.y * b + l2.v.y * a) / (a + b));
}

DBL CPIA(Point a[], Point b[], int na, int nb)
{
    Point p[20], tmp[20]; // na,nb <=20
    int i, j, tn, sflag, eflag;
    a[na] = a[0], b[nb] = b[0];
    memcpy(p,b,sizeof(Point)*(nb + 1));
    for(i = 0; i < na && nb > 2; i++)
    {
        sflag = sgn((a[i+1]-a[i])^(p[0]-a[i]));
        for(j = tn = 0; j < nb; j++, sflag = eflag)
        {
            if(sflag>=0) tmp[tn++] = p[j];
            eflag = sgn( (a[i + 1]-a[i])^(p[j + 1]-a[i]));
            if((sflag ^ eflag) == -2)
                tmp[tn++] = GetLineIntSec( Line(a[i], a[i + 1]) , Line(p[j], p[j + 1]));
        }
        memcpy(p, tmp, sizeof(Point) * tn);
        nb = tn, p[nb] = p[0];
    }
    if(nb < 3) return 0.0;
    return Area(nb, p);
}

DBL SPIA(Point a[], Point b[], int na, int nb)
{
    int i, j;
    Point t1[4], t2[4];
    double res = 0, num1, num2;
    a[na] = t1[0] = a[0], b[nb] = t2[0] = b[0];
    for(i = 2; i < na; i++)
    {
        t1[1] = a[i-1], t1[2] = a[i];
        num1 = sgn( (t1[1]-t1[0])^(t1[2]-t1[0]));
        if(num1 < 0) swap(t1[1], t1[2]);
        for(j = 2; j < nb; j++)
        {
            t2[1] = b[j - 1], t2[2] = b[j];
            num2 = sgn((t2[1]-t2[0])^(t2[2]-t2[0]));
            if(num2 < 0) swap(t2[1], t2[2]);
            res += CPIA(t1, t2, 3, 3) * num1 * num2;
        }
    }
    return res;
}
