# Union-Find (Disjoint Set) Algoritması

## Algoritmanın Amacı

Union-Find algoritması, bir veri kümesindeki elemanların hangi alt gruba (kümeye) ait olduğunu verimli bir şekilde takip etmek için kullanılır. Temel olarak kümeleri birleştirme (union) ve bir elemanın hangi kümeye ait olduğunu bulma (find) işlemlerini sağlar.

## Algoritma Yapısı ve Türü

Union-Find bir veri yapısı algoritmasıdır. Genellikle açgözlü (greedy) algoritmalarla birlikte çalışır. İki temel işlevi vardır:

- Find(x): x elemanının ait olduğu kümenin temsilcisini (kökünü) bulur.
- Union(x, y): x ve y elemanlarının ait olduğu kümeleri birleştirir.

## Kullanım Alanları

- Minimum Spanning Tree algoritmaları (örneğin Kruskal)
- Dinamik bağlantı takibi
- Sosyal ağlarda topluluk belirleme
- Kümeleme işlemleri
- Oyunlarda grup/lonca yapılarının yönetimi

## Örnek Senaryo: Kruskal ile Kullanım

Aşağıdaki gibi bir grafik üzerinde minimum ağırlıklı döngüsüz bir yapı (MST) oluşturmak için:

Kenarlar: (0-1):1, (1-3):3, (2-3):2, (0-2):4

Kenarlar ağırlığa göre sıralanır ve en düşükten başlanarak Union-Find kullanılarak döngü oluşturulmadan kenarlar seçilir.

## Örnek Senaryo: Sosyal Ağda Arkadaşlık Bağlantıları

Bir sosyal ağda, kullanıcılar arasında arkadaşlık ilişkilerini takip etmek için Union-Find algoritması kullanılabilir. Diyelim ki 6 kullanıcı var ve aralarındaki bazı arkadaşlıklar şu şekilde:

- 0 ve 1 arkadaş
- 2 ve 3 arkadaş
- 4 ve 5 arkadaş
- 1 ve 2 arkadaş

Bu bağlantılarla, aşağıdaki işlemleri gerçekleştirebiliriz:

- 0 ve 2'nin aynı arkadaş grubunda olup olmadığını kontrol etmek için find(0) ve find(2) kullanırız. Bu durumda, 0 ve 2'nin farklı kümelerde olduğu görülür.
- unionSets(0, 2) işlemi ile 0 ve 2'nin arkadaşlık grubunu birleştirebiliriz.
- Sonra, connected(0, 3) ile 0 ve 3'ün aynı grupta olup olmadığını kontrol edebiliriz. Bu durumda, 0 ve 3 artık aynı gruptadır çünkü 0 ve 2 arkadaş olmuştu.

## Zaman ve Bellek Karmaşıklığı

| İşlem     | Zaman Karmaşıklığı | Bellek Kullanımı |
|-----------|--------------------|------------------|
| Find      | O(α(n))            | O(n)             |
| Union     | O(α(n))            | O(n)             |

Buradaki α(n), inverse Ackermann fonksiyonudur. Uygulamada neredeyse sabit sürede işlem yapılabilir.

## Temel Adımlar

1. Her eleman başlangıçta kendi kümesindedir.
2. Find işlemi ile bir elemanın temsilcisi bulunur.
3. Union işlemi ile iki farklı küme birleştirilir.
4. Path Compression ile Find işlemi hızlandırılır.
5. Union by Rank veya Union by Size ile kümeler dengeli biçimde birleştirilir.

## Avantajları

- Hızlı ve verimli çalışır
- Büyük veri yapılarıyla başa çıkabilir
- Minimum Spanning Tree gibi algoritmalarla kolayca entegre olur

## Dezavantajları

- Sadece bağlantı ve birleşme işlemleri yapılabilir
- Karmaşık veri yapısı kavramları yeni başlayanlar için zor olabilir

## C++ Örnek Kod

#include <iostream>
#include <vector>

using namespace std;

class UnionFind {
private:
    vector<int> parent, rank; // Her eleman için bir 'parent' (kok) ve 'rank' (derinlik) tutuyoruz.

public:
    // Yapıcı fonksiyon: Union-Find veri yapısını başlatıyoruz. Her eleman kendi kümesinin temsilcisidir.
    UnionFind(int n) {
        parent.resize(n); // 'n' tane eleman için bir parent dizisi oluşturuyoruz.
        rank.resize(n, 0); // Her eleman için başlangıçta 0 derinliğiyle rank dizisi oluşturuyoruz.
        for (int i = 0; i < n; i++)
            parent[i] = i; // Başlangıçta her eleman kendi kendisinin köküdür.
    }

    // 'Find' fonksiyonu: Bu fonksiyon, bir elemanın hangi kümeye ait olduğunu bulmamıza yardımcı olur.
    int find(int x) {
        if (parent[x] != x) // Eğer 'x' kendisiyle aynı değere sahip değilse, yani kendi kökü değilse
            parent[x] = find(parent[x]); // Rekürsif olarak üst kümenin kökünü bulup, bu elemanı doğrudan köke bağlarız (yol sıkıştırma).
        return parent[x]; // Sonunda, kökü döndürüyoruz.
    }

    // 'Union' fonksiyonu: İki elemanın ait olduğu kümeleri birleştirmek için kullanılır.
    void unionSets(int x, int y) {
        int rootX = find(x); // x elemanının kökünü buluyoruz.
        int rootY = find(y); // y elemanının kökünü buluyoruz.
        if (rootX == rootY) return; // Eğer zaten aynı kümeye aitlerse, birleştirmeye gerek yoktur.

        // Kümeleri birleştirme işlemi. 'Union by Rank' ile, daha derin olan kümeyi diğerinin kökü yapıyoruz.
        if (rank[rootX] < rank[rootY])
            parent[rootX] = rootY; // Eğer x'in kümesi daha sığsa, x'in kökünü y'nin köküne bağlıyoruz.
        else if (rank[rootX] > rank[rootY])
            parent[rootY] = rootX; // Eğer y'nin kümesi daha sığsa, y'nin kökünü x'in köküne bağlıyoruz.
        else {
            parent[rootY] = rootX; // Eğer her iki küme aynı derinlikte ise, biri kök olacak, diğeri bağlı olacak.
            rank[rootX]++; // x'in derinliğini arttırıyoruz.
        }
    }

    // 'Connected' fonksiyonu: x ve y'nin aynı kümeye ait olup olmadığını kontrol eder.
    bool connected(int x, int y) {
        return find(x) == find(y); // Eğer x ve y'nin kökleri aynıysa, bu iki eleman aynı kümeye aittir.
    }
};

int main() {
    UnionFind uf(10); // 10 elemanlık bir Union-Find veri yapısı oluşturuyoruz.

    // Küme birleştirme işlemleri
    uf.unionSets(1, 2); // 1 ve 2'yi aynı kümeye dahil ediyoruz.
    uf.unionSets(2, 3); // 2 ve 3'ü de aynı kümeye bağlıyoruz.
    uf.unionSets(4, 5); // 4 ve 5'i birbirine bağlıyoruz.

    // Bağlantı kontrolü
    cout << "1 ve 3 bağlı mı? " << (uf.connected(1, 3) ? "Evet" : "Hayır") << "\n";
    cout << "3 ve 5 bağlı mı? " << (uf.connected(3, 5) ? "Evet" : "Hayır") << "\n";

    return 0;
}
## Kaynaklar
CLRS - Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein)

Wikipedia - Union-Find

GeeksforGeeks - Union-Find Algorithm

Competitive Programming Books (For example, Steven Halim's "Competitive Programming 3")
