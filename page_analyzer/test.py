n, m, q = map(int, input().split())

reset_count = [0] * n  # список числа перезапусков для каждого дата-центра
active_count = [[m] * n for _ in range(m)]  # таблица числа активных серверов в каждом дата-центре

max_center = min_center = 0  # текущий дата-центр с наибольшим/наименьшим произведением

for i in range(q):
    query = input().split()
    if query[0] == "RESET":
        center = int(query[1]) - 1
        reset_count[center] += 1
    elif query[0] == "DISABLE":
        center, server = map(int, query[1:])
        active_count[server-1][center-1] -= 1
        if active_count[server-1][center-1] == 0:
            reset_count[center-1] += 1
    elif query[0] == "GETMAX":
        max_prod = -1
        for i in range(n):
            prod = reset_count[i] * (m - sum(server == 0 for server in active_count[:, i]))
            if prod > max_prod:
                max_prod = prod
                max_center = i
        print(max_center+1)
    elif query[0] == "GETMIN":
        min_prod = float('inf')
        for i in range(n):
            prod = reset_count[i] * (m - sum(server == 0 for server in active_count[:, i]))
            if prod < min_prod:
                min_prod = prod
                min_center = i
        print(min_center+1)
