"""Generate synthetic documents, not external user data or copyrighted samples."""
from pathlib import Path
import io,json,math,struct,wave
import pymupdf
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent

def create(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    doc=pymupdf.open();page=doc.new_page(width=612,height=792)
    for xy,text,size in [((48,60),'DOCWEAVE INVOICE',19),((48,94),'Invoice: DW-2026-001',12),((48,118),'Date: 2026-11-20',12),((48,142),'Vendor: Harbor Labs',12),((48,166),'Currency: USD',12)]:page.insert_text(xy,text,fontsize=size)
    columns=[48,280,350,440,560];ys=[210,242,274,306]
    for x in columns:page.draw_line((x,ys[0]),(x,ys[-1]),width=.7)
    for y in ys:page.draw_line((columns[0],y),(columns[-1],y),width=.7)
    for y,row in zip([231,263,295],[['Item','Qty','Unit','Amount'],['Cable','2','12.50','25.00'],['Adapter','1','20.00','20.00']]):
        for x,text in zip(columns,row):page.insert_text((x+8,y),text,fontsize=12)
    for y,text in [(350,'Subtotal: 45.00'),(376,'Tax: 2.25'),(402,'Total: 47.25')]:page.insert_text((350,y),text,fontsize=12)
    page.insert_text((48,470),'Terms: Net 30. Bank details: not provided.',fontsize=11)
    page.insert_text((48,510),'Contact: demo@example.test',fontsize=11)
    page=doc.new_page(width=612,height=792)
    for xy,text in [((48,60),'DOCUMENT NOTES'),((48,110),'LEFT COLUMN'),((48,140),'A: Delivery within 7 days.'),((48,170),'B: Warranty is 12 months.'),((330,110),'RIGHT COLUMN'),((330,140),'C: Inspect before payment.'),((330,170),'D: Keep the source page.')]:page.insert_text(xy,text,fontsize=12)
    doc.set_metadata({'title':'Synthetic DocWeave fixture','author':'Learning Notes'})
    doc.save(directory/'invoice.pdf',garbage=4,deflate=True,no_new_id=True)
    pix=doc[0].get_pixmap(dpi=144,alpha=False);pix.save(directory/'scan.png')
    scan=pymupdf.open();scan.new_page(width=612,height=792).insert_image(pymupdf.Rect(0,0,612,792),stream=pix.tobytes('png'));scan.save(directory/'scan.pdf',deflate=True,no_new_id=True);scan.close()
    rotated=pymupdf.open();rotated.insert_pdf(doc,from_page=0,to_page=0);rotated[0].set_rotation(90);rotated.save(directory/'rotated.pdf',no_new_id=True);rotated.close();doc.close()
    form=pymupdf.open();fp=form.new_page(width=612,height=792);widget=pymupdf.Widget();widget.field_name='vendor';widget.field_type=pymupdf.PDF_WIDGET_TYPE_TEXT;widget.field_value='Harbor Labs';widget.rect=pymupdf.Rect(60,80,300,110);fp.add_widget(widget);form.save(directory/'form.pdf',no_new_id=True);form.close()
    payload={'invoice_no':'DW-2026-001','currency':'USD','subtotal_cents':4500,'tax_cents':225,'total_cents':4725}
    (directory/'expected.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    (directory/'transcript.json').write_text(json.dumps({'origin':'manually-authored transcript fixture; no ASR inference','segments':[{'start_ms':0,'end_ms':1500,'text':'Inspect invoice.'},{'start_ms':1500,'end_ms':3000,'text':'Confirm total.'}]},indent=2)+'\n',encoding='utf-8')
    with wave.open(str(directory/'tones.wav'),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000)
        f.writeframes(b''.join(struct.pack('<h',int(4000*math.sin(2*math.pi*(440 if i<24000 else 660)*i/16000))) for i in range(48000)))
    frames=[]
    for i in range(4):
        im=Image.new('RGB',(320,180),'#e7eee9');d=ImageDraw.Draw(im);d.rectangle((20+i*45,65,65+i*45,110),fill='#28685f');d.text((15,15),f'Synthetic frame {i}; {i*500} ms',fill='black');frames.append(im)
    frames[0].save(directory/'timeline.gif',save_all=True,append_images=frames[1:],duration=500,loop=0)
    return directory

if __name__=='__main__':print(create(ROOT/'data'))
