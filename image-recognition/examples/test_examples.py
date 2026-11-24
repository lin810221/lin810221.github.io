"""Numerical and integration acceptance tests; no downloads or external data."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np
import torch
from PIL import Image
from torchvision.ops import box_iou as official_iou, batched_nms
from torchvision import tv_tensors
from torchvision.transforms import v2
import vision_core as v

HERE=Path(__file__).resolve().parent

def module(name):
    spec=importlib.util.spec_from_file_location('cv_'+name.replace('.','_'),HERE/name)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


class GeometryTests(unittest.TestCase):
    def test_exact_overlap(self):
        self.assertAlmostEqual(float(v.box_iou([[0,0,10,10]],[[5,0,15,10]])[0,0]),1/3,places=6)

    def test_touching_not_intersection(self):
        self.assertEqual(float(v.box_iou([[0,0,1,1]],[[1,0,2,1]])[0,0]),0)

    def test_torchvision_equivalence(self):
        a=torch.tensor([[0.,0,10,10],[3,4,9,12]])
        torch.testing.assert_close(v.box_iou(a,a),official_iou(a,a))

    def test_degenerate_rejected(self):
        for b in [[[1,1,1,3]],[[4,2,1,3]],[[0,0,float('nan'),2]]]:
            with self.assertRaises(ValueError):v.validate_boxes(b)

    def test_empty_boxes(self):
        self.assertEqual(v.box_iou(torch.empty(0,4),torch.tensor([[0,0,1,1]])).shape,(0,1))

    def test_rounding_inverse(self):
        g=v.letterbox_geometry(37,21,64)
        self.assertNotEqual(g['scale'][0],g['scale'][1])
        b=torch.tensor([[4.,2.,31.,17.]])
        torch.testing.assert_close(v.map_boxes(v.map_boxes(b,g),g,True),b)

    def test_flip_involution(self):
        b=torch.tensor([[1.,2,4,5]])
        torch.testing.assert_close(v.flip_boxes(b,10),torch.tensor([[6.,2,9,5]]))
        torch.testing.assert_close(v.flip_boxes(v.flip_boxes(b,10),10),b)

    def test_class_aware_nms(self):
        b=torch.tensor([[0.,0,10,10],[0.,0,10,10],[0.,0,10,10]])
        self.assertEqual(batched_nms(b,torch.tensor([.9,.8,.7]),torch.tensor([1,1,2]),.5).tolist(),[0,2])


class DataTests(unittest.TestCase):
    def test_group_disjoint_and_complete(self):
        rows=[{'group':str(i//3),'id':i} for i in range(30)]
        splits=v.group_split(rows)
        self.assertEqual(sorted(r['id'] for x in splits.values() for r in x),list(range(30)))
        groups=[{r['group'] for r in x} for x in splits.values()]
        self.assertTrue(all(not groups[i]&groups[j] for i in range(3) for j in range(i)))

    def test_split_reproducible(self):
        rows=[{'group':str(i),'id':i} for i in range(10)]
        self.assertEqual(v.group_split(rows),v.group_split(rows))
        self.assertNotEqual(v.group_split(rows),v.group_split(rows,seed=24))

    def test_small_group_failure(self):
        with self.assertRaises(ValueError):v.group_split([{'group':'a'}])

    def test_image_alpha_policy(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'image.png';Image.new('RGBA',(3,2),(0,0,0,0)).save(path)
            result=v.load_rgb(path)
            self.assertEqual(result.getpixel((0,0)),(255,255,255))
            self.assertEqual(v.chw_float(result).shape,(3,2,3))
            self.assertTrue(torch.all(v.chw_float(result)==1))

    def test_exif_rotation(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'oriented.jpg';im=Image.new('RGB',(6,4),'red')
            exif=Image.Exif();exif[274]=6;im.save(path,exif=exif)
            result=v.load_rgb(path)
            self.assertEqual(result.size,(4,6))
            self.assertNotIn(274,result.getexif())

    def test_seed_and_distinct_data(self):
        a=v.make_shapes();b=v.make_shapes();c=v.make_shapes(seed=41)
        for x,y in zip(a,b):self.assertTrue(torch.equal(x,y))
        self.assertFalse(torch.equal(a[0],c[0]))

    def test_masks_match_boxes(self):
        _,_,masks,boxes=v.make_shapes(8)
        for mask,box in zip(masks,boxes):
            y,x=torch.where(mask==1)
            self.assertEqual([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],box.int().tolist())

    def test_joint_geometry_alignment(self):
        images,_,masks,boxes=v.make_shapes(2)
        im,b,m=v2.RandomHorizontalFlip(p=1)(tv_tensors.Image(images[0]),
            tv_tensors.BoundingBoxes(boxes[:1],format='XYXY',canvas_size=(24,24)),tv_tensors.Mask(masks[0]))
        torch.testing.assert_close(b.as_subclass(torch.Tensor),v.flip_boxes(boxes[:1],24))
        self.assertTrue(torch.equal(m,masks[0].flip(-1)))
        self.assertTrue(torch.equal(im,images[0].flip(-1)))

    def test_mask_resize_preserves_class_ids(self):
        m=tv_tensors.Mask(torch.tensor([[0,1],[255,2]],dtype=torch.int64))
        resized=v2.Resize((16,16))(m)
        self.assertEqual(set(torch.unique(resized).tolist()),{0,1,2,255})

    def test_loader_keeps_tail(self):
        ds=v.ShapeDataset(10)
        loader=torch.utils.data.DataLoader(ds,batch_size=4,num_workers=0,drop_last=False)
        self.assertEqual([len(y) for _,y in loader],[4,4,2])


class MetricsTests(unittest.TestCase):
    def test_duplicate_is_false_positive(self):
        p=[{'image':'a','box':[0,0,10,10],'score':.9},
           {'image':'a','box':[0,0,10,10],'score':.8},
           {'image':'b','box':[0,0,10,10],'score':.7}]
        result=v.toy_ap(p,{'a':[[0,0,10,10]],'b':[[0,0,10,10]]})
        self.assertEqual([r['tp'] for r in result['rows']],[True,False,True])
        self.assertAlmostEqual(result['ap'],5/6)
        self.assertEqual(result['policy'],'toy-all-points')

    def test_ap_never_matches_other_image(self):
        p=[{'image':'b','box':[0,0,10,10],'score':.9}]
        self.assertEqual(v.toy_ap(p,{'a':[[0,0,10,10]]})['ap'],0)

    def test_ap_empty_predictions(self):
        self.assertEqual(v.toy_ap([],{'a':[[0,0,1,1]]})['ap'],0)

    def test_ap_no_positive_explicit(self):
        with self.assertRaises(ValueError):v.toy_ap([],{'a':[]})

    def test_unmatched_candidate_selected(self):
        # A previous match must not prevent a slightly lower-IoU unused match.
        t={'a':[[0,0,10,10],[2,0,12,10]]}
        p=[{'image':'a','box':[0,0,10,10],'score':.9},
           {'image':'a','box':[1,0,11,10],'score':.8}]
        self.assertEqual(v.toy_ap(p,t)['ap'],1)

    def test_ignore_removed_from_both_masks(self):
        m=v.binary_mask_metrics([[1,0,0],[1,1,1]],[[1,1,0],[1,255,0]])
        self.assertAlmostEqual(m['iou'],.5);self.assertAlmostEqual(m['dice'],2/3)
        self.assertEqual(m['valid_pixels'],5)

    def test_absent_and_all_ignored_explicit(self):
        self.assertIsNone(v.binary_mask_metrics([[0]],[[0]])['iou'])
        self.assertEqual(v.binary_mask_metrics([[1]],[[255]])['valid_pixels'],0)

    def test_mask_probabilities_rejected(self):
        with self.assertRaises(ValueError):v.binary_mask_metrics([[.6]],[[1]])

    def test_confusion_orientation(self):
        self.assertEqual(v.confusion_matrix([0,0,1],[0,1,1]).tolist(),[[1,1],[0,1]])

    def test_calibration_endpoints(self):
        result=v.calibration([0,1],[0,1])
        self.assertEqual(result['ece'],0);self.assertEqual(result['brier'],0)

    def test_calibration_class1_definition(self):
        # One bin: predicted frequency .6, observed frequency .5.
        result=v.calibration([.6,.6],[0,1],bins=1)
        self.assertAlmostEqual(result['ece'],.1)
        self.assertAlmostEqual(result['brier'],.26)


class TrainingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model,cls.report=v.train_classifier()
        cls.segmenter,cls.seg=v.train_segmenter()

    def test_classifier_learns_and_generalizes_to_generator(self):
        self.assertLess(self.report['last_loss'],self.report['first_loss']*.1)
        self.assertGreaterEqual(self.report['valid_accuracy'],.9)

    def test_segmenter_learns_foreground(self):
        self.assertLess(self.seg['last_loss'],self.seg['first_loss']*.2)
        self.assertGreater(self.seg['iou'],.9)

    def test_eval_deterministic_and_grad_free(self):
        x=v.make_shapes(4)[0]
        with torch.inference_mode():a=self.model(x);b=self.model(x)
        self.assertTrue(torch.equal(a,b));self.assertFalse(a.requires_grad)

    def test_trained_state_dict_round_trip(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'state.pt';torch.save(self.model.state_dict(),path)
            restored=v.TinyClassifier().eval();restored.load_state_dict(torch.load(path,weights_only=True))
            x=v.make_shapes(4)[0]
            with torch.inference_mode():torch.testing.assert_close(self.model(x),restored(x))

    def test_training_reproducible(self):
        other,report=v.train_classifier()
        self.assertEqual(self.report,report)
        for a,b in zip(self.model.parameters(),other.parameters()):self.assertTrue(torch.equal(a,b))


class IntegrationTests(unittest.TestCase):
    def test_all_entrypoints_offline(self):
        # Import in one process to avoid repeatedly loading the same runtime.
        with (patch('torch.hub.download_url_to_file',side_effect=AssertionError('No downloads')),
              patch('urllib.request.urlopen',side_effect=AssertionError('No network'))):
            for path in sorted(HERE.glob('[0-9][0-9]_*.py')):
                with self.subTest(example=path.name),patch('sys.argv',[path.name]):
                    output=io.StringIO()
                    with contextlib.redirect_stdout(output):module(path.name).main()
                    self.assertTrue(output.getvalue().strip())

    def test_locator_validation_iou(self):
        output=io.StringIO()
        with patch('sys.argv',['23_train_locator.py']),contextlib.redirect_stdout(output):module('23_train_locator.py').main()
        report=json.loads(output.getvalue())
        self.assertGreater(report['valid_mean_iou'],.65)

    def test_dynamic_onnx_logits(self):
        with TemporaryDirectory() as folder:
            report=module('21_export_onnx.py').export_and_compare(folder)
            self.assertEqual(report['batches'],[1,3,8])
            self.assertLess(max(report['max_errors']),1e-5)
            contract=json.loads((Path(folder)/'contract.json').read_text())
            self.assertEqual(contract['sha256'],v.artifact_contract(Path(folder)/'classifier.onnx')['sha256'])

    def test_trained_model_export_parity(self):
        model,training=v.train_classifier()
        self.assertGreater(training['valid_accuracy'],.9)
        with TemporaryDirectory() as folder:
            report=module('21_export_onnx.py').export_and_compare(folder,model)
            self.assertLess(max(report['max_errors']),1e-4)

    def test_visual_project_deliverables(self):
        for name,columns in [('09_train_classifier.py',1),('17_train_segmenter.py',3),('23_train_locator.py',1)]:
            with self.subTest(project=name),TemporaryDirectory() as folder:
                with patch('sys.argv',[name,'--output',folder]),contextlib.redirect_stdout(io.StringIO()):module(name).main()
                path=Path(folder)
                with Image.open(path/'preview.png') as preview:self.assertEqual(preview.size,(columns*120,8*120))
                report=json.loads((path/'report.json').read_text(encoding='utf-8'))
                self.assertTrue(report)
                self.assertEqual(len(list(path.glob('*.pt'))),1)


if __name__=='__main__':unittest.main()
