"""
Person 0 has a secret and initially shares the secret with a person firstPerson at time 0

get all same time
build graph
"""
class Solution:
    def findAllPeople(self, _, meetings: List[List[int]], firstPerson: int) -> List[int]:
        # 按照 time 从小到大排序
        meetings.sort(key=lambda m: m[2])

        # 一开始 0 和 firstPerson 都知道秘密
        have_secret = set()
        have_secret.add(0)
        have_secret.add(firstPerson)

        i = 0 
        while i < len(meetings):
            x,y,time = meetings[i]
            g = defaultdict(list)
            while i < len(meetings) and meetings[i][2] == time:
                x,y,time = meetings[i]
                g[x].append(y)
                g[y].append(x)
                i += 1
            
            def dfs(x):
                vis.add(x)
                have_secret.add(x)
                for nie in g[x]:
                    if nie not in vis:
                        dfs(nie)
            vis = set()
            for x in g:
                if x in have_secret and x not in vis:
                    dfs(x)
        return list(have_secret)
                    