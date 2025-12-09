import matplotlib.pyplot as plt
import networkx as nx

def find_all_lis_and_draw(nums):
    n = len(nums)
    if n == 0:
        print("Urutan kosong.")
        return

    dp = [1] * n
    preds = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    preds[i] = [j]
                elif dp[j] + 1 == dp[i]:
                    preds[i].append(j)

    max_len = max(dp)

    end_indices = [i for i, x in enumerate(dp) if x == max_len]

    all_lis = []

    def backtrack(current_idx):
        if not preds[current_idx]:
            return [[(current_idx, nums[current_idx])]]

        paths = []
        for prev_idx in preds[current_idx]:
            sub_paths = backtrack(prev_idx)
            for path in sub_paths:
                paths.append(path + [(current_idx, nums[current_idx])])
        return paths

    for end_idx in end_indices:
        paths = backtrack(end_idx)
        for p in paths:
            values_only = [val for idx, val in p]
            if values_only not in all_lis:
                all_lis.append(values_only)

    G = nx.DiGraph()

    for i in range(n):
        G.add_node(i, label=f"{nums[i]}\n({i})", subset=i)

    lis_edges = set()


    def collect_edges(current_idx):
        if dp[current_idx] == 1:
            return
        for prev_idx in preds[current_idx]:
            lis_edges.add((prev_idx, current_idx))
            collect_edges(prev_idx)

    for end_idx in end_indices:
        collect_edges(end_idx)


    edge_colors = []


    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                if j in preds[i]:
                    G.add_edge(j, i)
                    if (j, i) in lis_edges:
                         edge_colors.append('red')
                    else:
                         edge_colors.append('lightgray')


    plt.figure(figsize=(14, 7))
    pos = nx.multipartite_layout(G, subset_key="subset", align='horizontal')


    node_colors = []
    flattened_lis_indices = set()
    for end_idx in end_indices:
        queue = [end_idx]
        while queue:
            curr = queue.pop(0)
            flattened_lis_indices.add(curr)
            queue.extend(preds[curr])

    for i in range(n):
        if i in flattened_lis_indices:
            node_colors.append('#00FF00')
        else:
            node_colors.append('#e0e0e0')

    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, labels=labels, with_labels=True,
            node_color=node_colors, edge_color=edge_colors,
            node_size=2500, font_size=9, font_weight='bold',
            arrowsize=20, width=2)

    plt.title(f"Visualisasi Semua Kemungkinan LIS\nPanjang: {max_len} | Jumlah Solusi: {len(all_lis)}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    print("\n" + "="*40)
    print("       HASIL PENCARIAN LIS")
    print("="*40)
    print(f"Urutan Input : {nums}")
    print(f"Panjang LIS  : {max_len}")
    print(f"Jumlah LIS   : {len(all_lis)} buah")
    print("-" * 40)
    print("Daftar Solusi LIS:")
    for i, seq in enumerate(all_lis, 1):
        print(f"{i}. {seq}")
    print("="*40)

if __name__ == "__main__":
    print("Masukkan urutan bilangan dipisahkan dengan spasi atau koma.")
    print("Contoh: 4 1 13 7 0 2 8 11 3")

    user_input = input("Input Anda: ")

    try:
        clean_input = user_input.replace(',', ' ')
        sequence = [int(x) for x in clean_input.split()]

        find_all_lis_and_draw(sequence)

    except ValueError:
        print("Error: Pastikan input hanya berupa angka!")