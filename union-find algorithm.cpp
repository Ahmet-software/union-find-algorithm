#include <iostream>
#include <vector>

using namespace std;

class UnionFind {
private:
    vector<int> parent, rank; // Her eleman için bir 'parent' (kok) ve 'rank' (derinlik) tutuyoruz.

public:
    // Yapici fonksiyon: Union-Find veri yapisini baslatiyoruz. Her eleman kendi kümesinin temsilcisidir.
    UnionFind(int n) {
        parent.resize(n); // 'n' tane eleman için bir parent dizisi olusturuyoruz.
        rank.resize(n, 0); // Her eleman için baslangicta 0 derinligiyle rank dizisi olusturuyoruz.
        for(int i = 0; i < n; i++)
            parent[i] = i; // Baslangicta her eleman kendi kendisinin kokudur.
    }

    // 'Find' fonksiyonu: Bu fonksiyon, bir elemanin hangi kümeye ait oldugunu bulmamiza yardimci olur.
    int find(int x) {
        if(parent[x] != x) // Eger 'x' kendisiyle ayni degere sahip degilse, yani kendi koku degilse
            parent[x] = find(parent[x]); // Rekursif olarak üst kümenin kokunu bulup, bu elemani dogrudan koke baglariz (yol sikistirma).
        return parent[x]; // Sonunda, koku döndürüyoruz.
    }

    // 'Union' fonksiyonu: Iki elemanin ait oldugu kümeleri birlestirmek için kullanilir.
    void unionSets(int x, int y) {
        int rootX = find(x); // x elemaninin kokunu buluyoruz.
        int rootY = find(y); // y elemaninin kokunu buluyoruz.
        if(rootX == rootY) return; // Eger zaten ayni kümeye aitlerse, birlestirmeye gerek yoktur.

        // Kümeleri birlestirme islemi. 'Union by Rank' ile, daha derin olan kümeyi digerinin koku yapýyoruz.
        if(rank[rootX] < rank[rootY])
            parent[rootX] = rootY; // Eger x'in kümesi daha sigysa, x'in kokunu y'nin kokuna baglariyoruz.
        else if(rank[rootX] > rank[rootY])
            parent[rootY] = rootX; // Eger y'nin kümesi daha sigysa, y'nin kokunu x'in kokuna baglariyoruz.
        else {
            parent[rootY] = rootX; // Eger her iki küme ayni derinlikte ise, biri kok olacak, digeri bagli olacak.
            rank[rootX]++; // x'in derinligini arttiriyoruz.
        }
    }

    // 'Connected' fonksiyonu: x ve y'nin ayni kümeye ait olup olmadigini kontrol eder.
    bool connected(int x, int y) {
        return find(x) == find(y); // Eger x ve y'nin kokleri ayniysa, bu iki eleman ayni kümeye aittir.
    }
};

int main() {
    UnionFind uf(10); // 10 elemanlik bir Union-Find veri yapisi olusturuyoruz.

    // Küme birlestirme islemleri
    uf.unionSets(1, 2); // 1 ve 2'yi ayni kümeye dahil ediyoruz.
    uf.unionSets(2, 3); // 2 ve 3'ü de ayni kümeye bagliyoruz.
    uf.unionSets(4, 5); // 4 ve 5'i birbirine bagliyoruz.

    // Baglanti kontrolü
    cout << "1 ve 3 bagli mi? " << (uf.connected(1, 3) ? "Evet" : "Hayir") << "\n";
    cout << "3 ve 5 bagli mi? " << (uf.connected(3, 5) ? "Evet" : "Hayir") << "\n";

    return 0;
}
