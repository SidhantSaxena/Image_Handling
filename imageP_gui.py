import os
import subprocess
import sys
from tkinter import messagebox
from tkinter import *


# reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
# installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
# if 'numpy' not in installed_packages:
#     os.system('cmd /c "pip install numpy"')
# if 'image' not in installed_packages:
#     os.system('cmd /c "pip install image"')
# if 'pandas' not in installed_packages:
#     os.system('cmd /c "pip install image"')


import PIL.Image
from PIL import ImageEnhance, Image
import numpy as np
import pandas as pd

np.set_printoptions(threshold=np.inf)

im = NONE
im2 = NONE

try:
    def open_ima(mag):
        global im
        try:
            try:
                im = PIL.Image.open(str(mag.get()) + '.jpg')
                print("Image Opened")

            except:
                im = PIL.Image.open(mag.get() + '.png')
                print("Image Opened")
        except:
            try:
                im = PIL.Image.open(mag.get() + '.jpeg')
                print("Image Opened")
            except:
                messagebox.showinfo("Error", "Does not exists")
                exit(0)


    def bin_img():
        global im
        print("*Note:Make sure that, the image uploaded consists of only pure white and pure black intensities")
        rgb_im = im.convert('L')
        width, height = im.size
        i, j = (0, 0)
        bin_ = []
        for w in range(height):
            i = 0
            for h in range(width):
                pix = rgb_im.getpixel((h, w))
                if pix != 0:
                    pix = 1
                bin_.append(pix)
        bin_ = np.array(bin_)
        bin_ = bin_.reshape(height,width)
        bin_dta = pd.DataFrame(bin_)
        bin_dta.columns = [str(i) + " pix" for i in range(1, width + 1)]
        bin_dta.index = [str(j) + " pix" for j in range(1, height + 1)]
        writer = pd.ExcelWriter('Binary_Data.xlsx')
        bin_dta.to_excel(writer, "Binary")
        writer.save()
        messagebox.showinfo("Notice", "Operation Completed")


    def RRgb():
        global im
        global im2
        rgb_im = im.convert('RGB')
        width, height = im.size
        i, j = (0, 0)
        rc, gc, bc = [], [], []
        for w in range(width):
            for h in range(height):
                r, g, b = rgb_im.getpixel((w, h))
                rc.append(r)
                gc.append(g)
                bc.append(b)
        rc = np.array(rc)
        gc = np.array(gc)
        bc = np.array(bc)
        rc = rc.reshape(height, width)
        gc = gc.reshape(height, width)
        bc = np.reshape(bc, (height, width))
        rc_dta = pd.DataFrame(rc)
        bc_dta = pd.DataFrame(bc)
        gc_dta = pd.DataFrame(gc)
        rc_dta.columns = [str(i) + " pix" for i in range(1, width + 1)]
        rc_dta.index = [str(j) + " pix" for j in range(1, height + 1)]
        gc_dta.columns = [str(i) + " pix" for i in range(1, width + 1)]
        gc_dta.index = [str(j) + " pix" for j in range(1, height + 1)]
        bc_dta.columns = [str(i) + " pix" for i in range(1, width + 1)]
        bc_dta.index = [str(j) + " pix" for j in range(1, height + 1)]
        writer = pd.ExcelWriter('RGB_Data.xlsx')
        rc_dta.to_excel(writer, "Red_Channel")
        gc_dta.to_excel(writer, "Green_Channel")
        bc_dta.to_excel(writer, "Blue_Channel")
        writer.save()
        messagebox.showinfo("Notice", "Operation Completed")


    def gray_C():
        global im
        gr = []
        rgb_im = im.convert('L')
        width, height = im.size
        i, j = (0, 0)
        for w in range(width):
            i = 0
            for h in range(height):
                gr.append(rgb_im.getpixel((w, h)))
        gr = np.array(gr)
        gr = np.reshape(gr, (height,width))
        gc_dta = pd.DataFrame(gr)
        gc_dta.columns = [i for i in range(1, width + 1)]
        gc_dta.index = [j for j in range(1, height + 1)]
        writer = pd.ExcelWriter('GrayScale_Data.xlsx')
        gc_dta.to_excel(writer, "GrayScale")
        writer.save()
        messagebox.showinfo("Notice", "Operation Completed")
        os.system("GrayScale_Data.xlsx")

    def Enha_con(scale, name):
        global im
        contrast = ImageEnhance.Contrast(im)
        scale = float(scale.get())
        contrast.enhance(scale).save(name.get() + '.jpg')
        messagebox.showinfo("Notice", "Operation Completed")
        os.system(name.get() + '.jpg')


    def Enha():
        sec_win = Tk()
        Label(sec_win, text="Enhance Image").grid(row=0, column=1, padx=5, pady=5)
        Label(sec_win, text="Scale factor").grid(row=1, column=0, padx=5, pady=5)
        scale = Entry(sec_win, width=50, borderwidth=5)
        scale.grid(row=1, column=1, padx=5, pady=5)
        Label(sec_win, text="Name of the new Image").grid(row=2, column=0)
        name = Entry(sec_win, width=50, borderwidth=5)
        name.grid(row=2, column=1, padx=5, pady=5)
        en = Button(sec_win, text="Convert and Save", command=lambda: Enha_con(scale, name))
        en.grid(row=3, column=2, padx=5, pady=5)
        sec_win.mainloop()


    def altering_(perc, name):
        global im
        basewidth = int(float(im.size[0]) + (float(im.size[0])) * float(float(perc.get()) / 100))
        wpercent = (basewidth / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        img = im.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save(name.get() + '.jpg')
        messagebox.showinfo("Notice", "Operation Completed")
        os.system(name.get() + '.jpg')


    def alterD():
        prox_win = Tk()
        Label(prox_win, text="Alter Image Dimension").grid(row=0, column=1, padx=5, pady=5)
        Label(prox_win, text="*For reduction use '-'<percentage desired>").grid(row=1, column=1, padx=5, pady=5)
        Label(prox_win, text="Enter Alter Percentage").grid(row=2, column=0, padx=5, pady=5)
        perc = Entry(prox_win, width=50, borderwidth=5)
        perc.grid(row=2, column=1, padx=5, pady=5)
        Label(prox_win, text="Name of the new Image").grid(row=3, column=0, padx=5, pady=5)
        name = Entry(prox_win, width=50, borderwidth=5)
        name.grid(row=3, column=1, padx=5, pady=5)
        at = Button(prox_win, text="Alter and Save", command=lambda: altering_(perc, name))
        at.grid(row=4, column=2, padx=5, pady=5)
        prox_win.mainloop()


    def makeImage(name,newname):
        edf = pd.read_excel(name.get()+".xlsx")
        edr,edc=edf.shape
        print(edr,edc)
        mat = edf.iloc[:, 1:].values
        pix = mat.reshape(edr, edc-1)
        matim= np.array(pix, dtype=np.uint8)
        img2 = Image.fromarray(matim)
        img2.save(newname.get()+".jpg")
        os.system(newname.get()+".jpg")


    def convertMat():
        sec_win = Tk()
        Label(sec_win, text="Image Generate").grid(row=0, column=1, padx=5, pady=5)
        Label(sec_win, text="Name of the file").grid(row=1, column=0, padx=5, pady=5)
        name = Entry(sec_win, width=50, borderwidth=5)
        name.grid(row=1, column=1, padx=5, pady=5)
        Label(sec_win, text="Name of the new Image").grid(row=2, column=0)
        newname = Entry(sec_win, width=50, borderwidth=5)
        newname.grid(row=2, column=1, padx=5, pady=5)
        en = Button(sec_win, text="Convert and Save", command=lambda: makeImage(name, newname))
        en.grid(row=3, column=2, padx=5, pady=5)
        sec_win.mainloop()


    if __name__ == "__main__":
        main_wind = Tk()
        Label(main_wind, text="Image Processing").grid(row=0, column=1, padx=5, pady=8)
        Label(main_wind, text="Enter Image Name").grid(row=1, column=0, padx=5, pady=7)
        mag = Entry(main_wind, width=50, borderwidth=5)
        mag.grid(row=1, column=1, padx=5, pady=7)
        openB = Button(main_wind, text="Open File", command=lambda: open_ima(mag))
        openB.grid(row=1, column=2, padx=5)
        binary = Button(main_wind, text="Binary Conversion", command=bin_img)
        binary.grid(row=2, column=0, padx=5, pady=5)
        rgbc = Button(main_wind, text="RGB Conversion", command=RRgb)
        rgbc.grid(row=2, column=1, padx=5, pady=5)
        grayS = Button(main_wind, text="GrayScale Conversion", command=gray_C)
        grayS.grid(row=3, column=0, padx=5, pady=5)
        enhan = Button(main_wind, text="Enhance Image", command=Enha)
        enhan.grid(row=3, column=1, padx=5, pady=5)
        dimension = Button(main_wind, text="Alter Dimension", command=alterD)
        dimension.grid(row=4, column=0, padx=5, pady=5)
        mattoimg = Button(main_wind, text="Matrix into Image", command=convertMat)
        mattoimg.grid(row=4, column=2, padx=5, pady=5)
        ex = Button(main_wind, text="Exit", command=exit)
        ex.grid(row=4, column=1, padx=5, pady=5)
        main_wind.mainloop()
except:
    print("")