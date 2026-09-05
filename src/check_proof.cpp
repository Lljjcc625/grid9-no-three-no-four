// Independent checker for GRIDPROOF 1: trusted inputs are n,target only.
// Geometry is rebuilt by full integer determinant enumeration; no group file.
// Branch rows come from the certificate and every feasible row choice is checked.
#include <algorithm>
#include <array>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Set=bitset<81>;
static Set lines[81][81],circles[81][81][81],row_sets[9];
static int n,N,target;
static ifstream proof;
static uint64_t nodes=0,row_leaves=0,col_leaves=0,branches=0;
static vector<array<int,4>> perms;
static vector<int> signs;
[[noreturn]] void fail(const string&s){throw runtime_error(s);}
long long orient(int a,int b,int c){
 int x=a%n,y=a/n,u=b%n,v=b/n,s=c%n,t=c/n;
 return 1LL*x*(v-t)+1LL*u*(t-y)+1LL*s*(y-v);
}
long long determinant4(int a,int b,int c,int d){
 int pts[4]={a,b,c,d};long long m[4][4];
 for(int i=0;i<4;i++){int x=pts[i]%n,y=pts[i]/n;m[i][0]=x*x+y*y;m[i][1]=x;m[i][2]=y;m[i][3]=1;}
 long long result=0;
 for(size_t z=0;z<perms.size();z++){long long term=signs[z];for(int i=0;i<4;i++)term*=m[i][perms[z][i]];result+=term;}
 return result;
}
Set add_point(Set available,int p,const vector<int>&selected){
 available.reset(p);
 for(size_t i=0;i<selected.size();i++){
  available&=~lines[p][selected[i]];
  for(size_t j=i+1;j<selected.size();j++)available&=~circles[p][selected[i]][selected[j]];
 }
 return available;
}
void check_node(Set available,unsigned remaining,vector<int>&selected){
 nodes++;int tag=proof.get();if(tag==EOF)fail("truncated certificate");
 int need=target-int(selected.size());if(need<=0)fail("certificate reaches target size");
 int rcount[9]={},ccount[9]={},used[9]={};
 for(int p=0;p<N;p++)if(available.test(p)){
  if(!(remaining&(1u<<(p/n))))fail("candidate in processed row");
  rcount[p/n]++;ccount[p%n]++;
 }
 for(int p:selected)used[p%n]++;
 int rb=0,cb=0;for(int i=0;i<n;i++){
  if(remaining&(1u<<i))rb+=min(2,rcount[i]);
  if(used[i]>2)fail("invalid selected column");
  cb+=min(2-used[i],ccount[i]);
 }
 if(tag==0){if(rb>=need)fail("invalid row-capacity leaf");row_leaves++;return;}
 if(tag==1){if(cb>=need)fail("invalid column-capacity leaf");col_leaves++;return;}
 int row=tag-16;if(row<0||row>=n||!(remaining&(1u<<row)))fail("invalid branch row");
 if(rb<need||cb<need)fail("noncanonical branch below capacity bound");
 branches++;vector<int> choices;for(int x=0;x<n;x++){int p=row*n+x;if(available.test(p))choices.push_back(p);}
 int lower=max(0,need-(rb-min(2,rcount[row])));Set future=available&~row_sets[row];unsigned rest=remaining&~(1u<<row);
 if(need>=2&&lower<=2){
  for(size_t i=0;i<choices.size();i++){
   int p=choices[i];Set after_p=add_point(available,p,selected);selected.push_back(p);
   for(size_t j=i+1;j<choices.size();j++){
    int q=choices[j];if(!after_p.test(q))continue;
    Set next=add_point(after_p,q,selected)&~row_sets[row];selected.push_back(q);
    check_node(next,rest,selected);selected.pop_back();
   }
   selected.pop_back();
  }
 }
 if(lower<=1)for(int p:choices){
  Set next=add_point(future,p,selected);selected.push_back(p);check_node(next,rest,selected);selected.pop_back();
 }
 if(lower==0)check_node(future,rest,selected);
}
int main(int argc,char**argv){
 try{
  if(argc!=4)fail("usage: check_proof certificate.trace expected_n expected_target");
  int expected_n=stoi(argv[2]),expected_target=stoi(argv[3]);
  proof.open(argv[1],ios::binary);string magic;int version;
  if(!(proof>>magic>>version>>n>>target)||magic!="GRIDPROOF"||version!=1||n!=expected_n||target!=expected_target||n<2||n>9||target<1||target>n*n)fail("invalid or mismatched header");
  if(proof.get()!='\n')fail("invalid header terminator");
  N=n*n;
  auto start=chrono::steady_clock::now();array<int,4> p={0,1,2,3};
  do{perms.push_back(p);int inversions=0;for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)inversions+=p[i]>p[j];signs.push_back(inversions%2?-1:1);}while(next_permutation(p.begin(),p.end()));
  uint64_t triples=0,zero_quads=0;
  for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++){
   if(orient(a,b,c)==0){triples++;int v[3]={a,b,c};do{lines[v[0]][v[1]].set(v[2]);}while(next_permutation(v,v+3));}
   for(int d=c+1;d<N;d++)if(determinant4(a,b,c,d)==0){zero_quads++;int v[4]={a,b,c,d};do{circles[v[0]][v[1]][v[2]].set(v[3]);}while(next_permutation(v,v+4));}
  }
  Set all;for(int q=0;q<N;q++){all.set(q);row_sets[q/n].set(q);}vector<int>selected;
  check_node(all,(1u<<n)-1,selected);
  if(proof.get()!=EOF)fail("trailing certificate data");
  cout<<"{\"status\":\"VERIFIED_UNSAT\",\"n\":"<<n<<",\"target\":"<<target<<",\"nodes\":"<<nodes<<",\"row_bound_leaves\":"<<row_leaves<<",\"column_bound_leaves\":"<<col_leaves<<",\"branch_nodes\":"<<branches<<",\"collinear_triples\":"<<triples<<",\"zero_determinant_quadruples\":"<<zero_quads<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
  return 0;
 }catch(const exception&e){cerr<<"REJECTED: "<<e.what()<<"\n";return 1;}
}
