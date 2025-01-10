from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from shapely import Point, unary_union
from .earth import _m2deg, _deg2m
from .utils import Qf32


# def change_radius(request):
#     if request.method == 'GET':
#         value = request.GET.get('value')
#         print(value)
#         print("radius =",value)
#         # Optionally, do something with the value here
#         return JsonResponse({'status': 'success', 'value': value})
#     return JsonResponse({'status': 'failed'})


@login_required
def change_geo(request):
    if request.method == 'GET':
        radius = request.GET.get('radius')
        markers = request.GET.get('markers')
        if radius is not None and markers is not None:
            try:                
                radius = int(radius)
                linear = json.loads(markers)
                lon = [linear[n*2] for n in range(len(linear)//2)]
                lat = [linear[n*2+1] for n in range(len(linear)//2)]
                if not lon: contours = "[]"
                else:
                    x = min(lon); X = max(lon)
                    y = min(lat); Y = max(lat)
                    if 0: contours = ("[["+','.join(["[%.6f,%.6f]"]*4)+"]]")%(y,x,Y,x,Y,X,y,X)
                    elif 0:
                        centre = [(x+X)/2,(y+Y)/2]
                        H,V = _deg2m(centre, Qf32(lon), Qf32(lat))
                        contours = []
                        for n in range(len(H)):
                            xy = Point(H[n],V[n]).buffer(radius).exterior.coords.xy
                            h,v = _m2deg(centre, Qf32(xy[0]), Qf32(xy[1]))                            
                            contours.append(list(zip(v.tolist(),h.tolist()))) # note order:v,h
                        contours = json.dumps(contours)
                    else:
                        centre = [(x+X)/2,(y+Y)/2]
                        H,V = _deg2m(centre, Qf32(lon), Qf32(lat))
                        MP = unary_union([Point(H[n],V[n]).buffer(radius) for n in range(len(H))])
                        MP = MP.buffer(-radius)
                        if MP.geom_type == 'MultiPolygon':
                            exteriors = [P.exterior for P in MP.geoms]
                        elif MP.geom_type == 'Polygon':
                            exteriors = [MP.exterior]
                        contours = []
                        for e in exteriors:
                            xy = e.coords.xy
                            h,v = _m2deg(centre, Qf32(xy[0]), Qf32(xy[1]))                            
                            contours.append(list(zip(v.tolist(),h.tolist()))) # note order:v,h                              
                        contours = json.dumps(contours)

                return JsonResponse({
                    'status': 'success',
                    'radius': radius,
                    'point_count': len(lon),
                    'contours': contours
                })
                
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid values'
                }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    }, status=400)

@login_required
def home(request):
    return render(request, 'index.html')
