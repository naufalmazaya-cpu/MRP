import pandas as pd
import math

def generate_eoq_mrp_with_cost():
    # --- 1. INPUT DATA & PARAMETER ---
    gross_requirements_p1_p6 = [100, 50, 150, 80, 120, 60]
    
    # Parameter Biaya
    cost_per_order = 500      # (S) Setup Cost per pesanan
    holding_cost_per_unit = 5 # (H) Holding Cost per unit/periode
    
    # Parameter MRP
    initial_inventory = 50    
    lead_time = 1             
    
    # --- 2. HITUNG EOQ (Q*) ---
    avg_demand = sum(gross_requirements_p1_p6) / len(gross_requirements_p1_p6)
    eoq_q = round(math.sqrt((2 * avg_demand * cost_per_order) / holding_cost_per_unit))
    
    # --- 3. PERSIAPAN DATA TABEL ---
    periods = [f"P{i}" for i in range(0, 7)]
    gross_req = [0] + gross_requirements_p1_p6
    scheduled_rec = [0] * 7
    beg_inv = [0] * 7
    end_inv = [0] * 7
    planned_rec = [0] * 7
    planned_rel = [0] * 7

    # --- 4. LOGIKA MRP ---
    current_inv = initial_inventory
    for i in range(1, 7):
        beg_inv[i] = current_inv
        if (beg_inv[i] + scheduled_rec[i]) < gross_req[i]:
            planned_rec[i] = eoq_q
        
        end_inv[i] = beg_inv[i] + scheduled_rec[i] + planned_rec[i] - gross_req[i]
        current_inv = end_inv[i]

    # Logika Lead Time
    for i in range(1, 7):
        if planned_rec[i] > 0:
            if i - lead_time >= 0:
                planned_rel[i - lead_time] = planned_rec[i]

    # --- 5. PERHITUNGAN TOTAL COST ---
    # Hitung berapa kali kita pesan (Planned Order Release > 0)
    num_orders = sum(1 for x in planned_rel if x > 0)
    total_setup_cost = num_orders * cost_per_order
    
    # Hitung total stok yang disimpan (Ending Inventory P1 - P6)
    total_inventory_held = sum(end_inv[1:]) 
    total_holding_cost = total_inventory_held * holding_cost_per_unit
    
    total_cost = total_setup_cost + total_holding_cost

    # --- 6. OUTPUT ---
    data = {
        'Gross Requirement': gross_req,
        'Scheduled Receipt': scheduled_rec,
        'Beginning Inventory': [0] + beg_inv[1:],
        'Ending Inventory': [initial_inventory] + end_inv[1:],
        'Planned Order Receipt': planned_rec,
        'Planned Order Release': planned_rel
    }
    
    df = pd.DataFrame(data, index=periods).T
    
    print("="*60)
    print(f"{'HASIL ANALISIS LOT SIZING: EOQ':^60}")
    print("="*60)
    print(df.to_string())
    print("-"*60)
    print(f"HASIL PERHITUNGAN BIAYA:")
    print(f"1. Total Setup Cost  : {num_orders} pesanan x {cost_per_order}  = {total_setup_cost}")
    print(f"2. Total Holding Cost: {total_inventory_held} unit x {holding_cost_per_unit}    = {total_holding_cost}")
    print("-"*60)
    print(f"TOTAL COST           : {total_cost}")
    print("="*60)

if __name__ == "__main__":
    generate_eoq_mrp_with_cost()
