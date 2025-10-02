import random

# --- 1. PARAMETER UTAMA ---
KARYAWAN = [f"Karyawan_{i+1}" for i in range(10)]
JUMLAH_HARI = 14
SHIFT_CHOICES = ['P', 'S', 'M', 'L']

# Parameter Algoritma Genetika
UKURAN_POPULASI = 300
JUMLAH_GENERASI = 1000
TINGKAT_MUTASI_DASAR = 0.01
TINGKAT_CROSSOVER = 0.9
UKURAN_TURNAMEN = 5
JUMLAH_ELIT = int(UKURAN_POPULASI * 0.05)
STAGNATION_PATIENCE = 50

# --- 2. FUNGSI-FUNGSI ALGORITMA GENETIKA ---

def buat_individu():
    return [[random.choice(SHIFT_CHOICES) for _ in range(JUMLAH_HARI)] for _ in range(len(KARYAWAN))]

def hitung_fitness(jadwal):
    penalti = 0
    for hari in range(JUMLAH_HARI):
        shift_harian = [jadwal[k][hari] for k in range(len(KARYAWAN))]
        if shift_harian.count('P') < 2: penalti += 100
        if shift_harian.count('S') < 2: penalti += 100
        if shift_harian.count('M') < 2: penalti += 100
    for idx_karyawan in range(len(KARYAWAN)):
        jadwal_karyawan = jadwal[idx_karyawan]
        if jadwal_karyawan.count('L') < 4:
            penalti += 50 * (4 - jadwal_karyawan.count('L'))
        for hari in range(JUMLAH_HARI - 1):
            if jadwal_karyawan[hari] == 'M' and jadwal_karyawan[hari + 1] == 'P':
                penalti += 10
        if 'LL' not in "".join(jadwal_karyawan):
            penalti += 5
    return -penalti

def seleksi_turnamen(populasi_berfitness):
    peserta_turnamen = random.sample(populasi_berfitness, UKURAN_TURNAMEN)
    peserta_turnamen.sort(key=lambda x: x['fitness'], reverse=True)
    return peserta_turnamen[0]['individu']

def crossover(induk1, induk2):
    if random.random() > TINGKAT_CROSSOVER:
        return induk1[:], induk2[:]
    anak1, anak2 = [], []
    for i in range(len(induk1)):
        if random.random() < 0.5:
            anak1.append(induk1[i])
            anak2.append(induk2[i])
        else:
            anak1.append(induk2[i])
            anak2.append(induk1[i])
    return anak1, anak2

def mutasi(jadwal, mutation_rate):
    for idx_karyawan in range(len(jadwal)):
        if random.random() < mutation_rate:
            idx_hari = random.randint(0, JUMLAH_HARI - 1)
            jadwal[idx_karyawan][idx_hari] = random.choice(SHIFT_CHOICES)
    return jadwal

def cetak_jadwal(jadwal, nama_karyawan_list):
    print("-" * (12 + JUMLAH_HARI * 4))
    header = "Karyawan".ljust(12) + "".join([f"H{i+1:<4}" for i in range(JUMLAH_HARI)])
    print(header)
    print("-" * (12 + JUMLAH_HARI * 4))
    for i, nama_karyawan in enumerate(nama_karyawan_list):
        baris = f"{nama_karyawan:<12}" + "".join([f"{shift:<4}" for shift in jadwal[i]])
        print(baris)
    print("-" * (12 + JUMLAH_HARI * 4))

# --- 3. PROGRAM UTAMA ---
def jalankan_optimasi(daftar_karyawan):  # <-- PERUBAHAN 1: Terima argumen
    populasi = [buat_individu() for _ in range(UKURAN_POPULASI)]
    jadwal_terbaik_global = None
    fitness_terbaik_global = -float('inf')
    stagnant_counter = 0
    current_mutation_rate = TINGKAT_MUTASI_DASAR

    print("Memulai proses optimasi Algoritma Genetika...")
    for gen in range(JUMLAH_GENERASI):
        populasi_berfitness = [{"individu": ind, "fitness": hitung_fitness(ind)} for ind in populasi]
        populasi_berfitness.sort(key=lambda x: x['fitness'], reverse=True)
        
        if populasi_berfitness[0]['fitness'] > fitness_terbaik_global:
            fitness_terbaik_global = populasi_berfitness[0]['fitness']
            jadwal_terbaik_global = populasi_berfitness[0]['individu']
            stagnant_counter = 0
            current_mutation_rate = TINGKAT_MUTASI_DASAR
        else:
            stagnant_counter += 1

        if stagnant_counter >= STAGNATION_PATIENCE:
            print(f"INFO: Stagnasi terdeteksi di generasi {gen+1}. Meningkatkan mutasi!")
            current_mutation_rate = 0.1
            stagnant_counter = 0

        print(f"Generasi {gen+1:04d}/{JUMLAH_GENERASI} | Fitness Terbaik: {fitness_terbaik_global: <5} | Mutasi: {current_mutation_rate:.2f}")

        if fitness_terbaik_global == 0:
            print("\nSOLUSI OPTIMAL (PENALTI 0) DITEMUKAN!")
            break
            
        populasi_baru = []
        elit = [d['individu'] for d in populasi_berfitness[:JUMLAH_ELIT]]
        populasi_baru.extend(elit)

        while len(populasi_baru) < UKURAN_POPULASI:
            induk1 = seleksi_turnamen(populasi_berfitness)
            induk2 = seleksi_turnamen(populasi_berfitness)
            anak1, anak2 = crossover(induk1, induk2)
            populasi_baru.append(mutasi(anak1, current_mutation_rate))
            if len(populasi_baru) < UKURAN_POPULASI:
                populasi_baru.append(mutasi(anak2, current_mutation_rate))
        
        populasi = populasi_baru

    print("\n--- PROSES SELESAI ---")
    print("JADWAL TERBAIK YANG DITEMUKAN:")
    cetak_jadwal(jadwal_terbaik_global, daftar_karyawan)  # <-- PERUBAHAN 2: Gunakan argumen
    print(f"SKOR FITNESS AKHIR (Total Penalti): {fitness_terbaik_global}")

# Jalankan program utama
if __name__ == "__main__":
    jalankan_optimasi(KARYAWAN)  # <-- PERUBAHAN 3: Kirim variabel KARYAWAN