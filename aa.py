import random
import numpy as np

KARYAWAN = ["Andi", "Budi", "Cici", "Dedi", "Eka", "Fani"]
JUMLAH_HARI = 100
SHIFTS = ["Pagi", "Siang", "Malam"]
KARYAWAN_PER_SHIFT = 1

UKURAN_POPULASI = 1000
JUMLAH_GENERASI = 2
LAJU_MUTASI = 0.1
UKURAN_TURNAMEN = 5
JUMLAH_ELIT = 1

def buat_individu():
    """Membuat satu individu (jadwal) secara acak."""
    jadwal = np.full((JUMLAH_HARI, len(SHIFTS)), -1, dtype=int)
    for hari in range(JUMLAH_HARI):
        karyawan_hari_ini = random.sample(range(len(KARYAWAN)), len(SHIFTS) * KARYAWAN_PER_SHIFT)
        jadwal[hari] = karyawan_hari_ini
    return jadwal.tolist()

def hitung_fitness(individu):
    """
    Menghitung skor fitness sebuah jadwal.
    Skor awal adalah 1000, lalu dikurangi penalti untuk setiap pelanggaran.
    Semakin tinggi skor, semakin bagus jadwalnya.
    """
    penalti = 0

    shift_counts = {i: 0 for i in range(len(KARYAWAN))}
    for hari in individu:
        for shift in hari:
            shift_counts[shift] += 1
    penalti += np.std(list(shift_counts.values())) * 50

    for i in range(JUMLAH_HARI - 1):
        jadwal_hari_ini = individu[i]
        jadwal_besok = individu[i+1]
        karyawan_shift_malam = jadwal_hari_ini[SHIFTS.index("Malam")]
        karyawan_shift_pagi_besok = jadwal_besok[SHIFTS.index("Pagi")]
        if karyawan_shift_malam == karyawan_shift_pagi_besok:
            penalti += 100

    return max(0, 1000 - penalti)



def seleksi_turnamen(populasi, fitnesses):
    """Memilih satu individu menggunakan metode seleksi turnamen."""
    turnamen = random.sample(list(zip(populasi, fitnesses)), UKURAN_TURNAMEN)
    pemenang = max(turnamen, key=lambda x: x[1])
    return pemenang[0]

def crossover(parent1, parent2):
    """
    Melakukan pindah silang (single-point crossover) antara dua parent.
    Titik potong adalah hari.
    """
    child1, child2 = parent1[:], parent2[:]
    titik_potong = random.randint(1, JUMLAH_HARI - 1)
    
    child1 = parent1[:titik_potong] + parent2[titik_potong:]
    child2 = parent2[:titik_potong] +    parent1[titik_potong:]
    
    return child1, child2

def mutasi(individu):
    """
    Melakukan mutasi dengan menukar jadwal dua karyawan pada hari dan shift acak.
    """
    jadwal_mutasi = [list(hari) for hari in individu]
    if random.random() < LAJU_MUTASI:
        hari = random.randint(0, JUMLAH_HARI - 1)
        shift1, shift2 = random.sample(range(len(SHIFTS)), 2)
        
        karyawan1 = jadwal_mutasi[hari][shift1]
        karyawan2 = jadwal_mutasi[hari][shift2]
        jadwal_mutasi[hari][shift1] = karyawan2
        jadwal_mutasi[hari][shift2] = karyawan1
        
    return jadwal_mutasi

def jalankan_ga():
    """Fungsi utama untuk menjalankan seluruh proses algoritma genetika."""
    populasi = [buat_individu() for _ in range(UKURAN_POPULASI)]
    
    best_solution_overall = None
    best_fitness_overall = -1

    print("Memulai proses optimasi penjadwalan...\n")

    for gen in range(JUMLAH_GENERASI):
        fitnesses = [hitung_fitness(individu) for individu in populasi]
        
        best_fitness_gen = max(fitnesses)
        if best_fitness_gen > best_fitness_overall:
            best_fitness_overall = best_fitness_gen
            best_solution_overall = populasi[fitnesses.index(best_fitness_gen)]
            
        print(f"Generasi {gen+1:03d} | Fitness Terbaik: {best_fitness_overall:.2f}")

        populasi_baru = []
        sorted_population = sorted(zip(populasi, fitnesses), key=lambda x: x[1], reverse=True)
        for i in range(JUMLAH_ELIT):
            populasi_baru.append(sorted_population[i][0])

        while len(populasi_baru) < UKURAN_POPULASI:
            parent1 = seleksi_turnamen(populasi, fitnesses)
            parent2 = seleksi_turnamen(populasi, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            populasi_baru.append(mutasi(child1))
            if len(populasi_baru) < UKURAN_POPULASI:
                populasi_baru.append(mutasi(child2))
        
        populasi = populasi_baru

    return best_solution_overall

def tampilkan_jadwal_lengkap(jadwal):
    """
    Menampilkan jadwal dalam format ringkasan per hari DAN rincian per karyawan.
    """
    print("\n\n===============================================")
    print("      RINGKASAN JADWAL KERJA OPTIMAL")
    print("===============================================")
    
    header = f"{'Hari':<10}"
    for shift in SHIFTS:
        header += f"| {shift:<10}"
    print(header)
    print("-" * len(header))
    
    hari_nama = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    for i, hari in enumerate(jadwal):
        row = f"{hari_nama[i]:<10}"
        for karyawan_id in hari:
            row += f"| {KARYAWAN[karyawan_id]:<10}"
        print(row)

    print("\n--- Analisis Jadwal ---")
    fitness_final = hitung_fitness(jadwal)
    print(f"Skor Fitness Final: {fitness_final:.2f}")

    shift_counts = {k: 0 for k in KARYAWAN}
    for hari in jadwal:
        for karyawan_id in hari:
            shift_counts[KARYAWAN[karyawan_id]] += 1
    print("Total Shift per Karyawan:")
    for karyawan, total in shift_counts.items():
        print(f"- {karyawan}: {total} shift")
    
    std_dev = np.std(list(shift_counts.values()))
    print(f"Distribusi Beban Kerja (StDev): {std_dev:.2f} (semakin kecil semakin baik)")

if __name__ == "__main__":
    jadwal_terbaik = jalankan_ga()
    tampilkan_jadwal_lengkap(jadwal_terbaik)