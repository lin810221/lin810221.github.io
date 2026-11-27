"""Real CPU OCR using the models bundled with the pinned RapidOCR wheel."""
from pathlib import Path
from hashlib import sha256
import argparse,json

def recognize(path):
    from PIL import Image
    with Image.open(path) as image:
        if image.width*image.height>8_000_000 or getattr(image,'n_frames',1)!=1:raise ValueError('OCR lab accepts a bounded single image')
    import rapidocr
    from rapidocr import RapidOCR
    models=Path(rapidocr.__file__).parent/'models'
    files={'Det.model_path':models/'PP-OCRv6_det_small.onnx','Rec.model_path':models/'PP-OCRv6_rec_small.onnx','Cls.model_path':models/'ch_ppocr_mobile_v2.0_cls_mobile.onnx'}
    if not all(f.is_file() for f in files.values()):raise RuntimeError('Pinned bundled models missing; do not auto-download unknown replacements')
    engine=RapidOCR(params={**{k:str(v) for k,v in files.items()},'EngineConfig.onnxruntime.intra_op_num_threads':1,'EngineConfig.onnxruntime.inter_op_num_threads':1})
    result=engine(str(Path(path).resolve()))
    return {'engine':'rapidocr-3.10.0','models':{f.name:sha256(f.read_bytes()).hexdigest() for f in files.values()},'texts':list(result.txts or []),'scores':[] if result.scores is None else [float(x) for x in result.scores],'boxes':[] if result.boxes is None else result.boxes.tolist(),'coordinate_system':'top-left pixels in the supplied image; recognition score is not calibrated probability'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('image',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();result=recognize(a.image);s=json.dumps(result,ensure_ascii=False,indent=2)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s+'\n',encoding='utf-8')
    else:print(s)
