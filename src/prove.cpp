// Proof-producing exhaustive row search. No symmetry reduction, no node limit.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Mask=__uint128_t;
static Mask L[81][81],C[81][81][81],rowmask[9],colmask[9];
static int n,N,target,S[81],cols[9];
static uint64_t nodes=0,prune_rows=0,prune_cols=0,leaves=0;
static bool found=false;
static string out;
static ofstream certificate;
int count(Mask m){return __builtin_popcountll((uint64_t)m)+__builtin_popcountll((uint64_t)(m>>64));}
int first(Mask m){return (uint64_t)m?__builtin_ctzll((uint64_t)m):64+__builtin_ctzll((uint64_t)(m>>64));}
Mask bit(int p){return Mask(1)<<p;}
Mask extend(Mask cand,int p,int depth){
 Mask ban=bit(p);
 for(int i=0;i<depth;i++){
  ban|=L[p][S[i]];
  for(int j=0;j<i;j++)ban|=C[p][S[i]][S[j]];
 }
 return cand&~ban;
}
void dfs(Mask cand,unsigned rows,int depth){
 if(found)return;
 nodes++;
 int need=target-depth;
 if(!need){found=true;leaves++;return;}
 if(!rows){leaves++;certificate.put(char(0));return;}
 int capacity=0,bestrow=-1,mincount=100,bestcap=0;
 for(int ix=0;ix<n;ix++){
  int y=(ix%2==0)?ix/2:n-1-ix/2;
  if(!(rows&(1u<<y)))continue;
  int cnt=count(cand&rowmask[y]);capacity+=min(2,cnt);
  if(cnt<mincount){mincount=cnt;bestrow=y;bestcap=min(2,cnt);}
 }
 if(capacity<need){prune_rows++;certificate.put(char(0));return;}
 int cc=0;for(int x=0;x<n;x++)cc+=min(2-cols[x],count(cand&colmask[x]));
 if(cc<need){prune_cols++;certificate.put(char(1));return;}
 int y=bestrow;certificate.put(char(16+y));Mask available=cand&rowmask[y],future=cand&~rowmask[y];
 unsigned nextrows=rows&~(1u<<y);int minimum=max(0,need-(capacity-bestcap));
 if(need>=2&&bestcap>=2){
  Mask bs=available;
  while(bs){int p=first(bs);bs&=bs-1;Mask afterp=extend(cand,p,depth);
   Mask qs=bs&afterp;S[depth]=p;cols[p%n]++;
   while(qs){int q=first(qs);qs&=qs-1;
    Mask next=extend(afterp,q,depth+1)&~rowmask[y];S[depth+1]=q;cols[q%n]++;
    dfs(next,nextrows,depth+2);cols[q%n]--;
    if(found)break;
   }
   cols[p%n]--;if(found)return;
  }
 }
 if(minimum<=1){
  Mask bs=available;
  while(bs){int p=first(bs);bs&=bs-1;
   Mask next=extend(future,p,depth);S[depth]=p;cols[p%n]++;
   dfs(next,nextrows,depth+1);cols[p%n]--;
   if(found)return;
  }
 }
 if(minimum==0)dfs(future,nextrows,depth);
}
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: prove groups.txt target certificate.trace\n";return 2;}
 ifstream f(argv[1]);int m;f>>n>>m;if(!f||n<2||n>9)return 2;N=n*n;target=stoi(argv[2]);out=argv[3];
 if(target<1||target>N)return 2;
 for(int i=0;i<m;i++){
  int cap,k;f>>cap>>k;vector<int> vs(k);Mask mask=0;
  for(int &v:vs){f>>v;if(v<0||v>=N)return 2;mask|=bit(v);}
  if(cap==2){for(int a:vs)for(int b:vs)if(a!=b)L[a][b]|=mask&~(bit(a)|bit(b));}
  else if(cap==3){for(int a:vs)for(int b:vs)if(a!=b)for(int c:vs)if(c!=a&&c!=b)C[a][b][c]|=mask&~(bit(a)|bit(b)|bit(c));}
  else return 2;
 }
 if(!f)return 2;
 Mask all=0;for(int p=0;p<N;p++){all|=bit(p);rowmask[p/n]|=bit(p);colmask[p%n]|=bit(p);}
 certificate.open(out,ios::binary);if(!certificate){cerr<<"cannot open certificate\n";return 2;}
 certificate<<"GRIDPROOF 1 "<<n<<" "<<target<<"\n";
 auto start=chrono::steady_clock::now();dfs(all,(1u<<n)-1,0);
 certificate.flush();bool written=bool(certificate);certificate.close();
 if(!written||found){remove(out.c_str());cerr<<"No UNSAT certificate produced\n";return 1;}
 cout<<"{\"status\":\"CERTIFICATE_PRODUCED\",\"n\":"<<n<<",\"target\":"<<target<<",\"nodes\":"<<nodes<<",\"row_prunes\":"<<prune_rows<<",\"column_prunes\":"<<prune_cols<<",\"leaves\":"<<leaves<<",\"node_limit\":0,\"root_reflection\":false,\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
 return 0;
}
