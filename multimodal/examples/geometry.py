"""Axis-aligned boxes in unrotated, top-left page coordinates."""
import math

def box(value,width=None,height=None):
    if len(value)!=4 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in value):raise ValueError('Four finite coordinates required')
    x0,y0,x1,y1=map(float,value)
    if x0<0 or y0<0 or x1<=x0 or y1<=y0:raise ValueError('Box must have positive area')
    if width is not None and x1>width+1e-6:raise ValueError('Box outside page width')
    if height is not None and y1>height+1e-6:raise ValueError('Box outside page height')
    return (x0,y0,x1,y1)

def iou(a,b):
    a,b=box(a),box(b);intersection=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    return intersection/((a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-intersection)

def normalize(value,width,height):
    if width<=0 or height<=0:raise ValueError('Positive dimensions required')
    x0,y0,x1,y1=box(value,width,height);return (x0/width,y0/height,x1/width,y1/height)

def pixels(value,dpi):
    if not math.isfinite(dpi) or dpi<=0:raise ValueError('Positive DPI required')
    return tuple(x*dpi/72 for x in box(value))

def restore_crop(value,origin,scale):
    if not math.isfinite(scale) or scale<=0 or len(origin)!=2 or any(not math.isfinite(x) or x<0 for x in origin):raise ValueError('Invalid transform')
    a=box(value);return box([a[0]/scale+origin[0],a[1]/scale+origin[1],a[2]/scale+origin[0],a[3]/scale+origin[1]])

def rotate_clockwise(value,width,height):
    x0,y0,x1,y1=box(value,width,height);return (height-y1,x0,height-y0,x1)

def tiles(width,height,side=512,overlap=64):
    if any(type(x) is not int for x in (width,height,side,overlap)) or min(width,height,side)<=0 or not 0<=overlap<side:raise ValueError('Invalid tiling')
    def starts(length):
        result=[0]
        while result[-1]+side<length:result.append(min(result[-1]+side-overlap,length-side))
        return result
    return [(x,y,min(x+side,width),min(y+side,height)) for y in starts(height) for x in starts(width)]
