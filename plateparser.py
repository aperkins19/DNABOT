import tkinter as tk

def parseplate(csvname, samplewells, final_conc):
    
    import pandas as pd
    import numpy as np
    from scipy import stats
    
    final_conc = 0.3
    final_conc = final_conc/2
    standard_curve_concs = [1]
    dilution_factor = 1/((final_conc)**(1/6))

    for i in range(6):
        standard_curve_concs.append(standard_curve_concs[i]/dilution_factor)
    standard_curve_concs.append(0)

    df = pd.read_csv(csvname + ".csv", header=11)
    plate_data = df.iloc[:8, 0:13]
    plate_data = plate_data.set_index('Unnamed: 0')
    plate_data = plate_data.rename_axis("")   
    slope, intercept, r_value, p_value, std_err = stats.linregress(standard_curve_concs, plate_data.loc[:,"12"])
    wellresults = {}
    for well in samplewells:
        wellresults[well] = round((float(plate_data.loc[well[0], well[1:]])-intercept)/slope, 3)
    
    wellresultsdf = pd.DataFrame(wellresults, index=["Result"])
    wellresultsdf.to_csv(csvname + "_results.csv")
    return wellresults

def run_parseplate():
    wellresults = parseplate(e1.get(), e2.get().split(","), float(e3.get()))
    print (wellresults)
    res = tk.Text(master, height=2, width=30)
    res.grid(row=4, column=0, columnspan = 2)
    res.insert(tk.END, wellresults)

    

master = tk.Tk()
tk.Label(master, 
         text="CSVname").grid(row=0)
tk.Label(master, 
         text="Sample Wells").grid(row=1)
tk.Label(master, 
         text="Final Conc").grid(row=2)


e1 = tk.Entry(master)
e1.insert(10, "plate_reader_template")
e2 = tk.Entry(master)
e2.insert(10, "A1,B1,C1,D1")
e3 = tk.Entry(master)
e3.insert(10, "0.03")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

tk.Button(master, 
          text='Calculate', command=run_parseplate).grid(row=3, column=1, pady=4)

tk.mainloop()