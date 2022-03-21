#include <stdio.h>
#include <stdlib.h>

struct Edge {
    int from, to, w, next;
} *e;
int *head;
int *dis;
int *pre;
int cnt = 0;
int n,m;
const int INF = 0x3f3f3f3f;

void addEdge(int from, int to, int w) {
    cnt++;
    e[cnt].from = from;
    e[cnt].to = to;
    e[cnt].w = w;
    e[cnt].next = head[from];
    head[from] = cnt;
}

void dv(int u, int v) {
    int i;
    for(i = 1; i <= n; i++) {
        dis[i] = INF;
    }
    dis[u] = 0;
    int flag = 1;
    while(flag) {
        flag = 0;
        for(i = 1; i <= cnt; i++) {
            if(dis[e[i].from] + e[i].w < dis[e[i].to]) {
                flag = 1;
                dis[e[i].to] = dis[e[i].from] + e[i].w;
                pre[e[i].to] = e[i].from;
            }
        }
    }
    int *path = (int*)malloc(sizeof(int) * (n+1));
    i = 1;
    int now = v;
    while(pre[now] != u && pre[now] != 0) {
        path[i++] = pre[now];
        now = pre[now];
    }
    printf("DV路径为：R%d", u);
    int j;
    for(j = i-1; j >= 1; j--) {
        printf("-->R%d", path[j]);
    }
    printf("-->R%d", v);
    free(path);
}

int main() {
    printf("输入路由器数量及边数：");
    scanf("%d %d", &n, &m);
    e = (struct Edge *) malloc(sizeof(struct Edge) * (2*m+1));
    head = (int*) malloc(sizeof(int) * (n+1));
    dis = (int*) malloc(sizeof(int) * (n+1));
    pre = (int*) malloc(sizeof(int) * (n+1));

    printf("输入边的开销：\n");
    int i;
    for(i = 1; i <= n;i ++) {
        int u,v,w;
        scanf("%d %d %d", &u, &v, &w);
        addEdge(u,v,w);
        addEdge(v,u,w);
    }
    printf("输入源路由器编号与目的路由器编号：");
    int u,v;
    scanf("%d %d", &u, &v);

    dv(u,v);

    return 0;
}