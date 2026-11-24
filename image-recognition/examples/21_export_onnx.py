"""Offline executable teaching example; run from this directory."""
import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import onnx
import onnxruntime as ort
import torch
from vision_core import TinyClassifier,artifact_contract,seed_everything,train_classifier,print_json

def export_and_compare(folder,model=None):
    seed_everything();model=TinyClassifier().eval() if model is None else model.eval()
    Path(folder).mkdir(parents=True,exist_ok=True)
    path=Path(folder)/'classifier.onnx'
    torch.onnx.export(model,(torch.zeros(2,3,24,24),),str(path),
        input_names=['images'],output_names=['logits'],dynamo=True,opset_version=18,
        dynamic_shapes={'x':{0:torch.export.Dim('batch',min=1,max=8)}},external_data=False)
    onnx.checker.check_model(onnx.load(path))
    session=ort.InferenceSession(str(path),providers=['CPUExecutionProvider'])
    errors=[]
    for batch in [1,3,8]:
        x=torch.rand(batch,3,24,24)
        with torch.inference_mode():reference=model(x).numpy()
        actual=session.run(['logits'],{'images':x.numpy()})[0]
        np.testing.assert_allclose(actual,reference,rtol=1e-4,atol=1e-5)
        errors.append(float(np.max(np.abs(actual-reference))))
    manifest=artifact_contract(path)
    (Path(folder)/'contract.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return {'batches':[1,3,8],'max_errors':errors,'contract':manifest}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--trained',action='store_true',help='Train the original synthetic classifier before export')
    args=parser.parse_args();model=None;training=None
    if args.trained:model,training=train_classifier()
    if args.output:report=export_and_compare(args.output,model)
    else:
        with TemporaryDirectory() as folder:report=export_and_compare(folder,model)
    print_json(dict(trained=args.trained,training=training,**report))

if __name__=='__main__': main()
