// Independent exhaustive verifier: rebuild geometry from integer determinants;
// branch on increasing point IDs (x-major), no geometric symmetry reduction.
// Does not read or import the primary generator, groups, or row-search source.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
using namespace std;
using Bits=unsigned __int128;
static Bits line_bad[81][81],circle_bad[81][81][81],vertical[9];
static int n,N,K,chosen[81],used[9];
static uint64_t nodes=0,maxnodes=0,pruned=0,triples=0,circular=0,degenerate=0;
static bool found=false,interrupted=false;
static string witness;
Bits one(int i){return Bits(1)<<i;}
int pop(Bits b){return __builtin_popcountll((uint64_t)b)+__builtin_popcountll((uint64_t)(b>>64));}
int low(Bits b){return (uint64_t)b?__builtin_ctzll((uint64_t)b):64+__builtin_ctzll((uint64_t)(b>>64));}
long long area(int a,int b,int c){
 long long x=a/n,y=a%n,u=b/n,v=b%n,s=c/n,t=c%n;
 return x*(v-t)+u*(t-y)+s*(y-v);
}
long long lift(int a,int b,int c,int d){
 long long xd=d/n,yd=d%n,zd=xd*xd+yd*yd;
 long long x=a/n,y=a%n,u=b/n,v=b%n,s=c/n,t=c%n;
 long long z=x*x+y*y-zd,w=u*u+v*v-zd,r=s*s+t*t-zd;
 x-=xd;y-=yd;u-=xd;v-=yd;s-=xd;t-=yd;
 return x*(v*r-w*t)-y*(u*r-w*s)+z*(u*t-v*s);
}
void recurse(Bits available,int depth){
 if(found||interrupted)return;
 if(maxnodes&&nodes>=maxnodes){interrupted=true;return;}nodes++;
 if(depth==K){
  found=true;ofstream f(witness);f<<"{\"n\":"<<n<<",\"points\":[";
  for(int i=0;i<depth;i++){if(i)f<<",";f<<"["<<chosen[i]/n<<","<<chosen[i]%n<<"]";}f<<"]}\n";return;
 }
 int need=K-depth,bound=0;
 for(int x=0;x<n;x++)bound+=min(2-used[x],pop(available&vertical[x]));
 if(bound<need){pruned++;return;}
 while(available){
  if(pop(available)<need)break;
  int p=low(available);available&=available-1;Bits next=available;
  for(int i=0;i<depth;i++){
   next&=~line_bad[chosen[i]][p];
   for(int j=i+1;j<depth;j++)next&=~circle_bad[chosen[i]][chosen[j]][p];
  }
  chosen[depth]=p;used[p/n]++;recurse(next,depth+1);used[p/n]--;
  if(found||interrupted)return;
 }
}
int main(int argc,char **argv){
 if(argc<5||argc>6){cerr<<"usage: independent n target node_limit witness.json [edges.txt]\n";return 2;}
 n=stoi(argv[1]);K=stoi(argv[2]);maxnodes=stoull(argv[3]);witness=argv[4];N=n*n;
 if(n<2||n>9||K<1||K>N)return 2;
 ofstream dump;if(argc==6)dump.open(argv[5]);
 auto start=chrono::steady_clock::now();
 for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++){
  if(area(a,b,c)==0){triples++;line_bad[a][b]|=one(c);line_bad[a][c]|=one(b);line_bad[b][c]|=one(a);
   if(dump){int ids[3]={a%n*n+a/n,b%n*n+b/n,c%n*n+c/n};sort(ids,ids+3);dump<<"3 "<<ids[0]<<" "<<ids[1]<<" "<<ids[2]<<"\n";}}
  for(int d=c+1;d<N;d++)if(lift(a,b,c,d)==0){
   if(area(a,b,c)==0)degenerate++;else{
    circular++;if(dump){int ids[4]={a%n*n+a/n,b%n*n+b/n,c%n*n+c/n,d%n*n+d/n};sort(ids,ids+4);dump<<"4 "<<ids[0]<<" "<<ids[1]<<" "<<ids[2]<<" "<<ids[3]<<"\n";}}
   circle_bad[a][b][c]|=one(d);circle_bad[a][b][d]|=one(c);circle_bad[a][c][d]|=one(b);circle_bad[b][c][d]|=one(a);
  }
 }
 if(dump)dump.close();
 Bits all=0;for(int p=0;p<N;p++){all|=one(p);vertical[p/n]|=one(p);}
 double gen_seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 recurse(all,0);
 cout<<"{\"status\":\""<<(found?"SAT":interrupted?"UNKNOWN":"EXHAUSTED")<<"\",\"n\":"<<n<<",\"target\":"<<K<<",\"nodes\":"<<nodes<<",\"capacity_prunes\":"<<pruned<<",\"collinear_triples\":"<<triples<<",\"circular_quadruples\":"<<circular<<",\"four_collinear_quadruples\":"<<degenerate<<",\"node_limit\":"<<maxnodes<<",\"generation_seconds\":"<<gen_seconds<<",\"total_seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
}
