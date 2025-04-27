
; set dimension
idim  = 3600L
jdim  = 1200L

pidim = 3600L/3L
pjdim = 1200L/3L


; set data format
data    = Fltarr(idim,jdim)      + (-999.9)
t_image = Bytarr(idim,jdim)      + ( 255L)
image   = Bytarr(pidim,pjdim)    + ( 255L)
tmp     = Bytarr(idim/2L,jdim,2) + ( 255L)

; set file name
fname = './gsmap_mvk.20211201.0000.v8.0000.0.dat'

; read data
Openr, lun_r, fname, /Get_lun, /Compress
Readu, lun_r, data
Free_lun, lun_r
Close


; For drawing image
;present device name is captured.
entry_device = !D.name

;Set plot area 
Set_plot, 'Z'


;Set plot area on device
xmarg = 100
ymarg = 150

Device, Set_resolution=[pidim + xmarg*2,pjdim + ymarg*2]


;Set colors
col = {COL, white:255, black:254, gray:253}

Tvlct, 255,255,255, col.white
Tvlct, 168,168,168, col.gray
Tvlct,   0,  0,  0, col.black

!P.background = col.white

Tvlct,r,g,b,/get


color_number = 11
rain_r     = [  0,  0,  0, 51,155,255,255,255,235,175,115]
rain_g     = [  0,100,180,219,235,235,179,100, 30,  0,  0]
rain_b     = [150,255,255,128, 74,  0,  0,  0,  0,  0,  0]
scale_min  = [0.0,0.5,  1,  2,  3,  5, 10, 15, 20, 25, 30]
scale_max  = [0.5,1.0,  2,  3,  5, 10, 15, 20, 25, 30, 35]

;Set Color bar 
bar_pix   = 50
bar_xsize = bar_pix * color_number 
bar_ysize = 20
bar       = Bytarr(bar_xsize,bar_ysize) + col.gray

bar_xpos  = (xmarg*2+pidim)/2 - bar_xsize/2
bar_ypos  = ymarg/2
bar_cxpos = Intarr(color_number) + 0L

for i = 0,color_number-1 do begin
   bar_cxpos[i]  = bar_xpos + bar_pix*i
endfor

bar_cypos = Bytarr(color_number) +  ymarg/3

scale_bar = Strcompress(String(scale_min, Format='(F6.1)'), /Remove_all)


for k =0,color_number-1 do begin
   r[k] = rain_r[k]
   g[k] = rain_g[k]
   b[k] = rain_b[k]

   m = bar_pix*k
   bar[m:m+bar_pix-1,*] = Byte(k)

  index = Where((data ge scale_min[k]) and (data lt scale_max[k]), count)
  if (count gt 1 ) then t_image[index] = Byte(k)
  
endfor


index = Where(data gt scale_max[color_number-1], count )
if (count gt 1)  then t_image[index] = Byte(color_number-1) 

index = Where((data lt 0.) and (data ge -999), count )
if ( count gt 1) then t_image[index] = col.gray

index = Where(data eq 0., count )
if ( count gt 1) then t_image[index] = col.white

;Regrid for image
image = Rebin(t_image,pidim,pjdim,/sample)
image = Reverse(image,2)

tvlct,r,g,b

; Set projection
latmin =-60
latmax =60
lonmin = 0
lonmax = 360
offset = 0.05

;GSMaP

Map_set, 0, 180+offset,  /Cylindrical ,/Isotropic, $
         Color=col.white,Xmargin=10,Ymargin=10, $
         Limit=[latmin,lonmin,latmax,lonmax],/Noerase, /Noborder

result = Map_image(image, startx, starty, xsize, ysize, Compress=1, $
                   Latmin=latmin, Lonmin=lonmin, Latmax=latmax, Lonmax=lonmax)

;Draw image
Erase,col.white
Tv, result, startx, starty, Xsize=xsize, Ysize=ysize
Map_Grid,Color=col.black, Charzise=2.0, Label=1, Latalign=0., Lonalign=1.0, $
         /Box_axes
Map_Continents,Color=col.black,Thick=2,Charzise=2.0

title_m   = 'SAMPLE'
Xyouts,(xmarg*2+pidim)/2-15, ymarg+pjdim+45, title_m, Alignment=0.5, Charthick=2, Charsize=3, Color=col.black, /Device

;Draw Color scale
bar_title = '[mm/hour]'
TV, bar, bar_xpos, bar_ypos
Xyouts, bar_cxpos, bar_cypos, scale_bar, Alignment=0.5, Charsize=1, Color=col.black, /Device
Xyouts, bar_cxpos[color_number-1]+bar_pix, bar_cypos[0], bar_title, Alignment=0.0, Charsize=1, Color=col.black, /Device


;Out put PNG file
fn_png = './test.png'
Write_png,fn_png,tvrd(),r,g,b

Spawn, 'display '+ fn_png

; Set defaults
Set_plot,entry_device


end
